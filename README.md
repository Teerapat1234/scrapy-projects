# Some Web-Scraping/Web-Crawling projects using python  Scrapy
# Also consider using ScrapyAPI dashboard to cycle IP in case yours got banned.

Follow this exact steps: 
- Open env : .venv\Scripts\activate
- install Scrapy for the basic html web scraping : pip install scrapy
- install Playwright for the basic html web scraping : pip install scrapy-playwright
- followed by : playwright install

Scrape and Crawled data from several websites and save data in JSON, CSV, XML format using python Scrapy framework. 

run command : scrapy crawl jcb 

jcb is the name of your spider. Spider will receive page's source code as response.
We're also using Playwright to actually loads the page in instead of just the source html.

Getting Reddit post specifically from this guy wsbApp and just capture the post.
scrapy crawl wsbApp -a value="https://www.reddit.com/r/wallstreetbets/comments/1n1rdc1/daily_discussion_thread_for_august_28_2025/"

Noted: Made to be called by an N8N container through an ssh node. This implements ssh keybased-authen
The keys are manually created and had public key given to this project while another given to the container calling for this container.

Needs to set up secrets inside .env file for the reddit creds and mount it.
docker run -d \
  --name my_app \
  # Mounts the host's secrets.env file into the container at /etc/secrets/secrets.env
  --mount type=bind,source=/path/to/host/secrets.env,target=/etc/secrets/secrets.env,readonly \
  my_docker_image