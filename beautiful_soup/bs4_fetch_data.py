# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError


def getTitle(url):
    """get title attribute value from html page through url"""
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs.body.h1
    except AttributeError as ex:
        print(f"Tag was not found in bs object, {ex}")
        return None
    except HTTPError as ex:
        print(f"the internal server error, page not found. {ex}")
        return None
    return title


def getPageElements():
    """define a function api interface to get title or other tag attribute values"""
    try:
        html = urlopen('http://www.pythonscraping.com/pages/page1.html')
        bs = BeautifulSoup(html.read(), 'html.parser')
        # <h1>An Interesting Title</h1>
        print(bs.h1)
        # 通过getTitle() method获取网页内容
        title = getTitle('http://www.pythonscraping.com/pages/page1.html')
        if title is None:
            print("<h1> tag could not be found")
        else:
            print(f"The <h1> title in html page is: {title}")

        # bs4#class属性取数据，{class='green'}可得到一个任务名称的python列表
        html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
        bs = BeautifulSoup(html.read(), 'html.parser')
        nameList = bs.findAll('span', {'class': 'green'})
        for name in nameList:
            print(name.get_text())
        # 从全局html中搜索含有'the prince' text对应tag的数量，总7个内容
        nameList = bs.find_all(text='the prince')
        print(f"the length of nameList array is: {len(nameList)}")

    except HTTPError as ex:
        print(ex)  # 返回空值，中断程序或执行另一种方案
    except URLError as ex:
        print('the server could not be found!')
    else:
        print("it worked!")


if __name__ == '__main__':
    try:
        html = urlopen('http://www.pythonscraping.com/pages/page3.html')
        bs = BeautifulSoup(html, 'html.parser')

        for sibling in bs.find('table', {'id': 'giftList'}).tr.next_siblings:
            print(sibling)
        # 通过.parent获取父标签，之后使用previous_siblings.get_text()获取父tag的相临节点 $15.00
        print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
    except HTTPError as ex:
        print(f"scrap data from page3.html cause exception: {ex}")
    else:
        print("it actually worked!")