from socket import socket, AF_INET, SOCK_STREAM


def main():
    server = socket(family=AF_INET, type=SOCK_STREAM)
    server.bind(('127.0.0.1', 61525))
    server.listen(1024)
    print('====================服务开启监听====================')
    while True:
        client, addr = server.accept()
        print(str(addr) + '连接到了服务器！')
        client.send('走好，不送'.encode('utf-8'))
        client.close()


if __name__ == '__main__':
    main()
