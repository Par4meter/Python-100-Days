from time import sleep


def countdown_gen(n, consumer):
    consumer.send(None)
    while n > 0:
        consumer.send(n)
        n -= 1
    consumer.send(None)


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
