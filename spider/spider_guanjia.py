#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

from core.crawler import CrawlerBase
from utils.common import format_list
from utils.tomongo import insert
from utils import req
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_guanjia"
    auth = "fairy"
    thread = 1

    def get_url_list(self):
        url_list = []
        page = 1
        flag = 0
        while flag == 0:
            url = "https://www.freebuf.com/author/腾讯电脑管家?page={}".format(
                str(page))
            res = req.get(url)
            if not res:
                continue

            resp_text = res.replace('<br />', '\n')
            if '该用户还没发表文章!' in resp_text:
                break
            soup = BeautifulSoup(resp_text, 'html5lib')
            articles = soup.select('dd')
            for article in articles:
                if article.find_all('a'):
                    title = article.find_all('a')[0].getText()
                    href = article.find_all('a')[0].get('href')
                    time = article.find_all('div', 'time')[0].getText()
                    if href:
                        url_list.append((title, href, time))
                    else:
                        flag = 1
                        break
            page += 1

        return url_list

    def get_info(self, target):
        url = target[1]
        result = []
        resp_text = req.get(url)
        if not resp_text:
            return

        soup = BeautifulSoup(resp_text, 'html5lib')
        content = soup.select_one(
            "#getWidth > div.article-wrap.panel.panel-default").getText()

        if "IOCs" in content and "参考" in content:
            for ioc in format_list(content[content.find('IOCs'):content.rfind('参考')].split('\n')):
                ioc['reference'] = url
                ioc['name'] = target[0]
                ioc['disclosuretime'] = target[2]
                result.append(ioc)
        else:
            for ioc in format_list(content.split('\n')):
                ioc['reference'] = url
                ioc['name'] = target[0]
                ioc['disclosuretime'] = target[2]
                result.append(ioc)

        ioc_info = set_data_md5(result)
        insert(ioc_info)
