# Some Web-Scraping/Web-Crawling projects using python  Scrapy

Scrape and Crawled data from several websites and save data in JSON, CSV, XML format using python Scrapy framework. 

run command : scrapy crawl jcb 
or if you're doing wsb img capture : scrapy crawl jcb -a value="post title"

jcb is the name of your spider. Spider will receive page's source code as response.
We're also using Playwright to actually loads the page in instead of just the source html.