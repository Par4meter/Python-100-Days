def read_file():
    f = open('../code/致橡树.txt', 'r', encoding='utf-8')
    print(f.read())


def read_file_with_try():
    try:
        f = open('../code/致橡树.txt', 'r', encoding='utf-8')
        print(f.read())
    except FileNotFoundError:
        print('无法找到指定文件！')
    finally:
        if f:
            f.close()


def read_lines_from_file():
    with open('../code/致橡树.txt', 'r', encoding='utf-8') as f:
        print(f.readlines())


if __name__ == '__main__':
    read_lines_from_file()
