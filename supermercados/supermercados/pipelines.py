# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SupermercadosPipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect('mysql.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tabla1 (
        description TEXT,
        market TEXT,
        price TEXT
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO tabla1 (description, market, price) VALUES (?, ?, ?)""", (
            item['description'],
            item['market'],
            item['price'],
        ))

        self.con.commit()

        return item