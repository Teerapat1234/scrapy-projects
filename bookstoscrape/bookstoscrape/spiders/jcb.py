import scrapy
import json
from scrapy_playwright.page import PageMethod

class JcbSpider(scrapy.Spider):
    name = "jcb"
    allowed_domains = ["specialoffers.jcb"]
    start_urls = ["https://www.specialoffers.jcb/th/campaign/"]

    def start_requests(self):
        for url in self.start_urls:
            print("test loop")
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_context": "default_context",
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', 'a.article-body', state='attached')
                    ]
                },
                callback=self.parse,
            )

    def parse(self, response):
        # articles = response.css("#offers-entry-wrap").getall()

        # offers = response.css("p.ttl").getall()
        offers = response.css('a.article-body')
        print("test ", offers)

        # with open("jcb.json", 'w') as file:
        #     json.dump(offers, file, indent=4)
        pass