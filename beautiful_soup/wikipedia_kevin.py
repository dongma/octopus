# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import datetime
import random
import requests

random.seed(datetime.datetime.now())
pages = set()


def get_links(article_url):
    """construct wikipedia request url using url format"""
    global pages
    html = urlopen('https://en.wikipedia.org{}'.format(article_url))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('页面缺少一些属性值!不过不用担心!')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile(''))
                new_page = link.attrs['href']
                print(f"{'-'*20}, new_page: {new_page}")
                pages.add(new_page)
                get_links(new_page)


def get_internal_links(bs, include_url):
    """get all internal links from html page which start with '/'"""
    include_url = '{}://{}'.format(urlparse(include_url).scheme, urlparse(include_url).netloc)
    internal_links = []
    # 找到所有以"/"开头的链接，这些链接为内部链接 (internal_link)
    for link in bs.find_all('^(/|.*)' + include_url +')'):
        if link.attrs['href'] not in internal_links:
            if link.attrs['href'].startswith('/'):
                internal_links.append(include_url + link.attrs['href'])
            else:
                internal_links.append(link.attrs['href'])
    return internal_links


if __name__ == '__main__':
    # links = getLinks('/wiki/Kevin_Bacon')
    # while len(links) > 0:
    #     new_article = links[random.randint(0, len(links) - 1)].attrs['href']
    # getLinks('')
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"}
    data = requests.get('https://movie.douban.com/subject/2222996/', headers=headers,
                        timeout=10)
    bs = BeautifulSoup(data.text, 'html.parser')