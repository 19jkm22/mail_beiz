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

"""
print ("Content-type: text/html\n\n")
print("<html><head><link rel='stylesheet' href='./../style.css' type='text/css'/></head><body><div class = 'main'>")
print('<div class="main2">')
n = 1
"""
def maru(text):
    #リストの生成
    list = {}

    #^を終端-始端記号に置換
    oneMails = text.split("^")
    num2 = 0
    for text2 in oneMails:
        #始端,終端記号の埋め込み
        text2 = "start "+text2
        text2 = text2 + " end"
        text2 = text2.replace("\r","")
        text2 = text2.replace("\u3000","")
        print("<br>"+text2+"<br>")
        mt = MeCab.Tagger("-Owakati")
        m2 = mt.parse(text2).split(" ")#文を分かち書きする
        
        num = 0
        if(len(m2)>3):
            while num+2 < len(m2):
                t3 = (m2[num],m2[num+1],m2[num+2])
                num+=1
                num2+=1
                list[str(num2)] = t3
        print(list)
    #改行はスペースに
    """
    text.replace("\n"," ")
    mt = MeCab.Tagger("-Owakati")
    m2 = mt.parse(text).split(" ")#文を分かち書きする
    num = 0
    if(len(m2)>3):
        while num+2 < len(m2):
            t3 = (m2[num],m2[num+1],m2[num+2])
            num+=1
            list[str(num)] = t3
    print(list)
    """
    
    #始端記号の指定
    init = "start"
    a = 0
    out = ""
    while ("end" not in init):
        randList = []
        for tempListNum in list.keys():
            if(list[tempListNum][0] == init):
                randList.append(tempListNum)
                
        if(len(randList) == 0):break
        rand = random.randint(0,len(randList)-1)
        start = list[str(randList[rand])]
        out+=start[1]+start[2]
        init = start[2]
        print("<br>")
        a+=1
    #終端記号を切り取ってから戻す
    print(out[:-4])
    return out[:-4]
            
"""
if n == 0:
	#ついったに接続＆タイムライン取得＆データベース書き込み
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
		#^を終端-始端に
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
"""
