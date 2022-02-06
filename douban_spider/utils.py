# -*- coding:utf-8 -*-
from scrapy.selector import Selector


class ParseUtils:
	"""定义解析html webpage的工具类"""

	@staticmethod
	def getMovieSpanValue(elem_data, path, getall=False):
		selector = Selector(text=elem_data)
		if getall is True:
			return selector.xpath(path).getall()
		else:
			return selector.xpath(path).get()