#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json

from bs4 import BeautifulSoup

from utils import req
from core.crawler import CrawlerBase
from utils.tomongo import insert
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = 'spider_symantec'
    thread = 10

    def get_url_list(self):
        url_list = []
        pagenum = 0
        while pagenum < 5:
            url_index = 'https://content.connect.symantec.com/api/v1/blogs/search?_format=json&blog=221&sort=&sortDirection=&rows=5&page={}'.format(
                pagenum)
            resp = req.get(url_index, verify=False)
            if not resp:
                continue
            newurl = list(
                map(lambda x: x['urlAlias'][11:], json.loads(resp)['results']))
            if newurl:
                pagenum += 1
                url_list.extend(newurl)
            else:
                break

        return url_list

    def get_info(self, url):
        articleurl = 'https://www.symantec.com/blogs/threat-intelligence/' + url
        resp = req.get(articleurl, verify=False)
        if not resp:
            return

        html = resp.decode()
        soup = BeautifulSoup(html, 'html.parser')
        iocinfos = []
        domains = list(map(lambda x: x.get_text().strip(), soup.find_all(
            attrs={'data-label': re.compile('.*Domains'), 'role': 'cell'})))
        hashes = list(map(lambda x: x.get_text().strip(), soup.find_all(
            attrs={'data-label': re.compile('.*Hashes'), 'role': 'cell'})))
        url = list(map(lambda x: x.get_text().strip(), soup.find_all(
            attrs={'data-label': re.compile('.*URLs'), 'role': 'cell'})))
        name = soup.find('title').get_text().split('|')[0]
        for item in domains:
            iocdata = dict()
            iocdata['name'] = name
            iocdata['reference'] = articleurl
            iocdata['domain'] = item
            iocinfos.append(iocdata)
        for item in url:
            iocdata = dict()
            iocdata['name'] = name
            iocdata['reference'] = articleurl
            iocdata['url'] = item
            iocinfos.append(iocdata)
        for item in hashes:
            iocdata = dict()
            iocdata['name'] = name
            iocdata['reference'] = articleurl
            if len(item) == 32:
                iocdata['md5'] = item
            elif len(item) == 40:
                iocdata['sha1'] = item
            elif len(item) == 64:
                iocdata['sha256'] = item
            else:
                continue
            iocinfos.append(iocdata)

        ioc_list = set_data_md5(iocinfos)
        insert(ioc_list)
