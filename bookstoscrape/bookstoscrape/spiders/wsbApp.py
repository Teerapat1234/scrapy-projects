import os
import scrapy
from scrapy_playwright.page import PageMethod

class RedditSpider(scrapy.Spider):

    # getting custom input from command line
    def __init__(self, value=None, *args, **kwargs):
        super(RedditSpider, self).__init__(*args, **kwargs)
        self.post_title = value

    name = "wsbApp"
    allowed_domains = ["reddit.com"]
    start_urls = ["https://www.reddit.com/r/wallstreetbets/comments/1n0hpbj/daily_discussion_thread_for_august_26_2025/"]

    def start_requests(self):
        if not self.post_title:
            raise Exception("No custom post title provided.")
        
        project_dir = os.getcwd() 
        image_path = os.path.join(project_dir, "wsb_report.png")

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    # PageMethod("locator.scroll_into_view_if_needed", selector={self.post_title}),
                    PageMethod("wait_for_timeout", timeout=60000),
                ],
                "playwright_page_screenshot": {
                    "path": image_path,
                    "full_page": True,
                },
            }
        )

    async def parse(self, response):
        self.log("Screenshot captured and saved to wsb_report.png")