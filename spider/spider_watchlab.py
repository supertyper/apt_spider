#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

import json
from copy import deepcopy

from core.crawler import CrawlerBase
from utils.tomongo import insert
from utils.req import get
from utils.req import post
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_watchlab"
    auth = "daMao"
    thread = 10
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "Host": "feed.watcherlab.com",
        "Origin": "https://feed.watcherlab.com",
        "Referer": "https://feed.watcherlab.com/index/apt",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    }

    def get_url_list(self):
        base_url = "https://feed.watcherlab.com/threatlib/apt/home/aptnotes"
        watchlab_list = list()

        for year in ["2006", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]:
        # for year in ["2019", "2020"]:
            data = {
                "type": "year",
                "data": year
            }

            res = post(base_url, json=data, headers=self.headers, verify=False)
            if not res:
                continue

            content = json.loads(res)
            for data in content["data"]:
                if not data["iocsUuid"]:
                    continue

                info_dict = {}
                info_dict["disclosuretime"] = data["time"]
                info_dict["link_id"] = data["iocsUuid"]
                info_dict["groups"] = data["groups"]
                info_dict["title"] = data["titleCn"]
                info_dict["comment"] = data["commentCn"]
                info_dict["attack_method"] = data["operandi"]
                watchlab_list.append(info_dict)
        # print(len(watchlab_list))
        return watchlab_list

    def get_info(self, apt_info):
        group_url = "https://feed.watcherlab.com/threatlib/apt/home/many/groups"
        pre_ioc_url = "https://feed.watcherlab.com/threatlib/feed/anon/manyquery/"
        group_id = apt_info["groups"]
        if not group_id:
            apt_dict = {
                "aptorganization": "",
                "disclosuretime": apt_info["disclosuretime"],
                "reference": apt_info["link_id"],
                "title": apt_info["title"],
                "comment": apt_info["comment"],
                "method": apt_info["attack_method"]
            }
        else:
            res = post(group_url, json=group_id, headers=self.headers, verify=False)
            if not res:
                return

            content = json.loads(res)
            # print(content)
            aptorganization = content["data"][0]["alias"][0]["alias"]
            apt_dict = {
                "aptorganization": aptorganization,
                "disclosuretime": apt_info["disclosuretime"],
                "reference": apt_info["link_id"],
                "title": apt_info["title"],
                "comment": apt_info["comment"],
                "method": apt_info["attack_method"]
            }

        # 抓取apt情报信息
        link_id = apt_dict["reference"]
        url = pre_ioc_url + link_id
        res = get(url, headers=self.headers, verify=False)
        if not res:
            return

        content = json.loads(res)
        iocs = content["data"]["iocs"]

        result_list = list()
        for key, ioc in iocs.items():
            if not ioc:
                continue
            for data in ioc:
                reslut = deepcopy(apt_dict)
                target = data["basicInfo"]["data"]
                reslut[key] = target
                reslut["reference"] = pre_ioc_url + reslut["reference"]
                result_list.append(reslut)

        ioc_list = set_data_md5(result_list)
        insert(ioc_list)


