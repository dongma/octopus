# -*- coding:utf-8 -*-
import scrapy


class ArticleItem(scrapy.Item):
	"""定义了从每个网页收集3个字段：标题、URL和页面最后修改时间"""
	url = scrapy.Field()
	title = scrapy.Field()
	text = scrapy.Field()
	last_updated = scrapy.Field()