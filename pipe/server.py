import os
import json

config = json.load(open('config.json'))

if os.path.exists(config['filepath']):
    os.remove(config['filepath'])

os.mkfifo(config['filepath'], 0o600)

print("FIFO named '% s' is created successfully." % config['filepath'])
print("Type in what you would like to send to clients.")

flag = True

while flag:
    # ユーザーからの入力を取得し、`inputstr`変数に代入します
    inputstr = input()

    if(inputstr == 'exit'):
        flag = False
    else:
        # ファイルを書き込みモードで開きます。
        # `config['filepath']` は設定ファイル内のファイルパスを指定する変数です。
        with open(config['filepath'], 'w') as f:
            # ファイルオブジェクトを`f`として参照します。
            # `with` 文のコンテキスト内では、ファイルは自動的にクローズされます。
            # 書き込み操作を行います。
            f.write(inputstr)

# プログラムの終了時に名前付きパイプを削除します。
os.remove(config['filepath'])