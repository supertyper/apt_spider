#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao


from core.crawler import CrawlerBase


class SpiderBase(CrawlerBase):
    desc = "red_drip7"
    auth = "red_drip7"
    thread = 1


    def get_url_list(self):
        print("get_url_list")
        return [True]

    def get_info(self, apt_info):
        print("get_info")

