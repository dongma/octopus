# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Content:
    """代表网站上的一块内容，如新闻文章、故事等内容"""
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def getPage(self, url):
        req = requests.get(url)
        return BeautifulSoup(req.text, 'html.parser')

    def scrapedNYTimes(self, url):
        bs = self.getPage(url)
        title = bs.find("h1").text
        lines = bs.find_all('p', {"class": "story-content"})
        body = '\n'.join([line.text for line in lines])
        return Content(url, title, body)

    def scrapeBrookings(self, url):
        bs = self.getPage(url)
        title = bs.find("h1").text
        body = bs.find("div", {"class": "post-body"}).text
        return Content(url, title, body)


class Website:
    """描述网站结构的信息，只存储关于如何抓取数据的指令"""
    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.titleTag = title_tag
        self.bodyTag = body_tag


class Crawler:
    """Crawler对象用于抓取任务网站的任务网页标题和内容"""
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return ''

    def safeGet(self, page_obj, selector):
        """用于从一个BeautifulSoup对象和一个选择器获取内容的辅助函数，当未找到时，就返回空字符串"""
        selected_elements = page_obj.select(selector)
        if selected_elements is not None and len(selected_elements) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elements])
        return ''

    def parse(self, site, url):
        """从指定url中提取内容，包括页面的title和body内容"""
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.title_tag)
            body = self.safeGet(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                print(content)


if __name__ == '__main__':
    print("ok!")