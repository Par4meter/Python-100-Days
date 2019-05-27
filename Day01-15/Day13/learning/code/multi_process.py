from multiprocessing import Process
from os import getpid
from random import randint
from time import time, sleep


def download_task(file_name):
    print('启动下载进程，进程号：{process_id}'.format(process_id=getpid()))
    print('开始下载：{file_name}'.format(file_name=file_name))
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('{file_name}下载完成,耗时：{download_time}'.format(file_name=file_name, download_time=time_to_download))


def main():
    start = time()
    p1 = Process(target=download_task, args=['Python 从入门到放弃.mobi'])
    p1.start()
    p2 = Process(target=download_task, args=['Peking Hot.avi'])
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print('共耗时：{total_time:.2f}'.format(total_time=(end - start)))


if __name__ == '__main__':
    main()
