#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

from core.crawler import CrawlerBase
from utils.common import random_sleep
from bs4 import BeautifulSoup
from utils import req
from utils.common import format_list
from utils.tomongo import insert
from utils.common import set_data_md5
from utils.logger import get_logger


logger = get_logger(__file__)


class SpiderBase(CrawlerBase):
    desc = "spider_antiy"
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        infos = []
        max_page = []
        max_page.append("")
        base_url = "https://www.antiy.com/response.html"
        pattern_pages = r'<a href="https://www.antiy.com/response\d.html" target="_blank">(.*?)</a></li>'
        index_text = req.get(base_url)
        if not index_text:
            return []

        for i in re.findall(pattern_pages, index_text, re.S):
            max_page.append(i)
        for i in max_page:
            url = "https://www.antiy.com/response{}.html".format(i)
            random_sleep()
            res = req.get(url)
            if not res:
                continue

            req_text = res.encode(
                'iso-8859-1').decode('utf-8')
            html = BeautifulSoup(req_text, 'html5lib')
            contents = html.select('#content > div')
            for content in contents:
                for i in content.select('.post-title'):
                    info = {}
                    info['url'] = i.find('a')['href']
                    info['title'] = i.find('a').getText().strip().replace(
                        "\n", "").replace("  ", "")
                    infos.append(info)
        return infos

    def get_info(self, info):
        if "http" in info['url']:
            url_id = info['url']
        else:
            url_id = "https://www.antiy.com/{}".format(info['url'])
        res = req.get(url_id)
        if not res:
            return

        req_text = res.encode(
            'iso-8859-1').decode('utf-8')
        pattern_time = r"(\d{4})年(\d+)月(\d+)"
        time = re.findall(pattern_time, req_text, re.S)
        try:
            html = BeautifulSoup(req_text, 'html5lib')
            trs = html.select('.MsoNormal')
            result_json = []
            result_list = []
            for tr in trs:
                text = tr.getText()
                result_list.append(text)
            infos = format_list(result_list)
            for ioc in infos:
                ioc['reference'] = url_id
                ioc['name'] = info['title']
                ioc['disclosuretime'] = '-'.join(time[0])[0:]
                result_json.append(ioc)

            ioc_info = set_data_md5(result_json)
            insert(ioc_info)

        except Exception as e:
            logger.error(e)
