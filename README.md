# Some Web-Scraping/Web-Crawling projects using python  Scrapy
# Also consider using ScrapyAPI dashboard to cycle IP in case yours got banned.

Scrape and Crawled data from several websites and save data in JSON, CSV, XML format using python Scrapy framework. 

run command : scrapy crawl jcb 
or if you're doing wsb img capture : scrapy crawl jcb -a value="post title"

jcb is the name of your spider. Spider will receive page's source code as response.
We're also using Playwright to actually loads the page in instead of just the source html.

Getting Reddit post specifically from this guy wsbApp and just capture the post.
scrapy crawl wsbApp -a value="https://www.reddit.com/r/wallstreetbets/comments/1n1rdc1/daily_discussion_thread_for_august_28_2025/"