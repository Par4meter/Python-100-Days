import asyncio


@asyncio.coroutine
def countdown(name, n, sleep_time):
    while n > 0:
        print(f'Countdown[{name}]:{n}')
        yield from asyncio.sleep(sleep_time)
        n -= 1


def main():
    loop = asyncio.get_event_loop()
    tasks = [
        countdown('A', 10, 1),
        countdown('B', 5, 5)
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
