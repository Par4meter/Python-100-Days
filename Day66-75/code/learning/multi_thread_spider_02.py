import pickle
import zlib
from _threading_local import local
from enum import Enum
from queue import Queue
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import pymongo
import requests
from _sha1 import sha1
from bs4 import BeautifulSoup
from bson import Binary
from redis import Redis


class SpiderStatus(Enum):
    IDLE = 0,
    WORKING = 1


def decode_page(page_bytes, charsets=tuple(['utf-8'])):
    page_html = None

    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            print('decode error')
    return page_html


class Spider(object):
    def __init__(self):
        self.status = SpiderStatus.IDLE

    @staticmethod
    def fetch(current_url, *, charsets=tuple(['utf-8']), useragent=None, proxies=None):
        thread_name = current_thread().name
        print(f'[{thread_name}]:{current_url}')
        headers = {'user-agent': useragent}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets) if 200 == resp.status_code else None

    @staticmethod
    def parse(page_html, *, domain='m.sohu.com'):
        soup = BeautifulSoup(page_html, 'html')
        redis_client = thread_local.redis_client
        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            scheme = parser.scheme or 'http'
            netloc = parser.netloc or domain
            if scheme != 'javascript' and netloc == domain:
                path = parser.path
                query_string = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query_string}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush(task_name, full_url)

    def store(self):
        pass


class SpiderThread(Thread):
    def __init__(self, name, spider):
        super().__init__(name=name, daemon=True)
        self.spider = spider

    def run(self):
        redis_client = Redis(host='127.0.0.1', port=6379)
        mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        thread_local.redis_client = redis_client
        thread_local.mongo_client = mongo_client
        while True:
            url = redis_client.lpop(task_name)
            while not url:
                url = redis_client.lpop(task_name)
            self.spider.status = SpiderStatus.WORKING
            url = url.decode('utf-8')
            if not redis_client.sismember('visited_urls', url):
                redis_client.sadd('visited_urls', url)
            page_html = self.spider.fetch(url)
            if page_html not in [None, '']:
                hasher = hasher_proto.copy()
                hasher.update(url.encode('utf-8'))
                doc_id = hasher.hexdigest()
                sohu_data_coll = mongo_client.msohu.webpages
                if not sohu_data_coll.find_one({'_id': doc_id}):
                    sohu_data_coll.insert_one({
                        '_id': doc_id,
                        'url': url,
                        'page': Binary(zlib.compress(pickle.dumps(page_html)))
                    })

                self.spider.parse(page_html)
            self.spider.status = SpiderStatus.IDLE


def is_any_alive(spider_threads):
    return any(SpiderStatus.WORKING == spider_thread.spider.status for spider_thread in spider_threads)


thread_local = local()
hasher_proto = sha1()
task_name = 'm_souhu_task'


def main():
    redis_client = Redis(host='127.0.0.1', port=6379)
    if not redis_client.exists(task_name):
        redis_client.rpush(task_name, 'http://m.sohu.com/')
    spider_threads = [SpiderThread(f'spider_thread_{i}', Spider()) for i in range(10)]

    for spider_thread in spider_threads:
        spider_thread.start()

    while redis_client.exists(task_name) or is_any_alive(spider_threads):
        sleep(5)
    print('finish')


if __name__ == '__main__':
    main()
