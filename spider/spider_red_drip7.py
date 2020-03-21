#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

import os
import re
from copy import deepcopy

from core.crawler import CrawlerBase
from utils.tomongo import insert
from utils.common import set_data_md5
from utils.logger import get_logger


logger = get_logger(__file__)


class SpiderBase(CrawlerBase):
    desc = "spider_red_drip7"
    auth = "daMao"
    thread = 1

    def get_url_list(self):
        os.system("git clone https://github.com/RedDrip7/APT_Digital_Weapon.git")
        return [True]

    def get_info(self, apt_info):
        path_dir = "./APT_Digital_Weapon"
        result_list = []
        for apt_dir in os.listdir(path_dir):
            apt_dir_path = os.path.join(path_dir, apt_dir)
            if not os.path.isdir(apt_dir_path):
                continue

            apt_dict = dict()
            # 1)获取apt组织&reference相关信息
            apt_org_file = os.path.join(apt_dir_path, "README.md")
            if os.path.isdir(apt_org_file) or ".git" in apt_org_file:
                continue
            with open(apt_org_file, "r") as f:
                content = f.read() + "\n"
            aptorganization = content.split("\n")[1]
            try:
                reference = re.search(r"(http.*?)\n", content).group(1)
            except:
                reference = ""
            apt_dict["aptorganization"] = aptorganization
            apt_dict["reference"] = reference

            # 2)获取apt信息
            for apt_file in os.listdir(apt_dir_path):
                if apt_file == "README.md":
                    continue
                apt_file_path = os.path.join(apt_dir_path, apt_file)
                if not apt_file_path.endswith("md"):
                    continue
                else:
                    with open(apt_file_path, "r") as f:
                        content = f.read() + "\n"
                    hash_info_list = content.split("\n")
                    for index, hash_info in enumerate(hash_info_list):
                        apt_dict_copy = deepcopy(apt_dict)
                        if index in [0, 1]:
                            continue

                        if not hash_info:
                            continue

                        try:
                            hash_value = hash_info.split("|")[1]
                        except Exception:
                            continue
                        if not hash_value:
                            continue

                        hash_value = hash_value[1:33]
                        filetype = hash_info.split("|")[2]
                        disclosuretime = hash_info.split("|")[4].split(" ")[0]
                        filename = hash_info.split("|")[5]
                        apt_dict_copy["md5"] = hash_value
                        apt_dict_copy["filetype"] = filetype
                        apt_dict_copy["disclosuretime"] = disclosuretime
                        apt_dict_copy["filename"] = filename
                        result_list.append(apt_dict_copy)

        try:
            ioc_list = set_data_md5(result_list)
            insert(ioc_list)
        except Exception as e:
            logger.error(e)
        finally:
            os.system("rm -rf ./APT_Digital_Weapon")
            pass