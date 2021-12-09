# -*- coding:utf-8 -*-
from datetime import datetime
from items import ArticleItem
from string import whitespace


class WikiPipeline(object):
	"""新的管线组件代码，默认情况下是配置在spider#settings.py文件中"""

	def process_item(self, article, spider):
		"""对于每一个管线组件来说，process_item是一个必选方法，scrapy用其来异步处理蜘蛛收集到的Items"""
		date_str = article['last_updated']
		article['last_updated'] = article['last_updated'].replace('This page was last edited on', '')
		article['last_updated'] = article['last_updated'].strip()
		article['text'] = [line for line in article['text'] if line not in whitespace]
		article['text'] = ''.join(article['text'])
		return article