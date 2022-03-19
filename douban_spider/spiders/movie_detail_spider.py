# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from douban_spider.items import DoubanSpiderMovie, HotComment
import json
from scrapy.selector import Selector
from douban_spider.utils import ParseUtils


class MovieDetailSpider(CrawlSpider):
	"""用于解析豆瓣电影详情页的数据，抓取《小偷家族》的数据，很喜欢'是枝裕和'的电影"""
	name = 'douban_movie_spider'
	allowed_domains = ['douban.com']

	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
					  'Chrome/99.0.4844.51 Safari/537.36',
		'sec-ch-ua-platform': 'macOS'
	}
	cookies = {
		# 'viewed': '33386709_24737674_6424904_1101779_25779298_26274624_26772677_2054201_35196328_26381341',
		# 'bid': 'fA9hGAT_iEQ',
		# 'gr_user_id': '8a699ab6-19ec-4a4f-88c8-1417a5b04adc',
		# '__gads': 'ID=3f43dda6a3d2833b-229f37c9c7d000ab:T=1646294592:RT=1646294592:S=ALNI_MafUa87tRIqF3w_gkXASOt4aGLcDQ',
		# 'll': '108288',
		# '__utmc': '30149280',
		# 'dbcl2': '253742920:baWr4fpDIaU',
		# 'ck': '=Kc9Q',
		# '__utma': '30149280.1137633045.1646306975.1646306975.1647619819.2',
		# '__utmb': '30149280.0.10.1644292281',
		# '__utmz': '30149280.1647619819.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
		# 'push_noty_num': '0',
		# 'push_doumail_num': '0'

		"bid": "fdyZudJS8XY",
		"douban - fav - remind": "1",
		"ll": "108288",
		"__gads": "ID = 3f43dda6a3d2833b - 229f37c9c7d000ab: T = 1646294592:RT = 1646294592:S = ALNI_MafUa87tRIqF3w_gkXASOt4aGLcDQ",
		"gr_user_id": "8a699ab6 - 19ec - 4a4f - 88c8 - 1417a5b04adc",
		"viewed": "33386709_24737674_6424904_1101779_25779298_26274624_26772677_2054201_35196328_26381341",
		"dbcl2": "161751427:grj+9+RcpSw",
		"frodotk": "30bc89815063bb8a92359c83f12b329e",
		"talionusr": "eyJpZCI6ICIxNjE3NTE0MjciLCAibmFtZSI6ICJTYW1NYUNvZGUifQ==",
		"__utma": "30149280.1137633045.1646306975.1647619819.1647707830.3",
		"__utmb": "30149280.0.10.1647707830",
		"__utmc": "30149280",
		"__utmz": "30149280.1647707830.3.3.utmcsr = google | utmccn = (organic) | utmcmd = organic | utmctr = (not% 20provided)"
	}

	# 是否开启调试模式，用于调试爬虫抓取json结果: scrapy crawl douban_movie_spider -a debug=true
	enable_debug = False

	# rules会用正则表达式匹配link url，匹配的地址会用scrapy重新抓取 (其实，这块就可以依据Rule#抓取不同的对象)
	rules = [
		Rule(LinkExtractor(allow=r'/subject/[0-9]+/'), callback='parse', follow=True,
			 cb_kwargs={'movie_url': True})
		# Rule(LinkExtractor(allow=r'/topic/[0-9]+/'), callback='topic', follow=True,
		# 	 cb_kwargs={'movie_url': True})
	]

	def __init__(self, *a, **kwargs):
		super().__init__(*a, **kwargs)
		self.logger.info("whether enable debug mode from command line: %s", kwargs.get("debug"))
		if str(kwargs.get("debug")).upper() == "TRUE" and bool(kwargs.get("debug")) is True:
			self.enable_debug = True

	def start_requests(self):
		start_urls = ['https://movie.douban.com/subject/27622447/?from=subject-page']
		yield scrapy.Request(url=start_urls[0], headers=self.headers, cookies=self.cookies,
							 callback=self.parse)

	def parse(self, response, **kwargs):
		"""从电影详情页中解析电影详情、演员、导演、热评的相关数据"""
		if kwargs.get('movie_url') is None or kwargs.get('movie_url') is True:
			self.logger.info('Hi this is an movie page! %s, debug mode: %s', response.url, self.enable_debug)
			if self.enable_debug:
				from scrapy.shell import inspect_response
				inspect_response(response, self)
			else:
				movie = self.extract_movie_info(response)
				if movie is None:
					self.logger.info("couldn't acquire movie data from movie url, url: %s", response.url)
					return None

				# 从response中解析hot_comment#div热评数据
				hot_comments = self.get_hot_comments_data(movie['id'], response)
				movie['hot_comments'] = hot_comments
				yield movie
				# 从电影推荐列表中#抓取"喜欢这部电影的人也喜欢"的影片列表 (用scrapy抓取这些数据)
				recommend_movies = response.css('div.recommendations-bd dd>a::attr(href)').getall()
				for movie_url in recommend_movies:
					joined_movie_url = response.urljoin(movie_url)
					# self.logger.info(f"movie_url: {movie_url}, joined movie_url value: {joined_movie_url}")
					yield scrapy.Request(url=joined_movie_url, headers=self.headers, cookies=self.cookies,
										 callback=self.parse)
		else:
			print(f"this is not an movie meta data url, url data: {response.url}")
			return None

	@staticmethod
	def extract_movie_info(response):
		"""从div#id=wrapper的content中取影片名称、发行地、导演、主要演员等数据"""
		titles = response.xpath('//div[@id="content"]/h1/span/text()').getall()
		movie = DoubanSpiderMovie()
		if len(titles) == 2:
			movie['movie_name'] = titles[0]
			movie['year'] = titles[1].replace('(', '').replace(')', '')
		# 从div#info#span list中开始解析，解析导演、编剧的名称、主题类型
		details = response.xpath('//div[@id="info"]/span').getall()

		if len(details) > 0:
			movie['director'] = ParseUtils.getMovieSpanValue(details[0], "//span/span/a/text()")
			movie['writer'] = ParseUtils.getMovieSpanValue(details[1], "//span/span/a/text()")
			movie['actor'] = ParseUtils.getMovieSpanValue(details[2], "//span/span/a/text()", getall=True)
		else:
			return None

		movie['topics'] = response.xpath('//div[@id="info"]/span[contains(@property, "v:genre")]/text()') \
			.getall()
		movie['official_site'] = response.xpath('//div[@id="info"]/span[contains(@rel, "nofollow")]/text()') \
			.get()

		# @please see https://stackoverflow.com/questions/43646685/select-sequence-of-next-siblings-in-scrapy/43647765
		regex = '//text()[preceding-sibling::span[text()="制片国家/地区:"]]'
		movie['movie_making_zone'] = response.xpath(regex).get()
		regex = '//text()[preceding-sibling::span[text()="IMDb:"]]'
		movie['IMDb'] = response.xpath(regex).get()
		# 解析影片的评分、参与评价的人数数据，从response.url中获取movie的id数据
		avg_rate = response.xpath("//strong[contains(@property, 'v:average')]/text()").get()
		movie['movie_rate'] = avg_rate
		movie['votes'] = response.xpath("//span[contains(@property, 'v:votes')]/text()").get()

		douban_id = response.url.split("subject")[1].split("/")[1]
		movie['id'] = douban_id
		print(f"scraping movie data: {json.dumps(movie.__dict__, ensure_ascii=False)}, movie title:《{titles}》")
		return movie

	@staticmethod
	def get_hot_comments_data(movie_id, response):
		"""从div#hot-comments中获取电影的热评数据，包括网友的id、名称、评论内容、打几棵星"""
		hot_comments = response.xpath("//div[@id='hot-comments']/div").getall()
		comment_list = []
		for div_elem in hot_comments:
			selector = Selector(text=div_elem)
			data = HotComment()
			data['data_cid'] = selector.xpath('//@data-cid').get()
			data['movie_id'] = movie_id
			data['valid_votes'] = selector.xpath("//span[contains(@class, 'vote-count')]/text()").get()

			# 从hot_comments#div的span中解析评论内容、投票数、评论时间、用户url地址、star数量
			data['content'] = selector.xpath("//span[contains(@class, 'short')]/text()").get()
			data['time'] = selector.xpath("//span[contains(@class, 'comment-time')]/text()").get().strip()
			data['nick_name'] = selector.xpath("//span[contains(@class, 'comment-info')]/a/text()").get()
			data['user_url'] = selector.xpath("//span[contains(@class, 'comment-info')]/a/@href").get()
			# 计算此条评论给了几颗星，从span#allstar40 class中进行提取
			star_class = selector.xpath("//span[contains(@class, 'rating')]/@class").get()
			data['stars'] = int(star_class.replace('rating', '').replace('allstar', '')) / 10
			comment_list.append(data)
			print(f"data-cid: {data['data_cid']}, hot comment: {json.dumps(data.__dict__, ensure_ascii=False)}")
		return comment_list
