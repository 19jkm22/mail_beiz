# -*- coding: utf-8 -*-
import Twi
import re
import cgi
from requests_oauthlib import OAuth1Session
import json
import MeCab
import sqlite3
import io, sys
import random
import codecs


print ("Content-type: text/html\n\n")
print("<html><head><link rel='stylesheet' href='./../style.css' type='text/css'/></head><body><div class = 'main'>")
print('<div class="main2">')
n = 1
if n == 0:
	#ついったに接続＆タイムライン取得＆データベース書き込み
	twi =  Twi.Twi()
	twi.getTweet()
	form = cgi.FieldStorage()
	conn = sqlite3.connect("data2.db")
	cur = conn.cursor()
	mt = MeCab.Tagger("-Owakati")
	f = codecs.open('neko.txt','r','utf-8')
	data1 = f.read()  # ファイル終端まで全て読んだデータを返す
	lines = data1.split('\r\n')
	textNum = 0
	for line in lines:
		m2 = start+mt.parse(line).split(" ")#文を分かち書きする
		num = 0
		if(len(m2)>3):
			while num+2 < len(m2):
				t3 = (textNum,m2[num],m2[num+1],m2[num+2])
				cur.execute('INSERT INTO text VALUES(?,?,?,?)', t3)
				textNum+=1
				num+=1
			conn.commit()

	f.close()

#データベースから３次のマルコフ連鎖を生成する
conn = sqlite3.connect("data2.db")
cur = conn.cursor()

init = ("start",)


list = ""
a = 0
while a < 50:
    cur.execute('SELECT COUNT(*) FROM text WHERE text1 == (?)',init)
    textNum = int(cur.fetchone()[0])-1
    if(textNum<0):break
    rand = random.randint(0,textNum)
    cur.execute('SELECT * FROM text WHERE text1 == (?)',init)
    cur.rowcount
    temp = 0
    start = cur.fetchall()[rand]
    list+=start[1]+start[2]
    init = (start[3],)
    print(start)
    print("<br>")
    a+=1
print(list)