from random import randint
from threading import Thread, Lock
from time import sleep, time


class DownloadTask(Thread):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name

    def run(self):
        print('开始下载：{file_name}'.format(file_name=self._file_name))
        time_to_download = randint(3, 10)
        sleep(time_to_download)
        print('{file_name}下载完成,耗时：{download_time}'
              .format(file_name=self._file_name, download_time=time_to_download))


class Account(object):

    def __init__(self):
        self._balance = 0

    def deposit(self, money):
        new_balance = self._balance + money
        sleep(0.01)
        self._balance = new_balance

    @property
    def balance(self):
        return self._balance


class AccountWithLock(object):

    def __init__(self):
        self._balance = 0
        self._lock = Lock()

    def deposit(self, money):
        self._lock.acquire()
        try:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            self._lock.release()

    @property
    def balance(self):
        return self._balance


class AddMoneyThread(Thread):

    def __init__(self, account, money):
        super().__init__()
        self._account = account
        self._money = money

    def run(self):
        self.deposit()

    def deposit(self):
        self._account.deposit(self._money)


def multi_thread_download_test():
    start = time()
    file_names = ['下载什么呢.txt', '就下这个吧.exe']
    threads = [DownloadTask(file_name) for file_name in file_names]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time()
    print('下载完成，共耗时:{:.2f}'.format((end - start)))


def multi_thread_deposit(account):
    threads = [AddMoneyThread(account, 100) for i in range(0, 100)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('当前账户余额：${balance}'.format(balance=account.balance))


if __name__ == '__main__':
    # multi_thread_download_test()
    multi_thread_deposit(Account())  # thread unsafe
    multi_thread_deposit(AccountWithLock())  # thread safe
