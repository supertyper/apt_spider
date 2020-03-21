#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

from pymongo.errors import BulkWriteError

from utils.logger import get_logger
from utils.database import MongoDB
from config.template import config


logger = get_logger(__file__)


def insert(ioc_list):
    # ioc对应的collection
    data_to_col = {
        'ip': 'ip',
        'filename': 'malware',
        'domain': 'domain',
        'email': 'email',
        'md5': 'malware',
        'url': 'url',
        'sha1': 'malware',
        'sha256': 'malware'}
    malwarekey = [
        'name',
        'filename',
        'md5',
        'sha1',
        'sha256',
        'filetype',
        'aptorganization',
        'disclosuretime',
        'reference']
    domainkey = [
        'aptorganization',
        'domain',
        'malbehavior',
        'disclosuretime',
        'reference']
    emailkey = [
        'aptorganization',
        'email',
        'malbehavior',
        'disclosuretime',
        'reference']
    ipkey = [
        'aptorganization',
        'ip',
        'malbehavior',
        'disclosuretime',
        'reference']
    urlkey = [
        'aptorganization',
        'url',
        'malbehavior',
        'disclosuretime',
        'reference']

    # 确定数据是写到哪个collection中去
    col = None
    ioc_template = ioc_list[0]

    # for key_type in ioc_template.keys():
    #     if key_type in data_to_col.keys():
    #         col = data_to_col[key_type]
    #         break
    # if not col:
    #     logger.error("数据结构出现问题，找不到对应集合，请检查！")
    #     return

    all_collection_data_list = {
        "ip": [],
        "malware": [],
        "domain": [],
        "email": [],
        "url": []
    }

    for ioc in ioc_list:
        col = None
        for key_type in ioc_template.keys():
            if key_type in data_to_col.keys():
                col = data_to_col[key_type]
                break
        if not col:
            logger.error("数据结构出现问题，找不到对应集合，请检查！")
            continue

        for key in locals()[col + 'key']:
            if key in ioc.keys():
                continue
            ioc.update({key: ""})

        all_collection_data_list[col].append(ioc)

    # for ioc in ioc_list:
    #     for key in locals()[col + 'key']:
    #         if key in ioc.keys():
    #             continue
    #         ioc.update({key: ""})
    # 连接mongodb，写入数据
    db = MongoDB(config["mongo"]["db"])
    for col, iocs in all_collection_data_list.items():
        if len(iocs):
            try:
                db.insert_many(col, iocs)
            except BulkWriteError:
                pass
