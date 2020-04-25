import imaplib, re, email, six, dateutil.parser
import pykf
import dateutil.parser
import base64
import io, sys
import sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                          encoding=sys.stdout.encoding, 
                          errors='backslashreplace', 
                          line_buffering=sys.stdout.line_buffering)
email_default_encoding = 'iso-2022-jp'

def setLabel():

def getLabel():
    conn = sqlite3.connect("mail.db")
    cur = conn.cursor()
    select_sql = "SELECT label FROM label ORDER BY labelID"
    print ("Content-type: text/html\n\n")
    print("<html><head></head><body>")
    for row in cur.execute(select_sql):
        print(row[0]);

def main():
    print ("Content-type: text/html\n\n")
    print("<html><head></head><body>")
    gmail = imaplib.IMAP4_SSL("imap.gmail.com")
    gmail.login("klsm.mum","kuresamo")
    gmail.select('INBOX') #受信ボックスを指定する
    #gmail.select() #ラベルを指定する
    
    #typ,[data] = gmail.search(None, "(UNSEEN)")
    typ, [data] = gmail.search(None, "(ALL)")
    
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

            print(date)

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

            print(title)

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
            print(body)
            print('')
    #お片付け
    gmail.close()
    gmail.logout()

getLabel();