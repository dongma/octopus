# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql as pymysql
from douban_spider.items import DoubanSpiderMovie


class DoubanSpiderPipeline:
    """将抓取的数据写入到mysql数据库中"""
    cursor = None

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
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        # self.log.info("enter DoubanSpiderPipeline#process_item method, elem data: {}",
        #               json.dumps(item.__dict__, ensure_ascii=False))
        if isinstance(item, DoubanSpiderMovie):
            sql, params = item.gen_insert_sql()
            print(f"[debug] movie, generate sql {sql}, params: {params}")
            self.cursor.execute(sql, params)
            self.connect.commit()
            # 从电影的meta信息中取得该电影的5条热评，并将其写入数据库中 (将生成的SQL通过log打印)
            hot_comments = item['hot_comments']
            for elem in hot_comments:
                sql, params = elem.gen_insert_sql()
                print(f"[debug] hot comments, generate sql {sql}, params: {params}")
                self.cursor.execute(sql, params)
                self.connect.commit()
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