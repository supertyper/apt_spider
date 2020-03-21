#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from bs4 import BeautifulSoup

from core.crawler import CrawlerBase
from utils.common import format_list
from utils.tomongo import insert
from utils import req
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_qianxin"
    auth = "fairy"
    thread = 5

    def get_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        resp = req.get(url, headers=headers)
        if not resp:
            return

        html = resp.decode()
        if 'Redirecting' in html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        tmp = soup.find_all('script')
        result = re.findall('''permlink:"(.*?)"}''', tmp[0].get_text())
        return result

    def get_url_list(self):
        qianxin_list = []
        url_index = 'https://ti.qianxin.com/blog/'
        result = self.get_url(url_index)
        if result:
            for i in result:
                if i:
                    qianxin_list.append(i)
                else:
                    return qianxin_list
        else:
            return qianxin_list

        page = 2
        while 1:
            url_other = 'https://ti.qianxin.com/blog/pages/{}/'.format(
                str(page))
            result = self.get_url(url_other)
            if result:
                for i in result:
                    if i:
                        qianxin_list.append(i)
                    else:
                        return qianxin_list
                page += 1
            else:
                return qianxin_list
        return qianxin_list

    def get_info(self, url):
        result_json = []
        if '.pdf' in url:
            return
        resp = req.get(url)
        if not resp:
            return

        html = resp.decode()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all(
            'div', 'title-detail')[0].get_text().replace('\n', '').replace(' ', '')
        time = re.findall(r"(\d{4}-\d{2}-\d{2})", html)
        tmp_ioc = soup.find_all('div', 'main-body')[0].get_text()
        if 'IOC' not in tmp_ioc:
            return
        if 'IOC' in tmp_ioc and '参考' in tmp_ioc:
            ioc_list = tmp_ioc[tmp_ioc.find('IOC'):tmp_ioc.rfind('参考')]
        elif 'IOC' in tmp_ioc and 'References' in tmp_ioc:
            ioc_list = tmp_ioc[tmp_ioc.find('IOC'):tmp_ioc.rfind('References')]
        elif 'IOC' in tmp_ioc and '[1]' in tmp_ioc:
            ioc_list = tmp_ioc[tmp_ioc.find('IOC'):tmp_ioc.rfind('[1]')]
        else:
            ioc_list = tmp_ioc
        ioc_list = ioc_list.split('\n')

        result_list = format_list(ioc_list)
        for ioc in result_list:
            ioc['reference'] = url
            ioc['name'] = title
            ioc['disclosuretime'] = time[0]
            result_json.append(ioc)

        ioc_list = set_data_md5(result_list)
        insert(ioc_list)
