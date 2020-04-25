import sqlite3
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)

conn = sqlite3.connect("data.db")
cur = conn.cursor()
select_sql = "SELECT name,image,text,mediaID FROM tweet,user WHERE tweet.userID = user.userID"
for row in cur.execute(select_sql):
    print(row[0]+"<br>")
    print("<img src = '"+row[1]+"'>")
    print(row[2])
    print(row[3])
    if(row[3]!=-1):
        img_sql = "SELECT * FROM image WHERE image.id = "+ str(row[3])
        print(img_sql)
        cur2 = conn.cursor()
        for r in cur2.execute(img_sql):
            print("huuu")
            break;
        print("")
    print("<br>")
