# -*- coding:utf-8 -*-
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import certifi
import ssl


def getAbsoluteUrl(base_url, source):
	"""格式化baseUrl地址，将链接url转换为标准格式"""
	if source.startswith('https://www.'):
		url = 'http://{}'.format(source[12:])
	elif source.startswith('https://'):
		url = source
	elif source.startswith("www."):
		url = source[4:]
		url = 'https://{}'.format(url)
	else:
		url = '{}/{}'.format(base_url, source)

	if base_url not in url:
		return None
	return url


def getDownloadPath(base_url, absolute_url, download_dir):
	"""获取image文件下载的路径，并创建文件夹路径"""
	path = absolute_url.replace('www.', '')
	path = path.replace(base_url, '')
	path = download_dir + path
	directory = os.path.dirname(path)

	if not os.path.exists(directory):
		os.makedirs(directory)
	return path


if __name__ == '__main__':
	storeDir = "/Users/madong/Downloads/scarp-images"
	baseUrl = "https://pythonscraping.com"

	html = urlopen('https://pythonscraping.com/', context=ssl.create_default_context(cafile=certifi.where()))
	bs = BeautifulSoup(html, 'html.parser')
	download_list = bs.findAll('img', src=True)
	ssl._create_default_https_context = ssl._create_unverified_context

	for element in download_list:
		fileUrl = getAbsoluteUrl(baseUrl, element['src'])
		if fileUrl is not None:
			print(fileUrl)
			urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, storeDir))
