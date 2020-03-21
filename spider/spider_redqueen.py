#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json
from urllib.parse import quote

from core.crawler import CrawlerBase
from utils.common import random_sleep
from utils.tomongo import insert
from utils import req
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = '''spider_redqueen'''
    auth = "co0ontty"
    thread = 5

    def get_url_list(self):
        infos = []
        index_html = "https://redqueen.tj-un.com/Json/intelHomeSafetyIntelList.json"
        res = req.get(index_html, origin=True)
        if not res:
            return []

        cookies = res.cookies
        cookie = cookies.get_dict()['JSESSIONID']
        header = {
            "Connection": "keep-alive",
            "Content-Length": "59",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://redqueen.tj-un.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://redqueen.tj-un.com/IntelHome.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "sid=82dec426-4e54-4c41-9c18-c90230230711; JSESSIONID={}".format(cookie)
        }
        data = '{"page":1,"page_count":1000000}'
        data = "query={}".format(quote(data))
        urls_json = req.post(
            index_html, data=data, headers=header)
        urls_json = json.loads(urls_json)

        for page_id in urls_json['intgs']:
            info = {}
            info['url'] = page_id['id']
            info['title'] = page_id['title']
            infos.append(info)

        return infos

    def get_info(self, infos):
        json_url = "https://redqueen.tj-un.com/Json/intelDetailsIocsGeneral.json"
        result_json = []
        pages_id = infos['url']
        pages_title = infos['title']
        url = "https://redqueen.tj-un.com/IntelDetails.html?id={}".format(
            pages_id)
        query = '{"id":"'+pages_id + \
            '","page":1,"page_count":1000000,"key_word":""}'
        post_data = 'query={}'.format(quote(query))
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "128",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "redqueen.tj-un.com",
            "Origin": "https://redqueen.tj-un.com",
            "Referer": "https://redqueen.tj-un.com/IntelDetails.html?id={}".format(pages_id),
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = req.get(url)
        if not response:
            return
        try:
            disclosuretime = re.search(
                r'\d{4}\-\d{2}\-\d{1,2}', pages_title, flags=0).group(0)
            name = pages_title.replace(disclosuretime, "")
        except:
            pass
        if "指示器" in response:
            random_sleep()
            ioc_json = req.post(
                json_url, data=post_data, cookies=response.cookies, headers=header, origin=True).json()
            for ioc in ioc_json['ioc']:
                content_type = ioc['type_id'].lower()
                if "域名" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "domain"
                    iocs[content_type] = ioc['content']
                elif "ip" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "ip"
                    iocs[content_type] = ioc['content']
                elif "md5" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "md5"
                    iocs[content_type] = ioc['content']
                elif "sha1" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "sha1"
                    iocs[content_type] = ioc['content']
                elif "sha256" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "sha256"
                    iocs[content_type] = ioc['content']
                elif "mail" in content_type:
                    iocs = {}
                    iocs['name'] = name
                    iocs['reference'] = url
                    iocs['disclosuretime'] = disclosuretime
                    content_type = "email"
                    iocs[content_type] = ioc['content']
                result_json.append(iocs)

        ioc_list = set_data_md5(result_json)
        insert(ioc_list)


