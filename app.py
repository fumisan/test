# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import os
import glob
from datetime import datetime
import openpyxl
import pprint
from flask_sqlalchemy import SQLAlchemy

UPLOAD_DIR = './uploads/'

app = Flask(__name__)

# オブジェクト変更追跡システム無効設定
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyでデータベースに接続する
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Comment(db.Model):
    """[テーブルの定義を行うクラス]
    Arguments:
        db {[Class]} -- [ライブラリで用意されているクラス]
    """

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text())
    comment = db.Column(db.Text())

    def __init__(self, pub_date, name, comment):
        """[テーブルの各カラムを定義する]
        [Argument]
            id_ -- 投稿番号(プライマリキーなので、自動で挿入される)
            pub_date -- 投稿日時
            name -- 投稿者名
            comment -- 投稿内容
        """

        self.pub_date = pub_date
        self.name = name
        self.comment = comment

try:
    db.create_all()
except Exception as e:
    print(e.args)
    pass

# Main
def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    return np.random.choice(messages)

# Routing
@app.route('/')
def index():
    title = "ようこそ"
    return render_template('index.html', message="ログインしてください", title=title)    

@app.route('/msg')
def msg():
    title = "ようこそ"
    message = picked_up()
    return render_template('msg.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        name = request.form['name']
        return render_template('index.html',
                               name=name, title=title)
    else:
        return redirect(url_for('msg'))

@app.route('/upload', methods=['GET', 'POST'])
def upload() :
    if request.method == 'POST' :
        f = request.files['file1']
        f.save(UPLOAD_DIR + f.filename)
        return render_template('upload.html', message='Uploaded ' + UPLOAD_DIR + f.filename)
    else :
        return render_template('upload.html', message="")


@app.route('/excel', methods=['GET', 'POST'])
def excel() :
    if request.method == 'POST' :
        f = request.files['file1']
        f.save(UPLOAD_DIR + f.filename)
        return render_template('excel.html', message='Uploaded ' + UPLOAD_DIR + f.filename)
    else :
        return render_template('excel.html', message="")

# index.htmlに投稿データを渡す
@app.route("/board", methods=['GET', 'POST'])
def board():
    # テーブルから投稿データをSELECT文で引っ張ってくる
    text = Comment.query.all()
    return render_template("board.html", lines=text)

# 投稿の送信とデータベース追加
@app.route("/boardresult", methods=["POST"])
def boardresult():
    # 現在時刻　投稿者名　投稿内容を取得
    date = datetime.now()
    comment = request.form["comment_data"]
    name = request.form["name"]
    # テーブルに格納するデータを定義する
    comment_data = Comment(pub_date=date, name=name, comment=comment)
    # テーブルにINSERTする
    db.session.add(comment_data)
    # テーブルへの変更内容を保存
    db.session.commit()
    return render_template("boardresult.html", comment=comment, name=name, now=date)



if __name__ == '__main__':
    app.debug = True
    app.run()
