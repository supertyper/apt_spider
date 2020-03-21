# coding: utf-8
from core.crawler import CrawlerBase
from utils.common import rand_header
from bs4 import BeautifulSoup
from utils import req
from utils.tomongo import insert
from utils.common import set_data_md5

class SpiderBase(CrawlerBase):
    desc = "spider_threatbook"
    auth = "fariy"
    thread = 10

    def get_url_list(self):
        url_list = []
        url = "https://x.threatbook.cn/nodev4/getAllList?currentPage=0"
        self.header = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        self.header['user-agent'] = rand_header()["User-Agent"]
        html = req.get(url, headers=self.header)
        if not html:
            return []

        soup = BeautifulSoup(html, "html5lib")
        new_end = {}
        new_end["website"] = "threatbook"
        new_end["reference"] = soup.select_one(
            "body > div:nth-child(2) > div > div.title > a").get('href')
        new_end["title"] = soup.select_one(
            "body > div:nth-child(2) > div > div.title > a").getText()
        for i in range(1, int(new_end['reference'].split('=')[-1])):
            url_list.append(
                "https://x.threatbook.cn/nodev4/vb4/article?threatInfoID={}".format(str(i)))
        return url_list

    def get_info(self, url):
        result_ioc = []
        self.header['user-agent'] = rand_header()["User-Agent"]
        html = req.get(url, headers=self.header)
        if not html:
            return

        soup = BeautifulSoup(html, "html5lib")
        # title = soup.select_one(
        #     "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.brief > div.title.J-title").getText().strip()
        time = soup.find_all('span', 'time')[0].getText().strip()
        try:
            domains = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.domain")
            for tr in domains.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['domain'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    result_ioc.append(ioc)
        except:
            pass
        try:
            ips = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.ip")
            for tr in ips.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['ip'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    result_ioc.append(ioc)
        except:
            pass

        try:
            urls = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.url")
            for tr in urls.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['url'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    result_ioc.append(ioc)
        except:
            pass

        try:
            hashs = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.hash")
            for tr in hashs.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    try:
                        ioc['filename'] = tmp[0].find_all(
                            'span', 'file-name cutWhenTooLong')[0].getText()
                    except:
                        pass
                    hash = tmp[0].find_all(
                        'span', 'file-hash')[0].getText().strip()
                    if len(hash) == 32:
                        ioc['md5'] = hash
                    elif len(hash) == 40:
                        ioc['sha1'] == hash
                    else:
                        ioc['sha256'] = hash
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    result_ioc.append(ioc)
        except:
            pass

        try:
            emails = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.email")
            for tr in emails.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['email'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    result_ioc.append(ioc)
        except:
            pass

        ioc_list = set_data_md5(result_ioc)
        insert(ioc_list)
