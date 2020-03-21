#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

import os
from importlib import import_module

from utils.common import set_path
from utils.set_config import set_config
from utils.common import get_spider
from utils.thread import start_thread
from utils.logger import get_logger


class AptSpider(object):

    def __init__(self):
        self.logger = get_logger("main")
        self.spider_class = list()
        self.real_path = os.path.dirname(os.path.realpath(__file__))
        set_path(self.real_path)

    def init(self):
        set_config()
        # 获取需要运行的爬虫名称
        spider_models = get_spider()
        spider_file_list = os.listdir("spider")
        spider_list = filter(lambda x: x.startswith("spider") and x in spider_models, spider_file_list)
        spider_import = list(map(lambda x: ".".join(["spider", x.split(".")[0]]), spider_list))

        if not spider_import:
            self.logger.warning("未加载到任何爬虫程序，请检查爬虫配置文件！")
            exit(0)

        # 加载爬虫对象
        for spider in spider_import:
            spider_class = import_module(spider)
            self.spider_class.append(spider_class.SpiderBase())

    # 开始执行apt情报抓取工作
    def start(self):
        while self.spider_class:
            spider = self.spider_class.pop(0)
            start_thread(spider.start())

    # 入口函数
    def main(self):
        self.init()
        self.start()


if __name__ == "__main__":
    spider = AptSpider()
    spider.main()


    # real_path = os.path.dirname(os.path.realpath(__file__))
    # set_path(real_path)
    # set_config()
    # from spider.spider_red_drip7 import SpiderBase
    # a = SpiderBase()
    # a.get_url_list()
    # a.get_info(1)