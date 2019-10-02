import pickle
import re
import zlib
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from redis import Redis
import requests
import hashlib


def main():
    base_url = 'https://www.zhihu.com/'
    seed_url = urljoin(base_url, 'explore')
    client = Redis(host='127.0.0.1', port=6379)
    headers = {'user-agent': 'Baiduspider'}
    resp = requests.get(seed_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html')
    href_regex = re.compile(r'^/question')
    hasher_proto = hashlib.sha1()
    for a_tag in soup.find_all('a', {'href': href_regex}):
        href = a_tag.attrs['href']
        full_url = urljoin(base_url, href)
        hasher = hasher_proto.copy()
        hasher.update(full_url.encode('utf-8'))
        field_key = hasher.hexdigest()
        if not client.hexists('zhihu', field_key):
            html_page = requests.get(full_url, headers=headers)
            zipped_page = zlib.compress(pickle.dumps(html_page))
            client.hset('zhihu', field_key, zipped_page)
    print('Total %d question pages found.' % client.hlen('zhihu'))


if __name__ == '__main__':
    main()
