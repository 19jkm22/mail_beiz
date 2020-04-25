from requests_oauthlib import OAuth1Session

import cgi
form = cgi.FieldStorage()

CK = 'KU12BvEYzuZmyiXV2Qek4aiDk'                             # Consumer Key
CS = 'dDJuhRScCFoP6yuAW76uLoB4oXTdVRH87NDVBUKXNKSmgJiVa9'         # Consumer Secret
AT = '522047290-rK549hzmCz0FBnNxaSORZvTburiAhbbS9Kkh5u95' # Access Token
AS = 'VPXBRbiRqAIMJ55OK0wnG4rbwxZzU0Jscx9vyR6XaroVV'         # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

# ツイート本文
params = {"status": form["foo"].value}

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.post(url, params = params)

print ("Content-type: text/html\n\n")
print("<html><head></head><body>")

# レスポンスを確認
if req.status_code == 200:
    print ("OK")
else:
    print ("Error: %d" % req.status_code)