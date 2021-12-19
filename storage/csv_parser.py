# -*- coding:utf-8 -*-
import csv
import ssl
from urllib.request import urlopen

import certifi
from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = urlopen('https://en.wikipedia.org/wiki/Comparison_of_text_editors',
                   context=ssl.create_default_context(cafile=certifi.where()))
    bs = BeautifulSoup(html, 'html.parser')
    # 取当前页面上的第一个表格，作为主对比表格
    table = bs.findAll('table', {'class': 'wikitable'})[0]
    rows = table.findAll('tr')

    csvfile = open('/Users/madong/Downloads/editors.csv', 'wt+')
    writer = csv.writer(csvfile)
    try:
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            writer.writerow(csvRow)
    finally:
        csvfile.close()