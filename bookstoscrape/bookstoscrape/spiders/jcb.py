import scrapy
import json
import re
from scrapy_playwright.page import PageMethod

class JcbSpider(scrapy.Spider):
    name = "jcb"
    allowed_domains = ["specialoffers.jcb"]
    start_urls = ["https://www.specialoffers.jcb/th/campaign/"]

    def start_requests(self):
        for url in self.start_urls:
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

    async def parse(self, response):
        offers = response.css('a.article-body')
        offersString = offers.getall()
        campaignList = []
        urlPattern = r'(?<=href=")[^"]*'
        categoryPattern = r'class="o-label\s+o-([^"]+)"'

        offersString = offersString[1:]
        offersString = offersString[:(len(offersString)-1) // 2]

        for i in offersString:
            urlMatch = re.findall(urlPattern, i)
            urlMatch = "https://www.specialoffers.jcb" + urlMatch[0]
            categoryMatch = re.findall(categoryPattern, i)[0]

            campaignList.append(
                {
                    "url": urlMatch, 
                    "category": categoryMatch
                }
            )

        print("ans:", campaignList)
        with open("jcb.json", 'w') as file:
            json.dump(campaignList, file, indent=4)
        pass