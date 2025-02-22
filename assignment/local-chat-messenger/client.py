import socket, os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

client_address = '/tmp/client_socket_file'

server_address = '/tmp/server_socket_file'

try:                                #client側でもソケットファイルが残っていたら、OSError: [Errno 98] Address already in use
    os.unlink(client_address)       #というエラー出るので、ソケットファイルを消しておく
except FileNotFoundError:
    pass

sock.bind(client_address)

try:
    while True:
        print("please enter your message to send to a server\n(enter \"exit\" to quit)\n")
        message = input()
        if message == "exit":
            break
        message = message.encode()
        sent = sock.sendto(message, server_address)
        data, server = sock.recvfrom(4096) #recvfrom : サーバーからのメッセージとアドレスを取得する

         # サーバから受け取ったメッセージを表示します
        print('received\n {} \n'.format(data.decode()))
finally:
    print("closing socket")
    sock.close()