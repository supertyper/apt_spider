#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from core.crawler import CrawlerBase
from bs4 import BeautifulSoup
from utils import req
from utils.common import format_list
from utils.tomongo import insert
from urllib.parse import urljoin
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_tencent"
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        infos = []
        for page_num in range(1, 2000):
            index_url = "https://s.tencent.com/research/report/list_1_{}.html".format(
                page_num)
            res = req.get(index_url, origin=True)
            status_code = res.status_code
            if status_code == 200:
                try:
                    index_soup = BeautifulSoup(res.text.encode(
                        'iso-8859-1').decode('utf-8'), 'html5lib')
                    new_lis = index_soup.select('h3')
                    for new_li in new_lis:
                        url = urljoin("https://s.tencent.com",
                                      new_li.find('a')['href'])
                        info = {}
                        info['reference'] = url
                        info['title'] = new_li.getText()
                        info['website'] = 'tencent'
                        infos.append(info)
                except:
                    continue
            else:
                break
        return infos

    def get_info(self, infos):
        url = infos['reference']
        title = infos['title']
        iocs = []
        res = req.get(url)
        if not res:
            return
        ioc_soup = BeautifulSoup(res.encode(
            'iso-8859-1').decode('utf-8'), 'html5lib').select('.MsoNormal')
        time = BeautifulSoup(res.encode('iso-8859-1').decode('utf-8'),
                             'html5lib').select_one('.time').getText().split(" ")[0]
        ioc_list = []
        for ioc_text in ioc_soup:
            ioc_list.append(ioc_text.getText().replace(
                "\n", "").replace("\t", ""))
        format_iocs = format_list(ioc_list)
        for ioc in format_iocs:
            ioc['reference'] = url
            ioc['title'] = title
            ioc['disclosuretime'] = time
            iocs.append(ioc)

        ioc_list = set_data_md5(iocs)
        insert(ioc_list)
