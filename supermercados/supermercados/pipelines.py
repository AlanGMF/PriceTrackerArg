# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import psycopg2
from itemadapter import ItemAdapter


class SupermercadosPipeline:
    def __init__(self) -> None:

        self.con = psycopg2.connect(
                    port=os.getenv("POSTGRES_PORT"),
                    database=os.getenv("POSTGRES_DATABASE"),
                    user=os.getenv("POSTGRES_USER"),
                    host=os.getenv("POSTGRES_HOST"),
                    password=os.getenv("POSTGRES_PASSWORD")
                    ) 
        
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Products (
        description TEXT,
        market TEXT,
        price TEXT,
        date TEXT,
        CONSTRAINT Products_pk PRIMARY KEY (description, market, date)
        )""")

    def process_item(self, item, spider):
        query = """
        INSERT INTO Products (description, market, price, date) 
        VALUES (%s, %s, %s, %s) 
        ON CONFLICT (description, market, date) DO NOTHING
        """
        self.cur.execute(query, (
            item['description'],
            item['market'],
            item['price'],
            item['date'],
        ))

        self.con.commit()

        return item