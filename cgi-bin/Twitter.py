import cgi
from requests_oauthlib import OAuth1Session
import json
import MeCab
import sqlite3
import io, sys
class Twitter:
    def getTweet(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)
        form = cgi.FieldStorage()
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        input = ""


        CK = 'KU12BvEYzuZmyiXV2Qek4aiDk'                             # Consumer Key
        CS = 'dDJuhRScCFoP6yuAW76uLoB4oXTdVRH87NDVBUKXNKSmgJiVa9'         # Consumer Secret
        AT = '522047290-rK549hzmCz0FBnNxaSORZvTburiAhbbS9Kkh5u95' # Access Token
        AS = 'VPXBRbiRqAIMJ55OK0wnG4rbwxZzU0Jscx9vyR6XaroVV'         # Accesss Token Secert

        # タイムライン取得用のURL
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

        # とくにパラメータは無い
        params = {'count':200}

        # OAuth で GET
        twitter = OAuth1Session(CK, CS, AT, AS)
        req = twitter.get(url, params = params)

        #ツイートの取得
        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            timeline = json.loads(req.text)

            # 各ツイートの本文を表示
            for tweet in timeline:
        
                #print(tweet)
                id = tweet["id_str"]
                cur.execute('SELECT COUNT(*) FROM tweet WHERE id = ?', (id,))
                if(cur.fetchone()[0] != 0):
                    continue
        
                #print(tweet["user"]["name"])
                #ユーザの情報を取得
                userID = tweet["user"]["id_str"]
                name = tweet["user"]["name"]
                user_img = tweet["user"]["profile_image_url"]
                cur.execute('SELECT COUNT(*) FROM user WHERE userID = ?', (userID,))
        
                if(cur.fetchone()[0] == 0):#登録されてないユーザなら登録
                    t2 = (userID,name,user_img)
                    cur.execute('INSERT INTO user VALUES(?,?,?)', t2)
        
                #print("<br>")
                #print("<img src = '"+tweet["user"]["profile_image_url"]+"' width = '45'>")
                #print(tweet["text"])
                input += tweet["text"]
        
                if("extended_entities" in tweet):
                    cur.execute('SELECT COUNT(*) FROM image')
                    imageID_key = cur.fetchone()[0]
                else:
                    imageID_key = -1
        
                #画像の情報を取得
                if("extended_entities" in tweet):
                    for img_url in tweet["extended_entities"]["media"]:
                        imageURL = img_url["media_url"]
                        imageID = img_url["id_str"]
                        t = (imageID_key,imageID,imageURL)
                        cur.execute('INSERT INTO image VALUES(?,?,?)', t)
                        #print("<br>"+"<img class = 'image_s' src = '"+img_url["media_url"]+"' width = '250'>")
                print("<br>")
                tweetText = tweet["text"]
        
                #print(imageID_key)
                t3 = (id,userID,tweetText,imageID_key)
                cur.execute('INSERT INTO tweet VALUES(?,?,?,?)', t3)
            conn.commit()

        else:
            # エラーの場合
            print ("Error: %d" % req.status_code)