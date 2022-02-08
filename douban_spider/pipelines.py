# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql as pymysql


class DoubanSpiderPipeline:
    """将抓取的数据写入到mysql数据库中"""
    def process_item(self, item, spider):
        return item

    def __init__(self, mysql_uri, mysql_db, mysql_user, password):
        self.mysql_uri = mysql_uri
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.password = password
        self.connect = pymysql.connect(host=self.mysql_uri, user=self.mysql_user, password=self.password,
                                       db=self.mysql_db, charset='utf8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URL'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE', 'douban_datahub'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD')
        )

    def open_spider(self, spider):
        cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class MongoPipeline:
    def process_item(self, item, spider):
        return item


class CsvPipeline:
    def process_item(self, item, spider):
        return item


class GraphDataPipeline:
    """从scrapy抓取的movie meta数据中抽取点、边表数据"""
    def process_item(self, item, spider):
        return item