from datetime import datetime

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from supermercados.items import SupermercadosItem

class Coto(CrawlSpider):
    name = 'coto'
    allowed_domains = ['cotodigital3.com.ar']
    start_urls = ['https://www.cotodigital3.com.ar/sitios/cdigi/']

    rules = (
        Rule(LinkExtractor(allow="browse"), callback="parse"),
    )

    def parse(self, response):
        current_date = datetime.now().date()
        date_string = current_date.strftime("%Y-%m-%d")

        for product in response.xpath('//li[contains(@class, "clearfix")]'):

            loader = ItemLoader(item= SupermercadosItem(), selector=product)
            
            loader.add_xpath('price_unit', './/span[@class= "unit"]/text()')
            loader.add_xpath('description', './/div[contains(@class, "descrip_full")]')
            loader.add_xpath('price', './/span[contains(@class, "atg_store_newPrice")]/text()')
            loader.add_xpath('sale_text', './/span[(@class="text_price_discount")]/text()')
            loader.add_xpath('sale_price', './/span[(@class="price_discount")]/text()')
            loader.add_value("market", response.url.split(".")[1])
            loader.add_value("date", date_string)
            
            yield loader.load_item()
