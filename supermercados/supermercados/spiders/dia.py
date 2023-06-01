import time
import json

import scrapy
from scrapy.loader import ItemLoader
from supermercados.items import SupermercadosItem

class Dia(scrapy.Spider):
    name = 'dia'
    allowed_domains = ['diaonline.supermercadosdia.com.ar']
    start_urls = [
        'https://diaonline.supermercadosdia.com.ar/almacen?page=1',
        'https://diaonline.supermercadosdia.com.ar/congelados?page=1',
        'https://diaonline.supermercadosdia.com.ar/limpieza?page=1',
        'https://diaonline.supermercadosdia.com.ar/perfumeria?page=1',
        'https://diaonline.supermercadosdia.com.ar/bebes-y-ninos?page=1',
        'https://diaonline.supermercadosdia.com.ar/mascotas?page=1',
        'https://diaonline.supermercadosdia.com.ar/electro-hogar?page=1',
        'https://diaonline.supermercadosdia.com.ar/bebidas?page=1',
        'https://diaonline.supermercadosdia.com.ar/desayuno?page=1',
        'https://diaonline.supermercadosdia.com.ar/frescos?page=1',
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
                    for itemz in items:
                        
                        loader = ItemLoader(item=SupermercadosItem(), selector=itemz)

                        a = itemz["item"]["name"]
                        b = str(itemz["item"]["offers"]["offers"][0]["price"])

                        loader.add_value("description", a)
                        loader.add_value("price", b)
                        loader.add_value("market", response.url.split(".")[1])
                    
                        yield loader.load_item()

                    if current_page % 2 == 0:
                        time.sleep(1)
                    yield response.follow(next_page, callback=self.parse)
            except Exception as e:
                pass
