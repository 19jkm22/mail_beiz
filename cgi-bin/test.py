#!/usr/bin/python
import cgi
form = cgi.FieldStorage()

print ("Content-type: text/html\n\n")
print("<html><head></head><body>")
print ("テスト："+form["foo"].value)


import MeCab
input = form["foo"].value
mt = MeCab.Tagger("")
m2 = mt.parse(input).split("\n")
num = 0
m3 = []
for s in m2:
	#m3[num] = s.split("\n");
	m3.append(s.split("\t"));
	num=num+1

beforeName = ""
num = 0
num2 = 0
index = 0;
dousi = []

countList = [];#主語をぶち込むlist
for s in m3:
	if(s[0] == "EOS"): break
	temp = s[0]#わかちがきしたやつ
	temp2 = s[1].split(",")[1]#こっちに名詞とか
	if(temp2.find("固有名詞")!=-1):
		countList.append(temp);
	if(temp2.find("動詞")!=-1):
		countList.append(temp);
print("<br>")
for s in countList:
	print(s)
	print("<br>")
