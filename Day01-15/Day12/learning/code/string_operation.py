def reserve_string(target):
    return target[::-1]


if __name__ == '__main__':

    string = '  Hello World  '
    print(string.strip())
    print(list(string))
    print(r'a\a\a\aa\a\a')
    print(reserve_string('Hello World'))
