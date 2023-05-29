import time
import json

import scrapy

class Dia(scrapy.Spider):
    name = 'disco'
    allowed_domains = ['disco.com.ar']
    start_urls = [
        "https://www.disco.com.ar/almacen?map=category-1&page=1",
        "https://www.disco.com.ar/bebidas?map=category-1&page=1",
        "https://www.disco.com.ar/frutas-y-verduras?map=category-1&page=1",
        "https://www.disco.com.ar/carnes?map=category-1&page=1",
        "https://www.disco.com.ar/pescados-y-mariscos?map=category-1&page=1",
        "https://www.disco.com.ar/quesos-y-fiambres?map=category-1&page=1",
        "https://www.disco.com.ar/lacteos?map=category-1&page=1",
        "https://www.disco.com.ar/congelados?map=category-1&page=1",
        "https://www.disco.com.ar/panaderia-y-reposteria?map=category-1&page=1",
        "https://www.disco.com.ar/perfumeria?map=category-1&page=1",
        "https://www.disco.com.ar/limpieza?map=category-1&page=1",
        "https://www.disco.com.ar/mascotas?map=category-1&page=1",
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

                        yield {
                            "price_unit" : "",
                            "description" : item["item"]["name"],
                            "price" : item["item"]["offers"]["offers"][0]["price"],
                            "sale_text" : "" ,
                            "sale_price" : "" , 
                        }
            except Exception as e:
                pass
            
            if current_page % 2 == 0:
                time.sleep(1)
            if response.xpath('//button[@tabindex="0"]/div/text()'):
                yield response.follow(next_page, callback=self.parse)