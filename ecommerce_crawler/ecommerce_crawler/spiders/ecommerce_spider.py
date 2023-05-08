from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from config import base_url, base_domain

class EcommerceSpider(CrawlSpider):
    name = 'ecommerce_spider'
    allowed_domains = [base_domain]
    start_urls = [base_url]

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        page_text = ' '.join(response.css('p::text').getall())
        yield {
            'url': response.url,
            'text': page_text
        }

def run_spider(output_file):
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': output_file
    })

    process.crawl(EcommerceSpider)
    process.start()  # the script will block here until the crawling is finished
