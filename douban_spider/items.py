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
    actor = scrapy.Field()
    official_site = scrapy.Field()
    movie_making_zone = scrapy.Field()
    IMDb = scrapy.Field()
    # 豆瓣评分、评价人数
    movie_rate = scrapy.Field()
    votes = scrapy.Field()
    hot_comments = scrapy.Field()

    def gen_insert_sql(self):
        sql = """insert into movie_meta(id, movie_name, year, topics, writer, director, actors, 
            official_site, movie_making_zone, IMDb, movie_rate, votes) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # 对抓取的字段进行处理(将数组拍平)，将actor->转换为string, topics数组->转为string
        actor_data = None
        if self['actor'] is not None and isinstance(self['actor'], list):
            actor_list = self['actor']
            actor_data = ",".join(actor_list)
        topic_data = None
        if self['topics'] is not None:
            topic_data = ",".join(self['topics'])
        director_data = None
        if self['director'] is not None:
            director_data = ",".join(self['director'])
        params = (self["id"], self["movie_name"], self["year"], topic_data, self["writer"], director_data, actor_data,
                  self["official_site"], self["movie_making_zone"], self["IMDb"], self["movie_rate"],
                  self["votes"])
        return sql, params


class Person(scrapy.Item):
    # 抽象人员的数据，包括其在豆瓣的id、角色（导演、编剧、演员）、名称等
    id = scrapy.Field()
    role = scrapy.Field()
    p_name = scrapy.Field()


class HotComment(scrapy.Item):
    # 豆瓣影评信息（热评），包括：网友的id、名称、写评论的时间、影评内容
    data_cid = scrapy.Field()
    movie_id = scrapy.Field()
    user_url = scrapy.Field()
    nick_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    # 星级（几颗星）、投票数（有用数）
    stars = scrapy.Field()
    valid_votes = scrapy.Field()

    def gen_insert_sql(self):
        sql = """insert into comment(data_cid, movie_id, user_url, nick_name, `time`, content, stars, valid_votes)
            values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self["data_cid"], self["movie_id"], self["user_url"], self["nick_name"], self["time"],
                  self["content"], self["stars"], self["valid_votes"])
        return sql, params
