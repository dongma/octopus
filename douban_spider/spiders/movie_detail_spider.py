# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MovieDetailSpider(CrawlSpider):
	"""用于解析豆瓣电影详情页的数据，抓取《小偷家族》的数据，很喜欢'是枝裕和'的电影"""
	name = 'douban_movie_spider'
	allowed_domains = ['https://movie.douban.com/']

	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
					  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
		'sec-ch-ua-platform': 'macOS'
	}
	cookies = {
		'DSID': 'AAO-7r4C8Em_M71p_MUerz5aaWOF4e04a6owMHoOJRS0cqIWmdAXLmD2_beeMjWNIN5tgVUqegEVKyChVNoELA45BKFPz9NaXekzwT7XSJiMzZwk6MlXmEcJOyRdSwIJ2ccT5L1sLixl5DcxBz_U5QShbxJKhmzve3Rqh40vcXK-3qRdtzcdYNMD8gskEFDHts9aUDACmK-X62TMV8WX_VWCoHU6Dqm42srxQ6l2csYYh6M93dnDZUyyTHzqHY16UDL0scH5GtifiWefeP5fxv1B_BwtNESGYrh8AqdiwzJAFkJKnnLn2II',
		'IDE': 'AHWqTUmsTPTihXvE5wlKtGnI_ri_3rwNMwXIwfudP2P9-978Dx5zV6x2GdB_XETgWxo'
	}

	def start_requests(self):
		start_urls = ['https://movie.douban.com/subject/27622447/?from=subject-page']
		yield scrapy.Request(url=start_urls[0], headers=self.headers, cookies=self.cookies,
							 callback=self.parse)

	def parse(self, response, **kwargs):
		"""从电影详情页中解析电影详情、演员、导演、热评的相关数据"""
		self.logger.info('Hi this is an movie page! %s', response.url)
		if kwargs.get("debug") is not None:
			from scrapy.shell import inspect_response
			inspect_response(response, self)
		else:
			response.xpath('//div[@id="content"]/h1').get()

	def extract_movie_info(self, response):
		"""从div#id=wrapper的content中取影片名称、发行地、导演、主要演员等数据"""
