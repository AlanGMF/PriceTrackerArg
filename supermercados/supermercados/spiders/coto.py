import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class Coto(CrawlSpider):
    name = 'coto'
    page = 'cotodigital3.com.ar'
    allowed_domains = ['cotodigital3.com.ar']
    start_urls = ['https://www.cotodigital3.com.ar/sitios/cdigi/']  #-> base base

    rules = (
        Rule(LinkExtractor(allow="browse"), callback="parse"),
    )

    def parse(self, response):

        for item in response.xpath('//li[contains(@class, "clearfix")]'):

            raw_price = item.xpath('.//span[contains(@class, "atg_store_newPrice")]/text()').get()
            raw_unit_price = item.xpath('.//span[@class= "unit"]/text()').get()

            price = raw_price.replace(' ', '').replace('\t', '').replace('\n', '')
            unit_price = raw_unit_price.replace('  ', '').replace('\t', '').replace('\n', '')

            yield {
                "price_unit" : unit_price,
                "description" :item.xpath('.//div[contains(@class, "descrip_full")]/text()').get(),
                "price" : price,
                "sale_text" : item.xpath('.//span[(@class="text_price_discount")]/text()').get(),
                "sale_price" : item.xpath('.//span[(@class="price_discount")]/text()').get(),
            }
