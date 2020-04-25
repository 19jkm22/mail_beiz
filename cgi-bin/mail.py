import imaplib, re, email, six, dateutil.parser
import pykf
import dateutil.parser
import base64
import io, sys
import sqlite3
import cgi,re
import os,Beiz
import Maru

from requests_oauthlib import OAuth1Session
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                          encoding=sys.stdout.encoding, 
                          errors='backslashreplace', 
                          line_buffering=sys.stdout.line_buffering)
email_default_encoding = 'iso-2022-jp'
print ("Content-type: text/html\n\n")
print("""
<html><head>
<title>めーる</title> 
<link rel='stylesheet' type='text/css' href='./../style.css'>
<script type='text/javascript' src='./../tree.js'></script>
</head><body>
""")

form = cgi.FieldStorage()
conn = sqlite3.connect("mail.db")
cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()
a = Beiz.Beiz()

def labelRe():
    for row in cur.execute("SELECT * FROM labelIndex"):
        a.setIndexNum(row[0],row[1])

    for row in cur2.execute("SELECT * FROM mailList"):
        temp = a.beiz(a.mm(row[3]))
        cur.execute('UPDATE mailList SET labelID = ? WHERE mailID = ?',(temp,row[0]))
        conn.commit()
    #print(a.getList())

    """
    for row in cur2.execute("SELECT * FROM mailLabel"):
        print(row)
        print("<br>")
    """
    conn.commit()
    
def set():
    t3 = (1,"テスト2")
    cur.execute('INSERT INTO label VALUES(?,?)', t3)
    conn.commit()
    t3 = (2,"2017-6-23","テスト3","テスト本文")
    cur.execute('INSERT INTO mailList VALUES(?,?,?,?)', t3)
    conn.commit()
    t3 = (1,"2017-6-23","テスト2","テスト本文")
    cur.execute('INSERT INTO mailList VALUES(?,?,?,?)', t3)
    conn.commit()
    print(t3)
    
def setup():
    listUpdate()
    #学習
    if("mailText" in form.keys()):
        t3 = (form["train"].value,form["mailText"].value)
        cur.execute("SELECT COUNT(*) FROM trainMail WHERE labelID = ?",(form["train"].value,))
        if(int(cur.fetchone()[0]) == 0):
            cur.execute('INSERT INTO trainMail VALUES(?,?)', t3)
        else:
            t3 = (form["mailText"].value,form["train"].value)
            cur.execute('UPDATE trainMail SET content = ? WHERE labelID = ?', (t3))
        conn.commit()
        print("保存したよ")
        #print(form["mailText"].value)
        
        wordBag = []
        temp = []
        a.resetLabel(form["train"].value)
        #学習フェーズ
        #indexNumのリセット
        for row in cur.execute("SELECT * FROM labelIndex"):
            print(row)
            a.setIndexNum(row[0],row[1])
        cur.execute("DELETE FROM trainData WHERE labelID = ?",(form["train"].value,))
        conn.commit()
        indexNum = 0        
        for text in str(form["mailText"].value).split('^'):
            temp = a.mm(text)
            a.train(str(form["train"].value),temp)
            indexNum+=1;
            wordBag.extend(temp)
            
        #indexNumの設定
        #a.setIndexNum(int(form["train"].value),indexNum);
        cur.execute("SELECT COUNT(*) FROM labelIndex WHERE labelID = ?",(form["train"].value,))
        if(int(cur.fetchone()[0]) == 0):
            cur.execute("INSERT INTO  labelIndex VALUES(?,?)", (form["train"].value,indexNum))
        else:
            t3 = (indexNum,form["train"].value)
            cur.execute('UPDATE labelIndex SET labelCount = ? WHERE labelID = ?',t3)
           
        #DBに単語を格納
        for w in wordBag:
            cur.execute("SELECT COUNT(*) FROM word WHERE word = ?",(w,))
            if(int(cur.fetchone()[0]) == 0):
                cur.execute("SELECT COUNT(*) FROM word")
                t3 = (int(cur.fetchone()[0]),w)
                cur.execute("INSERT INTO word VALUES(?,?)", t3)
                conn.commit()
                
        #学習データ保存
        for w in wordBag:
            cur.execute("SELECT COUNT(*) FROM trainData INNER JOIN word ON trainData.wordID = word.wordID WHERE trainData.labelID =:labelid AND word.word =:word",{'labelid':form["train"].value,'word':w})
            if(int(cur.fetchone()[0]) == 0):
                for row in cur.execute("SELECT * FROM word WHERE word = ?",(w,)):
                    t3 = (form["train"].value,int(row[0]),str(a.getList()[str(form["train"].value)][w]))
                    cur.execute('INSERT INTO trainData VALUES(?,?,?)',t3)
            else:
                for row in cur.execute("SELECT * FROM word WHERE word = ?",(w,)):
                    t3 = (str(a.getList()[str(form["train"].value)][w]),form["train"].value,int(row[0]))
                    cur.execute('UPDATE trainData SET count = ? WHERE labelID = ? AND wordID = ?',t3)       
            conn.commit()

        print("<br><br>")
        listUpdate()
        labelRe()
    #マルコフ連鎖用の学習データ
    if("mailText2" in form.keys()):
        t3 = (form["train2"].value,form["mailText2"].value)
        cur.execute("SELECT COUNT(*) FROM sendTrainData WHERE labelID = ?",(form["train2"].value,))
        if(int(cur.fetchone()[0]) == 0):
            cur.execute('INSERT INTO sendTrainData VALUES(?,?)', t3)
        else:
            t3 = (form["mailText2"].value,form["train2"].value)
            cur.execute('UPDATE sendTrainData SET text = ? WHERE labelID = ?', (t3))
        conn.commit()
        print("保存したよ")
    if("maru" in form.keys()):
        reply()
    else:
        if("train" in form.keys()):
            trainMain()
        if("train2" in form.keys()):
            trainMain2();
        if("getMail" in form.keys()):
            main();
    
    if("addLabel" in form.keys()):
        cur.execute('SELECT COUNT(*) FROM label')
        textNum = int(cur.fetchone()[0])
        t3 = (textNum,str(form["addLabel"].value))
        cur.execute('INSERT INTO label VALUES(?,?)', t3)
        conn.commit()
    #print("<button id = 'getMail'>メールの一括取得</button><br>")
