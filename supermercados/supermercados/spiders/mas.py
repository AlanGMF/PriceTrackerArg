import time
import json

import scrapy
from scrapy.loader import ItemLoader
from supermercados.items import SupermercadosItem

class mas(scrapy.Spider):
    name = 'mas'
    allowed_domains = ['masonline.com.ar']
    start_urls = [
        'https://www.masonline.com.ar/aceites-y-aderezos?page=1',
        'https://www.masonline.com.ar/aceitunas-y-encurtidos?page=1',
        'https://www.masonline.com.ar/arroz-y-legumbres?page=1',
        'https://www.masonline.com.ar/conservas?page=1',
        'https://www.masonline.com.ar/desayuno-y-golosinas?page=1',
        'https://www.masonline.com.ar/panaderia?page=1',
        'https://www.masonline.com.ar/lacteos?page=1',
        'https://www.masonline.com.ar/pastas-y-tapas?page=1',
        'https://www.masonline.com.ar/carniceria-y-pescaderia?page=1',
        'https://www.masonline.com.ar/frutas-y-verduras?page=1',
        'https://www.masonline.com.ar/fiambreria?page=1',
        'https://www.masonline.com.ar/aperitivos?page=1',
        'https://www.masonline.com.ar/cervezas?page=1',
        'https://www.masonline.com.ar/vinos-y-espumantes?page=1',
        'https://www.masonline.com.ar/bebidas-blancas-y-licores?page=1',
        'https://www.masonline.com.ar/a-base-de-hierbas?page=1',
        'https://www.masonline.com.ar/aguas?page=1',
        'https://www.masonline.com.ar/alimento-perro?page=1',
        'https://www.masonline.com.ar/alimento-gato?page=1',
        'https://www.masonline.com.ar/accesorios-y-otras-mascotas?page=1',
        'https://www.masonline.com.ar/cuidado-corporal?page=1',
        'https://www.masonline.com.ar/cuidado-del-adulto?page=1',
        'https://www.masonline.com.ar/cuidado-del-bebe?page=1', 
        'https://www.masonline.com.ar/cuidado-del-cabello?page=1',
        'https://www.masonline.com.ar/cuidado-facial?page=1',
        'https://www.masonline.com.ar/cuidado-oral?page=1',
        'https://www.masonline.com.ar/accesorios-de-limpieza?page=1',
        'https://www.masonline.com.ar/desodorante-de-ambientes?page=1',
        'https://www.masonline.com.ar/insecticidas?page=1',
        'https://www.masonline.com.ar/lavandina?page=1',
        'https://www.masonline.com.ar/limpieza-de-baño?page=1',
        'https://www.masonline.com.ar/limpieza-de-calzado?page=1',
        'https://www.masonline.com.ar/limpieza-de-cocina?page=1',
        'https://www.masonline.com.ar/alimentacion-infantil?page=1',
        'https://www.masonline.com.ar/cuidado-del-bebe?page=1',
        'https://www.masonline.com.ar/cuidado-mama?page=1',
        'https://www.masonline.com.ar/primera-infancia?page=1',
        ]

    def parse(self, response):
        current_page = int(response.url.split('=')[-1])
        next_page = response.url.replace(f'page={current_page}', f'page={current_page + 1}')

        json_str = response.xpath('//div[@class="flex flex-column min-vh-100 w-100"]//script[@type="application/ld+json"]/text()').get()

        if json_str:
            try:
                json_obj = json.loads(json_str)
                items = json_obj["itemListElement"]
                
                if items:
                    for item in items:

                        loader = ItemLoader(item=SupermercadosItem(), selector=item)

                        a = item["item"]["name"]
                        b = str(item["item"]["offers"]["offers"][0]["price"])

                        loader.add_value("description", a)
                        loader.add_value("price", b)
                        loader.add_value("market", response.url.split(".")[1])
                    
                        yield loader.load_item()
            except Exception as e:
                pass
            
            if current_page % 2 == 0:
                time.sleep(1)
            
            if response.xpath('//a[@tabindex="0" and @rel="next"]'):
                yield response.follow(next_page, callback=self.parse)
