import json
import re
import sqlite3
import sys

import nfc

dbname = "student_id_data.db"  # データベース名.db拡張子で設定
conn = sqlite3.connect(dbname, isolation_level=None)  # データベースを作成、自動コミット機能ON

cursor = conn.cursor()  # カーソルオブジェクトを作成

def extract_data_from_dump(dump_str: str) -> str:
    # 正規表現で | で囲まれた部分を抽出
    matches = re.findall(r"\|([^\|]+)\|", dump_str)
    student_number = matches[0].replace(" ", "")
    return student_number

def on_connect(tag: nfc.tag.Tag, grade: str, name: str) -> bool:
    print("connected")
    dump_str = "\n".join(tag.dump())
    extracted_data = extract_data_from_dump(dump_str)
    print(extracted_data)
    # 重複したidの場合は挿入をスキップするように修正
    sql = """INSERT OR IGNORE INTO student_data (class, id, name) VALUES(?, ?, ?)"""  # 重複時は無視して挿入しない

    data = (grade, extracted_data, name)  # 挿入するレコードを指定
    cursor.execute(sql, data)  # executeコマンドでSQL文を実行
    conn.commit()  # コミットする

    return True

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")

def main(grade: str, name: str):
    # テーブルを作成し、idカラムにユニーク制約を追加
    sql = """CREATE TABLE IF NOT EXISTS student_data(class TEXT, id INTEGER UNIQUE, name TEXT)"""
    cursor.execute(sql)  # executeコマンドでSQL文を実行
    conn.commit()  # データベースにコミット

    clf = nfc.ContactlessFrontend("usb")

    while True:
        try:
            clf.connect(rdwr={"on-connect": lambda tag: on_connect(tag, grade, name)})
            # clf.connect(rdwr={"on-connect": on_connect}) #, "on-release": on_release})

        except KeyboardInterrupt:
            print("Ctrl+Cが押されました．")
        finally:
            sql = """SELECT * FROM student_data"""
            cursor.execute(sql)
            print(cursor.fetchall())  # 全レコードを取り出す
            # 作業完了したらDB接続を閉じる
            conn.close()
            break

if __name__ == "__main__":
    if len(sys.argv) == 3:
        grade = sys.argv[1]
        name = sys.argv[2]
        main(grade, name)
    else:
        print("Error: 学年と名前の2つの引数を指定してください。")