def reply():
    select_sql = "SELECT * FROM sendTrainData WHERE labelID = ?"
    texts = ""
    for row in cur.execute(select_sql,(form["train"].value,)):
        texts += str(row[1])
    texts = Maru.maru(texts)
    print("""
    メール本文<br>""")
    print("""<br>
    <form name = "trainMailForm" method="POST" accept-charset="UTF-8" action='mail.py?trainMail=1'>""")
    recrlf = re.compile(r'\r\n')
    recr = re.compile(r'\r')
    print("<textArea name='mailText' rows = '20' cols = '50'>"+kaigyo(texts)+"</textArea><br>")
    print('<input type="hidden" name="train" value="'+str(form["train"].value)+'">')
    print("""<input type='submit' value = '送信（未実装）' id = 'submit'>
    
    </form>
    """)
def listUpdate():
    t2 = {}
    label = -1
    for row in cur.execute("SELECT * FROM trainData,word,label WHERE trainData.wordID = word.wordID AND trainData.labelID = label.labelID"):
        if(label!=int(row[5])):
            t3 = {}
            label = int(row[5])
        t3[str(row[4])]=(str(row[2]))
        t2[str(row[0])]=t3
    a.setList(t2)
    
def mail():
    print("<div id = 'mail'>")
    if("mailID" in form.keys()):
        for row in cur.execute("SELECT * FROM mailList WHERE mailID = ?",(form["mailID"].value,)):
            print(str(row[0])+"<br>")
            print(str(row[1])+"<br>")
            print(str(row[2])+"<br>")
            print(str(row[3]).replace('\r\n', '<br>')+"<br>")
        print("<br><a href= http://127.0.0.1:8000/cgi-bin/mail.py>戻る</a>")
        print("<br><a href= 'mail.py?maru=1&train="+str(row[5])+"'>返信</a>")
        print("<br>ラベルの付けなおし<br><select name='labels'>")
        for row in cur.execute("SELECT * FROM label"):
            print("<option value='"+str(row[0])+"'>"+str(row[1])+"</option>")
        print("</select>")
    else:
        labelRe()
        mailList()
    print("</div>")
    
