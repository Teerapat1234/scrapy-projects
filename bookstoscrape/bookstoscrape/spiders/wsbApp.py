import os
import scrapy
from scrapy_playwright.page import PageMethod
import asyncio
from playwright.async_api import async_playwright, Playwright
from PIL import Image

class RedditSpider(scrapy.Spider):

    # getting custom input from command line
    def __init__(self, value=None, *args, **kwargs):
        super(RedditSpider, self).__init__(*args, **kwargs)
        self.post_url = value

    name = "wsbApp"
    allowed_domains = ["reddit.com"]
    # post_urls = ["https://www.reddit.com/r/wallstreetbets/comments/1n1rdc1/daily_discussion_thread_for_august_28_2025/"]

    def start_requests(self):
        if not self.post_url:
            raise Exception("No url value provided.")
        
        project_dir = os.getcwd() 
        image_path = os.path.join(project_dir, "wsb_report.png")

        if os.path.exists(image_path):
            os.remove(image_path)
            self.log(f"Removed old screenshot: {image_path}")

        yield scrapy.Request(
            url=self.post_url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    #we could dynamic wait for element load but the img section of that post is entirely up to the board's continuos update.
                    #I'd rather have this wait time until a clear 1/2 minute is not enough
                    PageMethod("wait_for_timeout", timeout=30000),
                ],
                "playwright_page_screenshot": {
                    "path": image_path,
                    "full_page": True,
                },
                "playwright_context_kwargs": {
                    "ignore_https_errors": True,
                }
            }
        )

    async def parse(self, response):
        await asyncio.sleep(5)

        project_dir = os.getcwd() 
        image_path = os.path.join(project_dir, "wsb_report.png")

        page = response.meta["playwright_page"]
        await page.screenshot(path=image_path, full_page=True)
        self.crop_image(image_path)
        await page.close()

        try:
            if response.meta.get('playwright_page_screenshot'):
                self.log(f"Screenshot action was requested and page loaded successfully.")
            
        except Exception as e:
            self.log(f"An error occurred during the screenshot process: {e}")

    def crop_image(self, image_path):
        try:
            img = Image.open(image_path)
            #left, top, right, bottom
            crop_box = (280, 152, 934, 809)
            cropped_img = img.crop(crop_box)

            os.remove(image_path)
            #Pillow will infer the format from the extension
            cropped_img.save(image_path)
            print(f"Image successfully cropped and saved to {image_path}")

        except FileNotFoundError:
            print(f"Error: Input file not found at {image_path}")
        except Exception as e:
            print(f"An error occurred: {e}")