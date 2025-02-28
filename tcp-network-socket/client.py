import socket, sys, os

# protocol_header()という関数は、サーバに送信されるファイルのヘッダ情報をフォーマットするために使用されます。
# このヘッダは、ファイル名の長さ（バイト）、JSONデータの長さ（バイト）、データの長さ（バイト）の3つの値で構成されます。
# これらの値は、to_bytes()メソッドを用いてバイナリに変換され、1つの64ビットバイナリに結合されます。
def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3, "big") + data_length.to_bytes(4, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバが待ち受けているポートにソケットを接続します
server_address = input("Type in the server's address to connect to: ")
server_port = 9001

print('connecting to {}'.format(server_address, server_port))

try:
    # 接続後、サーバとクライアントが相互に読み書きができるようになります
    sock.connect((server_address, server_port))
    print("connection is success")
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    # ファイルを送信する場合は、テキストファイルで2GB以下に制限してください
    filepath = input('Type in a file to upload: ')

    # バイナリモードでファイルを読み込む
    with open(filepath, 'rb') as f:
        # ファイルの末尾に移動し、tellは開いているファイルの現在位置を返します。ファイルのサイズを取得するために使用します
        f.seek(0, os.SEEK_END)#seekメソッドはファイルの起点を変えることができる。デフォルトは０行目、ここではファイルの最後に起点を変えている。
        filesize = f.tell()#tellメソッドはファイルの現在の起点を整数（バイト）で返す。ファイルの先頭からのバイト数
        f.seek(0,0)#ファイルの起点を元に戻している

        if filesize > pow(2,32):#pow(num1, num2)は、num1のnum2乗を表す。ここでは、２の３２乗
            raise Exception('File must be below 2GB.')

        filename = os.path.basename(f.name)#basenameメソッドは、dir1/dir2/dir3/.../fileのfileのみを抜き出す

        # ファイル名からビット数
        filename_bits = filename.encode('utf-8')

        # protocol_header()関数を用いてヘッダ情報を作成し、ヘッダとファイル名をサーバに送信します。
        header = protocol_header(len(filename_bits), 0, filesize)

        # ヘッダの送信
        sock.send(header)

        # ファイル名の送信
        sock.send(filename_bits)

        # 一度に4096バイト（4096ビット）ずつ読み出し、送信することにより、ファイルを送信します。Readは読み込んだビットを返します
        data = f.read(4096)
        while data:
            print("Sending...")
            sock.send(data)
            data = f.read(4096)

finally:
    print('closing socket')
    sock.close()