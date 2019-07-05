import shutil
import os
import time
def main():
    #.は現在いるディレクトリ
    #つまり/schoolfestival
    s = input().strip()#第何回か入力
    a = os.system('sudo mkdir '+s)#sの名前のディレクトリを作る
    if a != 0:#すでにディレクトリがあるよ
        print('directry named "' + s +'" have already been made.You should remove this directory and database named "' + s + '".')
        exit()
    os.system('sudo mysqladmin -u user_name -p create ' + s)#新たなDATABASEを作成
    time.sleep(10)
    print('sudo mysql -u root -p ' + s + ' < from_db.dump.sql')
    os.system('sudo mysql -u root -p ' + s + ' < from_db.dump.sql')#DATABASEにschoolfestival(からのデータベース)をコピー
    name = "schoolfestival.py"#ファイル名になる文字列を作る
    dirPath = "./" + s #コピー先のディレクトリのパス
    shutil.copy("./schoolfestival.py",dirPath)#dirPathのディレクトリのなかにschoolfestival.pyをコピー
    filePath = dirPath + "/" + name #コピーされたschoolfrstivalのパス
    with open(filePath,encoding="utf-8") as f :#コピーされたschoolfestivalのファイルを開く
        data_lines = f.read()#中身のデータを取得
    data_lines = data_lines.replace("schoolfestival",s)#文字列を置換　sのデータベースに接続するようにする
    #このファイルではデータベースの選択にのみ「schoolfestival」の文字列が使われている
    shutil.copy('kill.py',dirPath)#kill.pyをdirPathの中にコピー
    with open(filePath,mode="w",encoding="utf-8") as f:#置換後の文字列をファイルに書き込み
        f.write(data_lines)
if __name__ == "__main__":
    main()

