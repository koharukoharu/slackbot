# -*- coding: utf-8 -*-
import mysql.connector
from urllib.parse import urlparse
import json

# DBコネクション
url = urlparse('mysql://db_user:db_user@localhost:3306/train')

conn = mysql.connector.connect(
host = url.hostname or 'localhost',
port = url.port or 3306,
user = url.username or 'db_user',
password = url.password or 'db_user',
database = url.path[1:]
)
cur = conn.cursor(dictionary=True)

# 路線名による曖昧検索
def Train_search_name(name):
    try:
        cur.execute("SELECT * FROM train_list where name Like '%%%s%%'" % (name))
        text = cur.fetchall()
        text = json.dumps(text, ensure_ascii=False)
    except:
        text = '検索に失敗しました'
    finally:
        return text
        conn.close()
        cur.close()

# エリアによる検索
def Train_search_area(area):
    try:        
        cur.execute("SELECT * FROM train_list where area = '%s'" % (area))
        text = cur.fetchall()
        text = json.dumps(text, ensure_ascii=False)
    except:
        text = '検索に失敗しました'
    finally:
        return text
        conn.close()
        cur.close()


