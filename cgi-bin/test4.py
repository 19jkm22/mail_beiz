#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Beiz
import cgi
import os
import sys
import io, sys
from struct import *
import Twitter
import sqlite3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)

print ("Content-type: text/html\n\n")
print("<html><head><link rel='stylesheet' href='./../style.css' type='text/css'/></head><body><div class = 'main'>")
form = cgi.FieldStorage()
a = Beiz.Beiz()
print((form["info"]))
print("</div>")

a.train("いらない",a.mm(form.getvalue('info','')))
a.train("いる",a.mm(form.getvalue('info2','')))
print(a.list)


conn = sqlite3.connect("data.db")
cur = conn.cursor()

print("<form name = 'f' action = 'test4.py' method = 'POST' onSubmit = 'add()' accept-charset = 'UTF-8'>")
#ツイートの表示
select_sql = "SELECT name,image,text,mediaID,tweet.id FROM tweet,user WHERE tweet.userID = user.userID ORDER BY tweet.id desc"
for row in cur.execute(select_sql):
    if(a.beiz(a.mm(row[2])) == "いらない"):
        print("いらない！！！！！！！！！！！！！！！！！！！！！！！！！！！")
    print("<div id = '"+str(row[4])+"' title = '"+str(row[2])+"'><br>"+row[0]+"<br>")
    print("<img src = '"+row[1]+"'>")
    print(row[2])
    if(row[3]!=-1):
        img_sql = "SELECT url FROM image WHERE (?) = image.id"
        cur2 = conn.cursor()
        for r in cur2.execute(img_sql,(row[3],)):
            print("<img src = '"+r[0]+"'>")
    print("<br>")
    print('<input type="checkbox" name = "c" value="'+str(row[4])+'" onClick="cl('+"'"+str(row[4])+"'"+')">いらないツイート<br> ')#なんか""でくくらないと値がおかしくなるっぽい（オーバーフロー？）
    print("</div>")
    
print("</form>")
print("</div>")
print("</div>")