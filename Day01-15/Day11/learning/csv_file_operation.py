import csv


def main():
    try:
        with open('../code/example.csv') as f:
            reader = csv.reader(f)
            print(type(reader))
            print(reader)
            data = list(reader)
    except FileNotFoundError:
        print('file note found!')
    else:
        for item in data:
            print('%-30s%-20s%-10s' % (item[0], item[1], item[2]))


if __name__ == '__main__':
    main()
