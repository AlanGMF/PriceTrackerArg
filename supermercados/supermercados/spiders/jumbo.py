import time
import json

import scrapy
from scrapy.loader import ItemLoader
from supermercados.items import SupermercadosItem

class Dia(scrapy.Spider):
    name = 'jumbo'
    allowed_domains = ['jumbo.com.ar']
    start_urls = [
        "https://www.jumbo.com.ar/almacen?map=category-1&page=1",
        "https://www.jumbo.com.ar/bebidas?map=category-1&page=1",
        "https://www.jumbo.com.ar/frutas-y-verduras?map=category-1&page=1",
        "https://www.jumbo.com.ar/carnes?map=category-1&page=1",
        "https://www.jumbo.com.ar/pescados-y-mariscos?map=category-1&page=1",
        "https://www.jumbo.com.ar/quesos-y-fiambres?map=category-1&page=1",
        "https://www.jumbo.com.ar/lacteos?map=category-1&page=1",
        "https://www.jumbo.com.ar/congelados?map=category-1&page=1",
        "https://www.jumbo.com.ar/panaderia-y-reposteria?map=category-1&page=1",
        "https://www.jumbo.com.ar/perfumeria?map=category-1&page=1",
        "https://www.jumbo.com.ar/limpieza?map=category-1&page=1",
        "https://www.jumbo.com.ar/mascotas?map=category-1&page=1",
        ]

    def parse(self, response):

        current_page = int(response.url.split('=')[-1])
        next_page = response.url.replace(f'page={current_page}', f'page={current_page + 1}')

        json_str = response.xpath('//div[@class="pr0 items-stretch vtex-flex-layout-0-x-stretchChildrenWidth   flex"]//script[@type="application/ld+json"]/text()').get()
    
        if json_str:
            try:
                json_obj = json.loads(json_str)
                items = json_obj["itemListElement"]
                
                if items:
                    for item in items:

                        loader = ItemLoader(item=SupermercadosItem(), selector=item)

                        a = item["item"]["name"]
                        b = str(item["item"]["offers"]["offers"][0]["price"])

                        # loader.add_value("price_unit", "")
                        loader.add_value("description", a)
                        loader.add_value("price", b)
                        loader.add_value("market", response.url.split(".")[1])
                        # loader.add_value("sale_text", "")
                        # loader.add_value("sale_price", "")
                    
                        yield loader.load_item()
            except Exception as e:
                pass
            
            if current_page % 2 == 0:
                time.sleep(1)
            if response.xpath('//button[@tabindex="0"]/div/text()'):
                yield response.follow(next_page, callback=self.parse)
