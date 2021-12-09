# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import ArticleItem


class ArticleSpider(CrawlSpider):
	"""use $scrapy startproject wikiSpider command to generate spider app"""
	name = 'articles'
	allowed_domain = ['www.wikipedia.org']

	start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
	rules = [
		Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)
	]

	def parse_items(self, response, **kwargs):
		"""parse webpage through CrawlSpider"""
		article_item = ArticleItem()
		article_item['url'] = response.url
		article_item['title'] = response.css('h1::text').extract_first()
		article_item['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
		last_updated = response.css('li#footer-info-lastmod::text')\
			.extract_first()
		article_item['last_updated'] = last_updated.replace('This page was last edited on', '')
		# print(f"Url is: {url}, title is: [{title}], last_updated: {last_updated}")
		return article_item