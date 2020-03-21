#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

import random

import requests
from bs4 import BeautifulSoup

from utils.common import rand_header
from utils.logger import get_logger


logger = get_logger(__file__)

headers = rand_header()


def get_proxy_jiangxianli():
    url = "http://ip.jiangxianli.com/"
    res_text = requests.get(url, headers=rand_header()).text
    html = BeautifulSoup(res_text, 'html5lib')
    tables = html.select_one(
        'body > div.row > div > div.box > div.box-body.table-responsive.no-padding > table > tbody')
    trs = tables.select('tr')
    proxys = []
    for tr in trs:
        proxy = {}
        proxy[tr.select('td')[4].getText()] = tr.select(
            'td')[1].getText() + ":" + tr.select('td')[2].getText()
        proxys.append(proxy)
    proxy = random.choice(proxys)
    return proxy


def get_proxy_goubanjia():
    url = "http://www.goubanjia.com"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
    }
    header['User-Agent'] = rand_header()['User-Agent']
    resp_text = requests.get(url, verify=False, headers=header).text
    html = BeautifulSoup(resp_text, 'html5lib')
    tables = html.select_one(
        "#services > div > div.row > div > div > div > table")
    trs = tables.select('tr')[1:]
    proxys = []
    for tr in trs:
        proxy = {}
        proxy[tr.select('td')[2].getText()] = tr.select('td')[0].getText()
        proxys.append(proxy)
    return random.choice(proxys)


def get_proxy_66ip():
    url = "http://www.66ip.cn/{}.html".format(random.randint(1, 1000))
    resp_text = requests.get(url, headers=rand_header()).text
    html = BeautifulSoup(resp_text, 'html5lib')
    tables = html.select_one('#main > div > div:nth-child(1) > table')
    trs = tables.select('tr')[1:]
    proxys = []
    for tr in trs:
        proxy = {}
        proxy['http'] = tr.select('td')[0].getText(
        ) + ":" + tr.select('td')[1].getText()
        proxys.append(proxy)
    return random.choice(proxys)


def get_proxy_iphai():
    url = "http://www.iphai.com"
    resp_text = requests.get(url, headers=rand_header()).text
    html = BeautifulSoup(resp_text, 'html5lib')
    tables = html.select_one(
        "body > div.container > div.table-responsive.module > table")
    trs = tables.select('tr')[1:]
    proxys = []
    for tr in trs:
        proxy = {}
        proxy[tr.select('td')[3].getText().strip()] = tr.select(
            'td')[0].getText().strip() + ":" + tr.select('td')[1].getText().strip()
        proxys.append(proxy)
    return random.choice(proxys)


def get_proxies():
    num = random.randint(0, 3)
    if num == 0:
        proxy = get_proxy_jiangxianli()
    elif num == 1:
        proxy = get_proxy_66ip()
    elif num == 2:
        proxy = get_proxy_iphai()
    else:
        proxy = get_proxy_goubanjia()
    return proxy


def get(url, data=None, headers=headers, cookies=None, proxies=None, verify=None, timeout=20, origin=False):
    if proxies:
        proxies = get_proxies()

    res = None
    for i in range(3):
        try:
            res = requests.get(url, data=data, headers=headers,
                               cookies=cookies, proxies=proxies,
                               verify=verify, timeout=timeout)
            logger.info('成功请求网站: {}'.format(url))
            break
        except Exception:
            logger.error("尝试获取链接[{}]失败，重试中...".format(url))

    if res != None:
        if not origin:
            return res.text
        return res
    else:
        return res


def post(url, data=None, json=None, headers=headers, cookies=None, proxies=None, verify=None, timeout=20, origin=False):
    if proxies:
        proxies = get_proxies()

    res = None
    for i in range(3):
        try:
            res = requests.post(url, data=data, headers=headers, json=json,
                                cookies=cookies, proxies=proxies,
                                verify=verify, timeout=timeout)
            logger.info('成功请求网站: {}'.format(url))
            break
        except Exception:
            logger.error("尝试获取链接[{}]失败，重试中...".format(url))

    if res != None:
        if not origin:
            return res.text
        return res
    else:
        return res
