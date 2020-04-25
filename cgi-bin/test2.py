#!/usr/bin/python
from requests_oauthlib import OAuth1Session

import cgi
import json
import MeCab
import sqlite3
import Twitter
import io, sys

conn = sqlite3.connect("data.db")
cur = conn.cursor()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)


print ("Content-type: text/html\n\n")
print("<html><head><link rel='stylesheet' href='./../style.css' type='text/css'/></head><body><div class = 'main'>")
print('<div class="main2">')

#twi =  Twitter.Twitter()
#twi.getTweet()
print("<form name = 'f' action = 'test4.py' method = 'POST' onSubmit = 'add()' accept-charset = 'UTF-8'>")
#ツイートの表示
select_sql = "SELECT name,image,text,mediaID,tweet.id FROM tweet,user WHERE tweet.userID = user.userID ORDER BY tweet.id desc"
for row in cur.execute(select_sql):
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
    
print('<input type="text" name = "info" id="info" value="てすとだよーーーーーー！！！！" />')
print('<input type="text" name = "info2" id="info2" value="てすとだよーーーーーー！！！！" />')
print("<input type = 'submit' value = 'おけ'>")

print("</form>")
print("</div>")
print("</div>")
print('''
<script>
function cl(value){
    var element = document.getElementById(value); 
    element.style.backgroundColor = 'red'; 
}
function add(f){
    var str = "";
    var str2 = "";
    // チェックボックスの数だけ判定を繰り返す（ボタンを表すインプットタグがあるので１引く）
    for(var i=0; i<document.f.c.length-1;i++){
        // i番目のチェックボックスがチェックされているかを判定
        if(document.f.c[i].checked){
            str += document.getElementById(document.f.c[i].value).title+",";
        }else{
            str2 += document.getElementById(document.f.c[i].value).title+",";
        }
    }
    document.getElementById('info').value = str;
    //document.getElementById('info2').value = str2;
    
}
</script>
''')