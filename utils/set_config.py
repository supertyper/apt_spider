from config.template import config, path
import configparser
import json
from utils.logger import get_logger


logger = get_logger(__file__)


def get_config_value(theme, params):
    """
    Get config value
    """

    conf = configparser.ConfigParser()
    conf.read(path['config_path'])
    value = conf.get(theme, params)

    return value


def set_mail_config():
    try:
        config['mail'] = dict()
        config['mail']['host'] = get_config_value('mail', 'host')
        config['mail']['port'] = get_config_value('mail', 'port')
        config['mail']['mails'] = get_config_value('mail', 'mails')
        config['mail']['from'] = get_config_value('mail', 'from')
        config['mail']['password'] = get_config_value('mail', 'password')
        config['mail']['to'] = get_config_value('mail', 'to').split(',')
    except Exception as e:
        logger.error(e)


def set_crawler_config():

    with open(path['crawler_path'], 'r') as f:
        json_conf = f.read()

    config['crawler'] = json.loads(json_conf)


def set_mongo_config():
    try:
        config['mongo'] = dict()
        config['mongo']["host"] = get_config_value('mongo', 'host')
        config["mongo"]["port"] = int(get_config_value('mongo', 'port'))
        config["mongo"]["db"] = get_config_value('mongo', 'db')
    except Exception as e:
        logger.error(e)
        print(e)


def set_redis_config():
    try:
        config['redis'] = dict()
        config['redis']['host'] = get_config_value('redis', 'host')
        config['redis']['port'] = get_config_value('redis', 'port')
    except Exception as e:
        logger.error(e)


def set_config():
    set_mail_config()
    set_crawler_config()
    set_mongo_config()
    set_redis_config()

