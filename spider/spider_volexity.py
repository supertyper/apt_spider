#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json

from bs4 import BeautifulSoup

from core.crawler import CrawlerBase
from utils.common import format_list
from utils.tomongo import insert
from utils import req
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_volexity"
    auth = "fariy"
    thread = 5

    def get_url_list(self):
        url_list = []
        page = 0
        while True:
            url = "https://www.volexity.com/wp-admin/admin-ajax.php?id=&post_id=0&slug=home&canonical_url=https%3A%2F%2Fwww.volexity.com%2Fblog%2F&posts_per_page=1&page={}&offset=0&post_type=post&repeater=default&seo_start_page=1&preloaded=false&preloaded_amount=0&order=DESC&orderby=date&action=alm_get_posts&query_type=standard".format(
                str(page))
            resp_dict = json.loads(req.get(url))
            if not resp_dict:
                continue
            if resp_dict['html']:
                soup = BeautifulSoup(resp_dict['html'], 'html5lib')
                url = soup.find_all('a', 'box-cta')[0].get('href')
                title = soup.find_all('h2', 'post-title')[0].getText()
                url_list.append((url, title))
            else:
                break
            page += 1
        return url_list

    def get_info(self, target):
        result = []
        url = target[0]
        resp_text = req.get(url)
        if not resp_text:
            return

        time = re.findall(r"(\d{4}/\d{2}/\d{2})", url)[0].replace("/", "-")
        soup = BeautifulSoup(resp_text, 'html5lib')
        content = soup.select_one('body > main > div > section > article > div').getText(
        ).replace('\t', '\n').replace(' ', '\n')
        result_list = format_list(content.split('\n'))
        for ioc in result_list:
            ioc['reference'] = url
            ioc['name'] = target[1]
            ioc['disclosuretime'] = time
            result.append(ioc)

        ioc_list = set_data_md5(result)
        insert(ioc_list)
