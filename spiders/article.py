# -*- coding:utf-8 -*-
import scrapy


class ArticleSpider(scrapy.Spider):
	name = 'article'

	def start_requests(self):
		urls = [
			'https://en.wikipedia.org/wiki/Functional_programming',
			"https://en.wikipedia.org/wiki/Monty_Python"
		]
		return [scrapy.Request(url=url, callback=self.parse) for url in urls]

	def parse(self, response, **kwargs):
		url = response.url
		title = response.css('h1::text').extract_first()
		print("Url is: {}".format(url))
		print("title is: {}".format(title))