from utils import req
import json
from filter.all_apt import all_apt


class Filter():
    def __init__(self, check_dict):
        self.check_ip_url = "https://www.venuseye.com.cn/ve/ip/ioc"
        self.check_mail_url = "https://www.venuseye.com.cn/ve/email/ioc"
        self.check_domain_url = "https://www.venuseye.com.cn/ve/domain/ioc"
        self.check_hash_url = "https://www.venuseye.com.cn/ve/sample/hash/ioc"
        self.check_md5_url = "https://www.venuseye.com.cn/ve/sample/md5"
        self.check_sha1_url = "https://www.venuseye.com.cn/ve/sample/sha1"
        self.check_sha256_url = "https://www.venuseye.com.cn/ve/sample/sha256"
        self.check_dict = check_dict
        self.id = None  # hash补充数据时使用

    def check_ip(self, ip):
        categories_list = []
        organizations_list = []
        data = {"target": ip}
        resp = req.post(self.check_ip_url, data=data)
        result_dict = json.loads(resp.text)
        if result_dict["status_code"] == 200:
            self.check_dict["verify"].append("venuseye")
            for ioc in result_dict["data"]["ioc"]:
                categories_list += ioc["categories"]
                if "organizations" in ioc:
                    organizations_list += ioc["organizations"]
        categories_list = [x for x in set(categories_list)]
        return categories_list, organizations_list

    def check_mail(self, mail):
        categories_list = []
        organizations_list = []
        data = {"target": mail}
        resp = req.post(self.check_mail_url, data=data)
        result_dict = json.loads(resp.text)
        if result_dict["status_code"] == 200:
            self.check_dict["verify"].append("venuseye")
            for ioc in result_dict["data"]["ioc"]:
                categories_list += ioc["categories"]
                if "organizations" in ioc:
                    organizations_list += ioc["organizations"]
        categories_list = [x for x in set(categories_list)]
        return categories_list, organizations_list

    def check_domain(self, domain):
        categories_list = []
        organizations_list = []
        data = {"target": domain}
        resp = req.post(self.check_domain_url, data=data)
        result_dict = json.loads(resp.text)
        if result_dict["status_code"] == 200:
            self.check_dict["verify"].append("venuseye")
            for ioc in result_dict["data"]["ioc"]:
                categories_list += ioc["categories"]
                if "organizations" in ioc:
                    organizations_list += ioc["organizations"]
        categories_list = [x for x in set(categories_list)]
        return categories_list, organizations_list

    def check_hash(self):
        categories_list = []
        organizations_list = []
        data = {"target": self.id}
        resp = req.post(self.check_hash_url, data=data)
        result_dict = json.loads(resp.text)
        if result_dict["status_code"] == 200:
            self.check_dict["verify"].append("venuseye")
            for ioc in result_dict["data"]["ioc"]:
                categories_list += ioc["categories"]
                if "organizations" in ioc:
                    organizations_list += ioc["organizations"]
        categories_list = [x for x in set(categories_list)]
        return categories_list, organizations_list

    def check_md5(self, md5):
        data = {"target": md5}
        resp = req.post(self.check_md5_url, data=data)
        md5_result = json.loads(resp.text)
        if md5_result["status_code"] == 200:
            self.id = md5_result["data"]["_id"]
            for i in ["sha1", "sha256", "file_name", "file_type", "file_size", "file_names"]:
                if self.check_dict[i]:
                    pass
                else:
                    self.check_dict[i] = md5_result["data"][i]

    def check_sha1(self, sha1):
        data = {"target": sha1}
        resp = req.post(self.check_sha1_url, data=data)
        md5_result = json.loads(resp.text)
        if md5_result["status_code"] == 200:
            self.id = md5_result["data"]["_id"]
            for i in ["md5", "sha256", "file_name", "file_type", "file_size", "file_names"]:
                if self.check_dict[i]:
                    pass
                else:
                    self.check_dict[i] = md5_result["data"][i]

    def check_sha256(self, sha256):
        data = {"target": sha256}
        resp = req.post(self.check_sha256_url, data=data)
        md5_result = json.loads(resp.text)
        if md5_result["status_code"] == 200:
            self.id = md5_result["data"]["_id"]
            for i in ["sha1", "md5", "file_name", "file_type", "file_size", "file_names"]:
                if self.check_dict[i]:
                    pass
                else:
                    self.check_dict[i] = md5_result["data"][i]

    def verify_apt_organization(self, apt_list):
        apt_organization = []
        for apt in apt_list:
            if apt in all_apt:
                apt_organization.append(apt)
            else:
                for organization in all_apt:
                    if apt in all_apt[organization]:
                        apt_organization.append(organization)
        apt_organization = [x for x in set(apt_organization)]
        return apt_organization

    def check_ioc(self):
        result_categories, result_organizations = [],[]
        if "ip" in self.check_dict:
            result_categories, result_organizations = self.check_ip(
                self.check_dict["ip"])
        if "email" in self.check_dict:
            result_categories, result_organizations = self.check_mail(
                self.check_dict["email"])
        if "domain" in self.check_dict:
            result_categories, result_organizations = self.check_domain(
                self.check_dict["domain"])
        if "url" in self.check_dict:
            result_categories, result_organizations = self.check_domain(
                self.check_dict["url"])
        if "file_name" in self.check_dict:
            if self.check_dict["md5"]:
                self.check_md5(self.check_dict["md5"])
            elif self.check_dict["sha1"]:
                self.check_sha1(self.check_dict["sha1"])
            else:
                self.check_sha256(self.check_dict["sha256"])
            if self.id:
                result_categories, result_organizations = self.check_hash()

        self.check_dict["apt_organization"] = self.verify_apt_organization(
            self.check_dict["apt_organization"] + result_organizations)

        self.check_dict["category"] = [x for x in set(
            self.check_dict["category"] + result_categories)]
        return self.check_dict