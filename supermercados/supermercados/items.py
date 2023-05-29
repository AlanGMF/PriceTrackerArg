# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SupermercadosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    price_unit= scrapy.Field()
    description= scrapy.Field()
    price = scrapy.Field()
    sale_text= scrapy.Field()
    sale_price= scrapy.Field()

    pass
