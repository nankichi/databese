#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
dbname = 'database.db'
#dbname = ':memory:'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
delete = 'delete from aozora'
cur.execute(delete)
create_table = 'create table if not exists aozora(id int, title varchar(64), author text)'
cur.execute(create_table)
open_csv = open("aozora-min.csv",encoding="utf-8")
read_csv = csv.reader(open_csv)
rows = []
for row in read_csv:
    rows.append(row)
cur.executemany("INSERT INTO aozora(id, title, author) VALUES(?,?,?)",rows)
con.commit()
open_csv.close
cur.close()
con.close()

def application(environ,start_response):
    # HTML（共通ヘッダ部分）
    html = '''<html lang="ja">
           <head>
           <meta charset="UTF-8">
           <title>青空文庫　データベース</title>
           <link rel="stylesheet" href="default.css">
           <style>
           body{
               background: #66cdaa;
               font-family: Meiryo;
           }
           h1{
               font-family: Impact;
               text-align: center;
           }
           div{
               background: #f0e68e;
               width: 400px;
               padding: 10px;
               text-align: center;
               margin: 30px auto;
           }
           p{
               font-family: Impact;
               font-size: 20px;
               text-align: center;
           }
           a{
               font-family: Impact;
               text-align: center;
           }
           input[type="submit"]{
               margin: 15px auto;
           }
           </style>
           </head>'''

    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
    if ('v1' not in form) and ('v2' not in form) and ('v3' not in form):
        # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）

        # HTML（入力フォーム部分）
        html += '<body>\n' \
                '<h1>青空文庫　検索</h1>\n' \
                '<div class="form1">\n' \
                '<form>\n' \
                'ID（整数） <input type="text" name="v1"><br>\n' \
                'タイトル　（文字列） <input type="text" name="v2"><br>\n' \
                '著者  （文字列） <input type="text" name="v3"><br>\n' \
                '<input type="submit" name="Add" value="追加">\n' \
                '<input type="submit" name="IdSearch" value="ID検索">\n' \
                '<input type="submit" name="TitleSearch" value="タイトル検索">\n' \
                '<input type="submit" name="AuthorSearch" value="著者検索">\n' \
                '<input type="submit" name="Delete" value="データの削除">\n' \
                '</form>\n' \
                '</div>\n' \
                '</body>\n'
            
    else:
        # 入力フォームの内容が空でない場合
        
        if form.getfirst('Add'):
            # フォームデータから各フィールド値を取得
            v1 = form.getvalue("v1", "0")
            v2 = form.getvalue("v2", "0")
            v3 = form.getvalue("v3", "0")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'insert into aozora (id, title, author) values (?,?,?)'
            cur.execute(sql, (int(v1),v2,v3))
            con.commit()

            # SQL文（select）の作成
            sql = 'select * from aozora order by rowid desc limit 1'

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' \
                    '<div class="ol1">\n' \
                    '<ol>\n'
            for row in cur.execute(sql):
                html += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
            html += '</ol>\n' \
                    '</div>\n' \
                    '<p>追加しました</p>\n'\
                    '<a href="/">ホームに戻る</a>\n' \
                    '</body>\n'

        elif form.getfirst('IdSearch'):
            # フォームデータから各フィールド値を取得
            v1 = form.getvalue("v1")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'select * from aozora where id = ?'
            con.commit()

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' \
                    '<div class="ol1">\n' \
                    '<ol>\n'
            for row in cur.execute(sql, (v1,)):
                html += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
            html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">ホームに戻る</a>\n' \
                '</body>\n'

        elif form.getfirst('TitleSearch'):
            # フォームデータから各フィールド値を取得
            v2 = form.getvalue("v2")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'select * from aozora where title = ?'
            con.commit()

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' \
                    '<div class="ol1">\n' \
                    '<ol>\n'
            for row in cur.execute(sql, (v2,)):
                html += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
            html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">ホームに戻る</a>\n' \
                '</body>\n'

        elif form.getfirst('AuthorSearch'):
            # フォームデータから各フィールド値を取得
            v3 = form.getvalue("v3")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'select * from aozora where author = ?'
            con.commit()

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' \
                    '<div class="ol1">\n' \
                    '<ol>\n'
            for row in cur.execute(sql, (v3,)):
                html += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
            html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">ホームに戻る</a>\n' \
                '</body>\n'

        elif form.getfirst('Delete'):
            # フォームデータから各フィールド値を取得
            v1 = form.getvalue("v1", "0")
            v2 = form.getvalue("v2", "0")
            v3 = form.getvalue("v3", "0")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'delete from aozora where id = ? and title = ? and author = ?'
            cur.execute(sql, (int(v1),v2,v3))
            con.commit()

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' 

            html += '<p>削除しました</p>\n'\
                '<a href="/">ホームに戻る</a>\n' \
                '</body>\n'



        # カーソルと接続を閉じる
        cur.close()
        con.close()



    html += '</html>\n'
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 test_wsgi.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 test_wsgi.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()
