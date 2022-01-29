# -*- coding:utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
	# name表示爬虫的名字，在整个project中每个爬虫的名字都必须是唯一的
	name = "quotes"

	def start_requests(self):
		"""start_requests方法必须返回一个iterable of Requests，爬虫会根据request开始抓取数据"""
		# usage 1, 用scrap抓取两个网页数据: urls = [
		# 	'http://quotes.toscrape.com/page/1/',
		# 	'http://quotes.toscrape.com/page/2/',
		# ]
		# for url in urls:
		# 	yield scrapy.Request(url=url, callback=self.parse)
		url = 'http://quotes.toscrape.com/'
		tag = getattr(self, 'tag', None)
		if tag is not None:
			url = url + 'tag/' + tag
		yield scrapy.Request(url, self.parse)

	def parse(self, response, **kwargs):
		"""parse方法是用来从response中解析下载的网页数据，hold the page content for further use"""
		for quote in response.css('div.quote'):
			yield {
				'test': quote.css('span.text::text').get(),
				'author': quote.css('small.author::text').get(),
				'tags': quote.css('div.tags a.tag::text').getall()
			}

		next_page = response.css('li.next a::attr(href)').get()
		if next_page is not None:
			# urljoin(url) method used to build a full absolute URL, since the links can be relative
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
	# usage 1: 将url对应的网页数据完全抓取下来，将对应的html文件保存在本地
	# page = response.url.split("/")[-2]
	# filename = f'quotes-{page}.html'
	# with open(filename, 'wb') as f:
	# 	f.write(response.body)
	# self.log(f'saved crawling data file {filename}')
