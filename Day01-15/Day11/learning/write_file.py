from math import sqrt


def is_prime(n):
    """判断是否素数"""
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True if n != 1 else False


def main():
    file_names = ['1.txt', '2.txt', '3.txt']
    fs_list = [open(filename, 'w', encoding='utf-8') for filename in file_names]
    for num in range(0, 1000000):
        if is_prime(num):
            if num < 100:
                fs_list[0].write(str(num) + '\n')
            elif num < 1000:
                fs_list[1].write(str(num) + '\n')
            elif num < 10000:
                fs_list[2].write(str(num) + '\n')

    print('all is done')


if __name__ == '__main__':
    main()
