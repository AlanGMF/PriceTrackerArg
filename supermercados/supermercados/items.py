# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

def remove_currency_n_double_space(value):
    return value.replace('$', '').replace('  ', '').replace('\t', '').replace('\n', '').strip()

class SupermercadosItem(scrapy.Item):
    # define the fields for your item here like:

    price_unit = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency_n_double_space), output_processor = TakeFirst())
    description = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency_n_double_space), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency_n_double_space), output_processor = TakeFirst())
    sale_text = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency_n_double_space), output_processor = TakeFirst())
    sale_price = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency_n_double_space), output_processor = TakeFirst())
    market = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(output_processor = TakeFirst())
