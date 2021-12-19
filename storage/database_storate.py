# -*- coding:utf-8 -*-
import re
import ssl
from datetime import datetime
import random
from urllib.request import urlopen

import certifi
import pymysql as pymysql
from bs4 import BeautifulSoup


random.seed(datetime.now())


def store(title, content, cur):
	"""执行原生sql，将抓取到的title和content写到pages表"""
	cur.execute('insert into pages(title, content) values ("%s", "%s")', (title, content))
	cur.conn.commit()


def getLinks(article_url, cur):
	html = urlopen('https://en.wikipedia.org' + article_url, context=ssl.create_default_context(cafile=certifi.where()))
	bs = BeautifulSoup(html, 'html.parser')
	title = bs.find('h1').get_text()
	content = bs.find('div', {'id': 'mw-content-text'}).find('p').get_text()

	store(title, content, cur)
	return bs.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))


if __name__ == '__main__':
	conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='scraping', charset='utf8')
	cursor = conn.cursor()
	cursor.execute("use scraping")

	links = getLinks('/wiki/Kevin_Bacon', cursor)
	try:
		while len(links) > 0:
			new_article = links[random.randint(0, len(links)-1)].attrs['href']
			print(new_article)
			links = getLinks(new_article)
	finally:
		cursor.close()
		conn.close()