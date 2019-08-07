import requests
from threading import Thread


class DownloadHandler(Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        resp = requests.get(url=self.url)
        print(resp.content)


def main():
    url = 'https://www.baidu.com'
    DownloadHandler(url).start()


if __name__ == '__main__':
    main()
