def fib():
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield a


def even(gen):
    for val in gen:
        if 0 == val % 2:
            yield val


def main():
    gen = even(fib())
    for _ in range(10):
        print(next(gen))


if __name__ == '__main__':
    main()
