# ecommerce_crawler/spiders/ecommerce_spider.py
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class EcommerceSpider(CrawlSpider):
    name = 'ecommerce_spider'
    allowed_domains = ['mysunday2sunday.com']  # Replace with the actual domain
    start_urls = ['https://mysunday2sunday.com/']  # Replace with the actual homepage URL

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        page_text = ' '.join(response.css('p::text').getall())
        yield {
            'url': response.url,
            'text': page_text
        }
