#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

from core.crawler import CrawlerBase
from bs4 import BeautifulSoup
from utils import req
from utils.common import format_list
from utils.tomongo import insert
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_paloalto"
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        infos = []

        index = "https://unit42.paloaltonetworks.com/?pg=4"

        index_text = req.get(index)
        if not index_text:
            return

        index_soup = BeautifulSoup(index_text, 'html5lib').select('h3')
        for h3 in index_soup:
            a = h3.find('a')
            try:
                url = a['href']
                title = a.getText()
                info = {}
                info['reference'] = url
                info['title'] = title
                info ['website'] = "palpalto"
                infos.append(info)
            except:
                continue

        return infos
        

    def get_info(self, infos):
        results = []
        url = infos['reference']
        title = infos['title']
        index_text = req.get(url)
        if not index_text:
            return

        partten = "<br />(.*?)<br />"
        time_pattern = 'datetime="(.*?)T'
        texts = re.findall(partten, index_text, re.DOTALL)
        time = re.findall(time_pattern, index_text, re.S)
        infos = []
        for text in texts:
            info = text.strip().replace("[", "").replace("]", "")
            if " " not in info:
                infos.append(info)
        result_list = format_list(infos)
        for result in result_list:
            result['reference'] = url
            result['title'] = title
            result['time'] = time[0]
            results.append(result)

        ioc_list = set_data_md5(results)
        insert(ioc_list)