def mailList():
    select_sql = """SELECT * FROM mailList
    INNER JOIN senderList ON mailList.senderID = senderList.senderID
    INNER JOIN label ON mailList.labelID = label.labelID
    """
    if("labelSelect" in form.keys()):
        select_sql += "WHERE label.labelID = ?"
        temp = cur.execute(select_sql,(int(form["labelSelect"].value),))
    else:
        temp = cur.execute(select_sql)
    print("<table>")
    print("<tr id = 'tableTop'>")
    print("<td>件名</td>")
    print("<td>日時</td>")
    print("<td>差出人</td>")
    print("<td>カテゴリ</td>")
    print("</tr>")
    
    for row in temp:
        a = "http://127.0.0.1:8000/cgi-bin/mail.py"+"?mailID="+str(row[0])
        print("<tr>")
        if(len(row[2])>24):
            print("<td><a href = '"+a+"'>"+row[2][:25]+"......</a></td>");
        else:
            print("<td><a href = '"+a+"'>"+row[2][:25]+"......</a></td>");
        print("<td><a href = '"+a+"'>"+row[1]+"</a></td>")
        print("<td><a href = '"+a+"'>"+str(row[7])+"</a></td>")
        print("<td><a href = '"+a+"'>"+str(row[9])+"</a></td>")
        print("</tr>")
    print("</table>")
        
def showMail(id):
    select_sql = ("SELECT * FROM mailList WHERE mailID = VALUES(?)",id)
    for row in cur.execute(select_sql):
        print(str(row[0]))
        print("<br>")

        
def getLabel():
    select_sql = "SELECT * FROM label"
    print("<div id = 'labels'>")
    print('<form method="GET" action="mail.py?addLabelFlag=1" accept-charset="utf-8">')
    print("ラベル<br>")
    for row in cur.execute(select_sql):
        print("<a href = mail.py?labelSelect="+str(row[0])+">");
        print(row[1]);
        print("</a><br>")
    print("<input type='text' id = 'addLabel' name = 'addLabel'><br>")
    print('<input type="submit" name="submit" id = "submit" value="ラベル追加" />')
    print("</form>")
    print("</div>")
    
def getTrainLabel():
    select_sql = "SELECT * FROM label"
    print("<div id = 'labels'>")
    print("ラベル一覧<br>")
    print('<form method="GET" action="mail.py?train=1" accept-charset="utf-8">')
    for row in cur.execute(select_sql):
        print(" ● <a href = mail.py?train="+str(row[0])+">"+str(row[1])+"</a>");
        print("<br>")

    print("</form></div>")
    
def getTrainLabel2():
    select_sql = "SELECT * FROM label"
    print("<div id = 'labels'>")
    print("ラベル一覧<br>")
    print('<form method="GET" action="mail.py?train2=2" accept-charset="utf-8">')
    for row in cur.execute(select_sql):
        print(" ● <a href = mail.py?train2="+str(row[0])+">"+str(row[1])+"</a>");
        print("<br>")
    print("</form></div>")
def trainMenu():
    print("""
    <a href = 'javaScript:treeMenu("trainMenu")'>学習</a><br><div id = trainMenu style = 'display:none'>
    """)
    getTrainLabel()
    print("""
    </div><hr><a href = 'javaScript:treeMenu("trainMenu2")'>送信データ用の学習</a><br><div id = trainMenu2 style = 'display:none'>
    """)
    getTrainLabel2()
    
def trainMain():
    select_sql = "SELECT * FROM trainMail WHERE labelID = ?"
    texts = ""
    for row in cur.execute(select_sql,(form["train"].value,)):
        texts += str(row[1])
    print("""
    <div id = 'trainMain'>
    <div id = 'mailData'>
    メール本文<br>""")
    
    print("""<br>
    <form name = "trainMailForm" method="POST" accept-charset="UTF-8" action='mail.py?trainMail=1'>""")
    recrlf = re.compile(r'\r\n')
    recr = re.compile(r'\r')
    print("<textArea name='mailText' rows = '20' cols = '50'>"+kaigyo(texts)+"</textArea><br>")
    print('<input type="hidden" name="train" value="'+str(form["train"].value)+'">')
    print("""<input type='submit' value = '保存' id = 'submit'>
    
    </form>
    </div>
    </div>
    """)

def trainMain2():
    select_sql = "SELECT * FROM sendTrainData WHERE labelID = ?"
    texts = ""
    for row in cur.execute(select_sql,(form["train2"].value,)):
        texts += str(row[1])
    print("""
    <div id = 'trainMain2'>
    <div id = 'mailData2'>
    メール本文<br>""")
    
    print("""<br>
    <form name = "trainMailForm" method="POST" accept-charset="UTF-8" action='mail.py?sendTrainData2=1'>""")
    recrlf = re.compile(r'\r\n')
    recr = re.compile(r'\r')
    print("<textArea name='mailText2' rows = '20' cols = '50'>"+kaigyo(texts)+"</textArea><br>")
    print('<input type="hidden" name="train2" value="'+str(form["train2"].value)+'">')
    print("""<input type='submit' value = '保存' id = 'submit'>
    
    </form>
    </div>
    </div>
    """)
    
