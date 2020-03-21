import redis
from filter.filter import Filter
import json
import time
from config.template import config

class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host=config["redis"]["host"],port=config["redis"]["port"])
        # self.__conn = redis.Redis(host="127.0.0.1",port="32769")
        self.channel = 'ioc' 

    def publish(self,msg):
        self.__conn.publish(self.channel,msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub

def send_ioc(ioc):
    obj = RedisHelper()
    obj.publish(json.dumps(ioc))

def deal_ioc():
    obj = RedisHelper()
    redis_sub = obj.subscribe()
    while True:
        msg= redis_sub.parse_response()
        ioc = json.loads(msg[-1])
        test = Filter(ioc)
        print(test.check_ioc())
        time.sleep(5)