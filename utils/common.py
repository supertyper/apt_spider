from config.template import path, config
import os
import random
import re
import hashlib
import time
from random import random
import linecache
import tldextract
from urllib.parse import urlparse
from config.template import az
from functools import reduce


# 对抓取到的任一条数据生成一个唯一MD5值，防止数据库数据重复
def set_data_md5(data_list):

    for data in data_list:
        data_values = data.values()
        all_str_add = reduce(lambda x, y: str(x) + str(y), data_values)
        md5_value = hashlib.md5(all_str_add.encode("utf-8")).hexdigest()
        data["_id"] = md5_value

    return data_list


def set_path(root_path):

    path['root_path'] = root_path
    path['plugins_path'] = os.path.join(root_path, 'spider')
    path['log_path'] = os.path.join(root_path, 'logs')
    path['config_path'] = os.path.join(root_path, 'config/config.cfg')
    path['crawler_path'] = os.path.join(root_path, 'config/crawler.json')
    path['lib_path'] = os.path.join(root_path, 'utils')
    path['core_path'] = os.path.join(root_path, 'core')
    path['user_agent_path'] = os.path.join(root_path, 'data/user-agents.txt')


def rand_header():
    f = open(path['user_agent_path'], 'r')
    rand = random.randint(0, len(f.readlines()))
    f.close()
    header = {
        'User-Agent': linecache.getline(path['user_agent_path'], rand).strip()}
    return header


def get_spider():
    target_list = list()
    apt_spider = config['crawler']
    for i in apt_spider:
        spider_module = apt_spider[i]['module']
        target_list.append(spider_module)
    az.plugins_num = len(target_list)
    return target_list


def format_list(list_name):
    pattern_url = r"^([-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])$"
    pattern_ip = r"(((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))"
    pattern_md5 = "^[a-zA-z0-9]{32}$"
    pattern_sha1 = "^[a-zA-z0-9]{40}$"
    pattern_sha256 = "^[a-zA-z0-9]{64}$"
    pattern_Domain = r'(^[A-za-z0-9]+\.[A-za-z0-9]+\.[A-za-z0-9]+|^[A-za-z0-9]+\.[A-za-z0-9]+)'
    pattern_email = r"^(\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14})"
    result_json = []
    for text in list_name:
        urls = re.findall(pattern_url, text, re.S)
        ips = re.findall(pattern_ip, text, re.S)
        md5s = re.findall(pattern_md5, text, re.S)
        sha1s = re.findall(pattern_sha1, text, re.S)
        sha256s = re.findall(pattern_sha256, text, re.S)
        Domains = re.findall(pattern_Domain, text, re.DOTALL)
        emails = re.findall(pattern_email, text, re.S)
        for url in urls:
            if "/" in url and len(url) > 8 and urlparse(url).netloc:
                iocs = {}
                iocs['url'] = url
                result_json.append(iocs)
        for ip in ips:
            iocs = {}
            iocs['ip'] = ip[0]
            result_json.append(iocs)
        for md5 in md5s:
            # print(md5)
            iocs = {}
            iocs['md5'] = md5
            result_json.append(iocs)
        for sha1 in sha1s:
            iocs = {}
            iocs['sha1'] = sha1
            result_json.append(iocs)
        for sha256 in sha256s:
            iocs = {}
            iocs['sha256'] = sha256
            result_json.append(iocs)
        for Domain in Domains:
            # if re.findall(r'[a-zA-Z]',Domain):
            if tldextract.extract(Domain).suffix:
                iocs = {}
                iocs['domain'] = Domain
                result_json.append(iocs)
        for email in emails:
            iocs = {}
            iocs['email'] = email[0]
            result_json.append(iocs)

    return result_json


def random_sleep():
    random_time = random()
    time.sleep(random_time)
