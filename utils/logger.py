#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from config.template import LogPath

'''
    最细化日志文件，对于每一个爬虫生成一份日志文件，根据爬虫文件名定义logger名称
'''


def get_logger(file, console_confirm=True):
    logger_name = str(datetime.now()).split(" ")[0]
    file_name = file.split('/')[-1]
    log_path = LogPath
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_fn = "{0}/{1}.log".format(log_path, logger_name)
    # getLogger 为单例模式
    ndr_logger = logging.getLogger(file_name)
    ndr_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("""[%(asctime)s]  [File][%(name)s][line:%(lineno)d]  %(levelname)s:  %(message)s""")
    # handler 存在判定，防止添加多个handler，造成日志重复
    if not ndr_logger.handlers:
        ndr_handler = TimedRotatingFileHandler(log_fn, 'midnight', backupCount=60)
        ndr_handler.setFormatter(formatter)
        ndr_logger.addHandler(ndr_handler)
        # 是否输出到控制台
        if console_confirm:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            ndr_logger.addHandler(console_handler)

    return ndr_logger

if __name__ == '__main__':
    pass
