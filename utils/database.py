#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao

from pymongo import MongoClient

from utils.set_config import config
from utils.logger import get_logger


logger = get_logger(__file__)


class MongoDB(object):
    '''一个数据集合只创建一个数据库连接，单例'''
    __instance = list()
    __first_init = list()
    __cls_pool = dict()
    __database_pool = dict()

    def __new__(cls, args):
        if args not in MongoDB.__instance:
            init_cls = object.__new__(cls)
            MongoDB.__instance.append(args)
            MongoDB.__cls_pool[args] = init_cls
        return MongoDB.__cls_pool[args]

    def __init__(self, database):
        if database not in self.__first_init:
            self.conn = MongoClient(
                host=config['mongo']["host"],
                port=config['mongo']["port"]
            )
            MongoDB.__first_init.append(database)
            db = self.conn[database]
            MongoDB.__database_pool[database] = db
        self.db = MongoDB.__database_pool[database]

    def get_state(self):

        # return self.conn is not None and self.db is not None

        try:
            client = self.conn
            # 利用server_info()判断mongodb状态
            client.server_info()
        except Exception as e:
            logger.error(e)
            return False

        else:
            return True

    def insert_one(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def insert_many(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_many(data, ordered=False)
            return ret.inserted_ids
        else:
            return ""

    def update(self, collection, filter, data, insert=False):
        # data format:
        if self.get_state():
            return self.db[collection].update_one(filter, {"$set": data}, upsert=insert)
        return 0

    def update_one(self, collection, filter, data, insert=False):
        # data format:
        if self.get_state():
            return self.db[collection].update_one(filter, data, upsert=insert)
        return 0

    def update_many(self, collection, filter, data):
        # data format:
        if self.get_state():
            return self.db[collection].update_many(filter, {"$set": data})
        return 0

    def aggs(self, collection, pipeline):
        if self.get_state():
            return list(self.db[collection].aggregate(pipeline))
        return None

    def find(self, col, condition, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition)
            else:
                return self.db[col].find(condition, column)
        else:
            return None

    def find_one(self, col, condition, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find_one(condition)
            else:
                return self.db[col].find_one(condition, column)
        else:
            return None

    def delete(self, col, condition):
        if self.get_state():
            return self.db[col].delete_many(filter=condition).deleted_count
        return 0

    def count(self, col, condition):
        if self.get_state():
            return self.db[col].count_documents(condition)
        return 0

    def drop(self, col):
        if self.get_state():
            return self.db[col].drop()
        return 0

    def close(self):
        if self.get_state():
            self.conn.close()
            return True
        return False
