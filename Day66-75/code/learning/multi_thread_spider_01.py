from enum import Enum
from queue import Queue
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


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
        self.staus = SpiderStatus.IDLE

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
        links = []
        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            scheme = parser.scheme or 'http'
            netloc = parser.netloc or domain
            if scheme != 'javascript' and netloc == domain:
                path = parser.path
                query_string = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query_string}'
                if full_url not in visited_url:
                    links.append(full_url)
        return links

    def store(self):
        pass


class SpiderThread(Thread):
    def __init__(self, name, spider, task_queue):
        super().__init__(name=name, daemon=True)
        self.spider = spider
        self.task_queue = task_queue

    def run(self):
        while True:
            url = self.task_queue.get()
            self.spider.status = SpiderStatus.WORKING
            page_html = self.spider.fetch(url)
            if page_html not in [None, '']:
                links = self.spider.parse(page_html)
                for link in links:
                    self.task_queue.put(link)
            self.spider.status = SpiderStatus.IDLE


def is_any_alive(spider_threads):
    return any(SpiderStatus.WORKING == spider_thread.spider.status for spider_thread in spider_threads)


visited_url = set()
default_charsets = ['utf-8', 'gbk', 'gb2312']


def main():
    task_queue = Queue()
    task_queue.put('http://m.sohu.com/')
    spider_threads = [SpiderThread(f'spider_thread_{i}', Spider(), task_queue) for i in range(10)]

    for spider_thread in spider_threads:
        spider_thread.start()

    while not task_queue.empty() or is_any_alive(spider_threads):
        sleep(5)
    print('finish')


if __name__ == '__main__':
    main()