def kaigyo(string):
    recrlf = re.compile(r'\r\n')
    recr = re.compile(r'\r')
    string = recrlf.sub(r'\n', string)
    string = recr.sub(r'\n', string)
    return string
    
def main():
    print ("Content-type: text/html\n\n")
    print("<html><head></head><body>")
    gmail = imaplib.IMAP4_SSL("imap.gmail.com")
    gmail.login("beiztest2","kuresamo")#ログイン
    gmail.select('INBOX') #受信ボックスを指定する
    #gmail.select() #ラベルを指定する
    
    #typ,[data] = gmail.search(None, "(UNSEEN)")
    typ, [data] = gmail.search(None, "(ALL)")
    
    mail = {}
    
    ##確認
    if typ == "OK":
        if data != '':
            print("New Mail")
        else:
            print("Non")
       
    #取得したメール一覧の処理
    for num in data.split():
        mailReadFlag = 1
        print(num)

        ### 各メールへの処理 ###
        result, d = gmail.fetch(num, "(RFC822)")
        raw_email = d[0][1]
        
        
        #文字コード取得用
        try:
            temp = raw_email.decode('iso-2022-jp')
        except:
            try:
                temp=raw_email.decode('utf-8')
            except:
                print("えらー")
                mailReadFlag = 0
                
        if(mailReadFlag):
            msg = email.message_from_string(temp)
            msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp'

            for a in msg.keys():
                print(a,msg[a])
            date = dateutil.parser.parse(msg.get('Date')).strftime("%Y/%m/%d %H:%M:%S")

            #print(date)
            mail["date"] = date

            subject = email.header.decode_header(msg.get('Subject'))
            title = ""
            for sub in subject:
                if isinstance(sub[0], bytes):
                    try:
                        title += sub[0].decode(msg_encoding)
                    except:
                        print("えらー")
                else:
                    title += sub[0]

            #print(title)
            mail["title"] = title
            
            
            senderTemp = email.header.decode_header(msg.get('From'))
            sender = ""
            for sub in senderTemp:
                if isinstance(sub[0], bytes):
                    try:
                        sender += sub[0].decode(msg_encoding)
                    except:
                        print("えらー")
                else:
                    sender += sub[0]

            #print(title)
            mail["sender"] = sender
            

            body = ""
            if msg.is_multipart():
                for payload in msg.get_payload():
                    if payload.get_content_type() == "text/plain":
                        body = payload.get_payload()
                        if msg_encoding == 'utf-8':
                            try:
                                body = base64.urlsafe_b64decode(body.encode('ASCII')).decode("utf-8")
                            except:
                                print("えらー")
            else:
                if msg.get_content_type() == "text/plain":
                    body = msg.get_payload()
                    print(msg_encoding)
                    if msg_encoding == 'utf-8':
                        try:
                            body = base64.urlsafe_b64decode(body.encode('ASCII')).decode("utf-8")
                        except:
                            print("えらー")
            #print(body)
            mail["content"] = body
            #cur.execute('SELECT COUNT(*) FROM mailList')
            #textNum = int(cur.fetchone()[0])
            #mail["num"] = textNum
            #print(mail)

            cur.execute('SELECT COUNT(*) FROM senderList WHERE mailAddress = ?',(mail["sender"],))
            if(int(cur.fetchone()[0]) == 0):
                cur.execute('INSERT INTO senderList(mailAddress) VALUES(?)',(mail["sender"],))
            cur.execute('SELECT senderID FROM senderList WHERE mailAddress = ?',(mail["sender"],))
            mail["senderID"] = cur.fetchone()[0]
            
            cur.execute('SELECT COUNT(*) FROM mailList WHERE date = ? AND title = ? AND content = ?',(mail["date"],mail["title"],mail["content"]))
            if(int(cur.fetchone()[0]) == 0):
                cur.execute('INSERT INTO mailList(date,title,content,senderID,labelID) VALUES(?,?,?,?,?)', (mail["date"],mail["title"],mail["content"],mail["senderID"],0))
            conn.commit()
            
    #お片付け
    gmail.close()
    gmail.logout()
#set()
#main()
print("<div id = 'main'>")
print("<div id = 'side'>")
print("<br><a href= http://127.0.0.1:8000/cgi-bin/mail.py?getMail=1>メールの一括取得</a>")
print("<hr>")

getLabel()
print("<hr>")
trainMenu()
print("</div>")
print("<div id = 'main2'>")
print("<h1>メール一覧</h1><hr>")
setup()
mail()
print("<hr>")
print("</div>")
print("</div>")