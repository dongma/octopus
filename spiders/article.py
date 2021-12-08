# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ArticleSpider(CrawlSpider):
	"""use $scrapy startproject wikiSpider command to generate spider app"""
	name = 'articles'
	allowed_domain = ['www.wikipedia.org']

	start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
	rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)]

	def parse_items(self, response, **kwargs):
		"""parse webpage through CrawlSpider"""
		url = response.url
		title = response.css('h1::text').extract_first()
		text = response.xpath('//div[@id="mw-content-text"]//text()').extract()
		last_updated = response.css('li#footer-info-lastmod::text')\
			.extract_first()
		last_updated = last_updated.replace('This page was last edited on ', '')
		print(f"Url is: {url}, title is: [{title}], text is: {text}, last_updated: {last_updated}")