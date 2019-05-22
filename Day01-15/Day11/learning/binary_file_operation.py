def move_file(original_file_path, target_file_path):
    try:
        with open(original_file_path, 'rb') as fs:
            data = fs.read()
            print(type(data))
        with open(target_file_path, 'wb') as t_fs:
            t_fs.write(data)
    except FileNotFoundError:
        print('file not found!')
    except IOError:
        print('read or write error!')
    print('all is done!')


if __name__ == '__main__':
    move_file('../code/mm.jpg', './mm.jpg')
