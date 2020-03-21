#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from utils import req
from utils.tomongo import insert
from core.crawler import CrawlerBase
from utils.common import format_list
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_netlab360"
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        result = []
        for page_num in range(1, 3000):
            url = "https://blog.netlab.360.com/page/{}/".format(page_num)
            res = req.get(url)
            if not res:
                continue
            soup = BeautifulSoup(res, "html5lib").select(
                ".post-card-content-link")
            for info in soup:
                infos = {}
                url = urljoin("https://blog.netlab.360.com/", info['href'])
                if url:
                    title = info.select_one('h2').getText()
                    infos['reference'] = url
                    infos['title'] = title
                    infos['website'] = "netlab360"
                    result.append(infos)
                else:
                    return result

    def get_info(self, infos):
        iocs = []
        url = infos['reference']
        title = infos['title']
        res = req.get(url)
        if not res:
            return

        soup = BeautifulSoup(res, 'html5lib')
        lis = soup.select('li')
        for li in lis:
            text = li.getText()
            result_list = text.replace("：", " ").replace(
                ": ", " ").replace("，", " ").split(" ")
            results = format_list(result_list)
            if results != None:
                for ioc in results:
                    ioc['reference'] = url
                    ioc['title'] = title
                    ioc['website'] = "netlab360"
                    iocs.append(ioc)

                ioc_list = set_data_md5(iocs)
                insert(ioc_list)
