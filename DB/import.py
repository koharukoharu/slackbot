# -*- coding: utf-8 -*-

# yahoo路線にあった路線データ(CSVを作成)から一括でmySQLにインサート
# dbはテーブルまで作成済みの状態から実行する。

#db = train
#show tables;
#+-----------------+
#| Tables_in_train |
#+-----------------+
#| train_list      |
#+-----------------+

#+--------------------------------------------------+-----------+------+
#| name                                             | area      | user |
#+--------------------------------------------------+-----------+------+

import csv
from urllib.parse import urlparse
import mysql.connector

url = urlparse('mysql://db_user:db_user@localhost:3306/train')
conn = mysql.connector.connect(
    host = url.hostname or 'localhost',
    port = url.port or 3306,
    user = url.username or 'db_user',
    password = url.password or 'db_user',
    database = url.path[1:],
)

cur = conn.cursor()

def cleate_csv_dic():
    csv_file = open("train.csv", "r")
    f = csv.reader(csv_file)
    for row in f:
        rosen = row[0]
        areas = row[1]

        try:
            cur.execute("INSERT INTO train.train_list (name, area, user) VALUES (%s, %s, '-')", (rosen, areas))
            conn.commit()
        except:
            conn.rollback()
            raise

cleate_csv_dic()
