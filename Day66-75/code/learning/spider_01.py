import re
import ssl
from urllib.error import URLError
from urllib.request import urlopen

import pymysql
from pymysql import Error


def decode_page(page_bytes, charsets=('utf-8')):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except Exception:
            pass
    return page_html


def get_html_page(seed_url, *, retry_times=3, charsets=('utf-8')):
    """获取指定URL的HTML文本"""
    html_page = None
    try:
        if retry_times > 0:
            html_page = decode_page(urlopen(seed_url).read(), charsets)
    except URLError:
        return get_html_page(seed_url, retry_times=retry_times - 1, charsets=charsets)
    return html_page


def get_matched_part(html_page, match_pattern, pattern_ignore_case=re.I):
    regex = re.compile(match_pattern, pattern_ignore_case)
    return regex.findall(html_page) if html_page else []


def format_links(links):
    formatted_links = []
    for link in links:
        if link.startswith('http') or link.startswith('https'):
            formatted_links.append(link)
        if link.startswith('//'):
            formatted_links.append(link.replace('//', 'http://'))
    return formatted_links


def start_crawl(seed_url, match_pattern, *, max_depth=-1):
    """开始执行爬虫程序并持久化"""
    conn = pymysql.connect(host='localhost', port=3306, database='python-learning', user='eric', password='eric@mysql',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            url_list = [seed_url]
            visited_url_list = {seed_url: 0}
            while url_list:
                current_url = url_list.pop(0)
                depth = visited_url_list[current_url]
                if depth != max_depth:
                    html_page = get_html_page(current_url, charsets=('utf-8', 'gbk', 'gb2312'))
                    links = format_links(get_matched_part(html_page, match_pattern))
                    param_list = []
                    for link in links:
                        if link not in visited_url_list:
                            visited_url_list[link] = depth + 1
                            page = get_html_page(link, charsets=('utf-8', 'gbk', 'gb2312'))
                            headings = get_matched_part(page, r'<h[1,2]>.*<span>.*</span>')
                            if headings:
                                param_list.append((headings[0], link))
                    cursor.executemany('insert into tb_result(title, link) values (%s,%s)', param_list)
                    conn.commit()
    except Error:
        pass
    finally:
        conn.close()


def main():
    ssl.create_default_https_context = ssl._create_unverified_context
    start_crawl('http://sports.sohu.com/s/nba',
                r'<a[^>]+\s[^>]*href=["\'](.*?)["\']',
                max_depth=2)


if __name__ == '__main__':
    main()
