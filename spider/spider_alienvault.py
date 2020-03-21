# coding: utf-8

import json

from utils import req
from utils.tomongo import insert
from core.crawler import CrawlerBase
from utils.common import set_data_md5


class SpiderBase(CrawlerBase):
    desc = "spider_alienvault"
    auth = "fariy"
    thread = 5

    def get_url_list(self):
        result = []

        for i in range(1, 51):
            url = "https://otx.alienvault.com/otxapi/pulses/?sort=-created&filter=pulses&limit=100&page={}".format(
                str(i))
            res = req.get(url)
            if not res:
                continue

            resp_json = req.get(url)
            resp_dict = json.loads(resp_json)
            for i in resp_dict['results']:
                result.append((i['name'], i['id'], i['created'][0:10]))

        if result:
            new_end = {}
            new_end['website'] = "alienvault"
            new_end['reference'] = result[0][1]
            new_end['title'] = result[0][0]
        return result

    def get_info(self, target):
        iocs = []
        url = "https://otx.alienvault.com/otxapi/pulses/{}/indicators/?limit=1000&page=1&sort=-created&hasAnalysis=true".format(
            target[1])
        res = req.get(url)
        if not res:
            return

        resp_json = req.get(url)
        resp_dict = json.loads(resp_json)
        for i in resp_dict['results']:
            ioc = {}
            ioc['name'] = target[0]
            ioc['reference'] = url
            ioc['disclosuretime'] = target[2]
            if i['slug'] == "email":
                ioc['email'] = i['indicator']
            elif i['slug'] == "hostname":
                ioc['domain'] = i['indicator']
            elif i['slug'] == "hostname" or i['slug'] == "domain":
                ioc['doman'] = i['indicator']
            elif i['slug'] == 'file':
                if i['type'] == 'FileHash-SHA256':
                    ioc['sha256'] = i['indicator']
                elif i['type'] == 'FileHash-MD5':
                    ioc['md5'] = i['indicator']
                else:
                    ioc['sha1'] = i['indicator']
            elif i['slug'] == 'url':
                ioc['url'] = i['indicator']
            elif i['slug'] == 'ip':
                ioc['ip'] = i['indicator']

            iocs.append(ioc)

        ioc_info = set_data_md5(iocs)

        insert(ioc_info)
