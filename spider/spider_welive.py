#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

from core.crawler import CrawlerBase
from utils import req
from utils.common import format_list
from utils.tomongo import insert
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "welivesecurity"
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        result_list = []
        index_url = "https://www.welivesecurity.com/page/1/"
        res = req.get(index_url)
        if not res:
            return []
        index_soup = BeautifulSoup(res, 'html5lib')

        pages_num = index_soup.select(
            "#news-feed > div.pagination-wrapper.col-xs-12.no-padding > div > a:nth-child(9)")

        for page_num in pages_num:
            max_page = page_num.getText()
        for page in range(1, int(max_page)+1):
            index_soup = BeautifulSoup(res, 'html5lib')
            articles = index_soup.select('article')
            for article in articles:
                infos = article.select('h2')
                for info in infos:
                    inf = info.select('a')
                    for i in inf:
                        new_push = {}
                        new_push['reference'] = i['href']
                        new_push['title'] = i.getText().replace(
                            '\t', '').replace('\n', '')
                        new_push['website'] = 'welive'
                        result_list.append(new_push)

        return result_list

    def get_info(self, infos):
        url = infos['reference']
        title = infos['title']
        index_soup = BeautifulSoup(req.get(url), 'html5lib')
        tables = index_soup.select('td')
        texts = index_soup.select('p')
        result_list = []
        if tables:
            for table in tables:
                result = table.getText().replace(
                    "[", "").replace("]", "").split("\n")
                for i in result:
                    result_list.append(i)
            ioc_list = format_list(result_list)
            if ioc_list:
                ioc_list = format_list(result_list)
                iocs = []
                for ioc in ioc_list:
                    ioc['reference'] = url
                    ioc['title'] = title
                    iocs.append(ioc)

                ioc_list = set_data_md5(iocs)
                insert(ioc_list)
            else:
                for text in texts:
                    result = text.getText().replace(
                        "[", "").replace("]", "").split("\n")
                    for i in result:
                        result_list.append(i)
                ioc_list = format_list(result_list)
                if ioc_list:
                    ioc_list = format_list(result_list)
                    iocs = []
                    for ioc in ioc_list:
                        ioc['reference'] = url
                        ioc['title'] = title
                        iocs.append(ioc)

                    ioc_list = set_data_md5(iocs)
                    insert(ioc_list)
