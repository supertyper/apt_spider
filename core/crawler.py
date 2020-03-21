from utils.thread import task_thread
from utils.logger import get_logger


class CrawlerBase(object):

    def __init__(self):
        self.thread = getattr(self, "thread", 5)
        self.desc = getattr(self, "desc")
        self.crawl_logger = get_logger("crawler")
        self.logger = get_logger(self.desc)

    def get_url_list(self):
        pass

    def get_info(self, url):
        pass

    def start(self):
        try:
            task_thread(self.get_info, self.get_url_list(), self.thread)
            self.crawl_logger.info("{}插件加载成功,线程{}".format(self.desc, self.thread))
        except:
            import traceback
            traceback.print_exc()
