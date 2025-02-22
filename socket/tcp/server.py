import os, socket
                    
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)#socketをstreamモードで作っている

server_address = '/tmp/socket_file'# このサーバが接続を待つUNIXソケットのパスを設定します

try:
    os.unlink(server_address)   #以前の接続が残っている場合があるので、サーバアドレスを削除している
except FileNotFoundError:
    pass

print("Starting up on {}".format(server_address))

sock.bind(server_address)#サーバアドレスにソケットを接続

sock.listen(1)#ソケットが接続要求を待機するようにする

while True:
    connection, client_address = sock.accept()
    try:
        print("connection from", client_address)

        while True:
            data = connection.recv(16)
            data_str = data.decode('utf-8')
            print('Received' + data_str)
            # もしデータがあれば（つまりクライアントから何かメッセージが送られてきたら）以下の処理をします。
            if data:
                # 受け取ったメッセージを処理します。
                response = 'Processing ' + data_str

                # 処理したメッセージをクライアントに送り返します。
                # ここでメッセージをバイナリ形式（エンコード）に戻してから送信します。
                connection.sendall(response.encode())

            # クライアントからデータが送られてこなければ、ループを終了します。
            else:
                print('no data from', client_address)
                break

    # 最終的に接続を閉じます
    finally:
        print("Closing current connection")
        connection.close()