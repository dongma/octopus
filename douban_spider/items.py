# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class DoubanSpiderMovie(scrapy.Item):
    # define the fields for your item here like: name = scrapy.Field()
    id = scrapy.Field()
    movie_name = scrapy.Field()
    year = scrapy.Field()
    # 主题类型、导演、编剧、主演的名称、官方网站、制片国家/地区、影片长度、又名、IMDb
    topics = scrapy.Field()
    writer = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    official_site = scrapy.Field()
    movie_making_zone = scrapy.Field()
    IMDb = scrapy.Field()
    # 豆瓣评分、评价人数
    movie_rate = scrapy.Field()
    person_numbers = scrapy.Field()


class Person(scrapy.Item):
    # 抽象人员的数据，包括其在豆瓣的id、角色（导演、编剧、演员）、名称等
    id = scrapy.Field()
    role = scrapy.Field()
    p_name = scrapy.Field()


class HotComment(scrapy.Item):
    # 豆瓣影评信息（热评），包括：网友的id、名称、写评论的时间、影评内容
    movie_id = scrapy.Field()
    audience_id = scrapy.Field()
    audience_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    # 星级（几颗星）、投票数（有用数）
    stars = scrapy.Field()
    voters = scrapy.Field()

