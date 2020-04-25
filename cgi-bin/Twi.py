import cgi
from requests_oauthlib import OAuth1Session
import json
import MeCab
import re
import sqlite3
import io, sys
class Twi:
    def getTweet(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)
        form = cgi.FieldStorage()
        conn = sqlite3.connect("data2.db")
        cur = conn.cursor()
        input = ""


        CK = 'KU12BvEYzuZmyiXV2Qek4aiDk'                             # Consumer Key
        CS = 'dDJuhRScCFoP6yuAW76uLoB4oXTdVRH87NDVBUKXNKSmgJiVa9'         # Consumer Secret
        AT = '522047290-rK549hzmCz0FBnNxaSORZvTburiAhbbS9Kkh5u95' # Access Token
        AS = 'VPXBRbiRqAIMJ55OK0wnG4rbwxZzU0Jscx9vyR6XaroVV'         # Accesss Token Secert

        # タイムライン取得用のURL
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

        # とくにパラメータは無い
        params = {'count':10}

        # OAuth で GET
        twitter = OAuth1Session(CK, CS, AT, AS)
        req = twitter.get(url, params = params)
        cur.execute('SELECT COUNT(*) FROM text')
        textNum = cur.fetchone()[0]
        #ツイートの取得
        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            timeline = json.loads(req.text)
            mt = MeCab.Tagger("-Owakati")
            # 各ツイートの本文を表示
            for tweet in timeline:
                tweetText = "start"+re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+',"",tweet["text"])
                m2 = mt.parse(tweetText).split(" ")#文を分かち書きする
                num = 0
                if(len(m2) > 3):
                    while num+2 < len(m2):
                        t3 = (textNum,m2[num],m2[num+1],m2[num+2])
                        cur.execute('INSERT INTO text VALUES(?,?,?,?)', t3)
                        print(t3)
                        textNum+=1
                        num+=1
                
            conn.commit()

        else:
            # エラーの場合
            print ("Error: %d" % req.status_code)