from functools import wraps
from time import sleep


def coroutine(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        gen = fn(*args, **kwargs)
        next(gen)
        return gen

    return wrapper


def countdown_gen(n, consumer):
    while n > 0:
        consumer.send(n)
        n -= 1
    consumer.send(None)


@coroutine
def countdown_consumer():
    while True:
        n = yield
        if n:
            print(f'Countdown {n}')
            sleep(1)
        else:
            print('Countdown over')


def main():
    countdown_gen(5, countdown_consumer())


if __name__ == '__main__':
    main()
