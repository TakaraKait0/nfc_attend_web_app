import re
import sqlite3

import nfc
import pymsteams
import requests


def extract_data_from_dump(dump_str: str) -> str:
    # 正規表現で | で囲まれた部分を抽出
    matches = re.findall(r"\|([^\|]+)\|", dump_str)
    student_number = matches[0].replace(" ", "")
    return student_number

def fetch_data_from_db(extracted_id):
    connection = sqlite3.connect('student_id_data.db')  # SQLデータベースに接続します
    cursor = connection.cursor()
    
    query = "SELECT class, name FROM student_data WHERE id = ?"
    cursor.execute(query, (extracted_id,))
    result = cursor.fetchone()
    
    connection.close()
    return result

def slack(message):
    webhook_url = "slackでbotを作成するときのURL"
    payload = {"text": message}
    result = requests.post(webhook_url, json=payload)

def on_connect(tag: nfc.tag.Tag) -> bool:
    print("connected")
    dump_str = "\n".join(tag.dump())
    extracted_data = extract_data_from_dump(dump_str)
    print(extracted_data)

    result = fetch_data_from_db(extracted_data)
    print(result)
    
    if result:
        class_name, student_name = result
        slack(f"{class_name} {student_name} 活動します")
    return True

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")

def main():
    clf = nfc.ContactlessFrontend("usb")

    while True:
        try:
            clf.connect(rdwr={"on-connect": on_connect}) #, "on-release": on_release})
        except KeyboardInterrupt:
            print("Ctrl+Cが押されました．")
        finally:
            break

if __name__ == "__main__":
    main()