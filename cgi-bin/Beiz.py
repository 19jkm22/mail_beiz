import MeCab
import math
import re
class Beiz:
    def __init__(self):
        self.count = 0 #訓練データ数
        self.indexNum = {} #訓練したカテゴリの、各カテゴリの数をカウント
        self.list = {} #カテゴリと、そのカテゴリで出現した各ワードの回数
        self.list2 = {}
        
    def setIndexNum(self,label,num):
        self.indexNum[str(label)] = num
        self.count = 0
        for a in self.indexNum.keys():
            self.count += int(self.indexNum[str(a)])
        #print("合計学習数:",self.count)
    def setIndexList(self,list):
        self.indexNum = list
    def getList(self):
        return self.list;
    def setList(self,list):
        self.list = list
    def resetLabel(self,label):
        self.list[label] = {}
    def getList2(self,words):
        for w in words:
            list[w] = 1 + list[w]
        return list
        
    def train(self,cat,words):#学習
        if(not cat in self.list.keys()):
            self.list[cat] = {}
        for word in words:
            if (not word in self.list[cat]):
                self.list[cat].update({word:"0"})
            self.list[cat][word] = str(int(self.list[cat][word])+1)
        self.count+=1
        if(not cat in self.indexNum):
            self.indexNum[cat] = 0#カテゴリが辞書内になかったら新規作成
        self.indexNum[cat] += 1 #カテゴリ出現回数を＋１
        #print(self.list)
        #print(self.indexNum)
        
    def p_cat(self,cat):
        if(self.indexNum[cat]/self.count==0):return 0
        return math.log(self.indexNum[cat]/self.count)
        
    def p_word_i_cat(self,word,cat):
        num = len(self.list[cat])
        #num = 0
        v = 0
        for a in self.list.values():
            num += len(a)
            
        if(not word in self.list[cat]):#カテゴリ内にワードが存在しなかったら分子を１にして無理矢理返す
            v = 1
            return v/num
        else:
            v = int(self.list[cat][word])+1#＋１する
            return v/num
        
    def p_doc_cat(self,cat,words):
        #num = 1
        num = 0
        for word in words:
            #num *= self.p_word_i_cat(word,cat)
            #logを取った時は掛け算が足し算になる...???????
            num +=  math.log(self.p_word_i_cat(word,cat))
        return num
    def kaigyo(self,string):
        recrlf = re.compile(r'\r\n')
        recr = re.compile(r'\r')
        string = recrlf.sub(r'\r\n', string)
        string = recr.sub(r'\r\n', string)
        return string
    
    def beiz(self,words):
        ncat = -10000 #初期値 単語数が増えるともっと小さくないとだめかも
        tcat = ""
        for cat in self.list.keys():
            #temp = self.p_cat(cat) * self.p_doc_cat(cat,words)
            temp = self.p_cat(cat) + self.p_doc_cat(cat,words)
            #print(cat+":"+str(temp)+"\n")
            if(temp>ncat):
                ncat = temp
                tcat = cat
        #print(tcat)
        #print("<br>")
        return tcat
        
    def mm(self,temp):#名詞とか動詞とかぬきとり
        mt = MeCab.Tagger("")
        m2 = mt.parse(temp).split("\n")
        list = []
        for s in m2:
            if(len(s.split("\t"))>1):
                if("名詞" in s.split("\t")[1] or ("動詞" in s.split("\t")[1]) and ("自立" in s.split("\t")[1]) or ("形容詞" in s.split("\t")[1])):
                   list.append(s.split("\t")[0])
        return list
        
"""
a = Beiz()
import MeCab
import math
import sys
files = ["orei","oiwai","taisha","tuuti","owabi","chuui","shoudaku"]
for fil in files:
	f = open(fil+".txt")
	line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
	mail = ""
	while line:
	    mail+=line
	    line = f.readline()
	    if("^" in line):
	    	#print(mail)
	    	a.train(fil,a.mm(mail))
	    	mail = ""
	f.close
while 1:
	print("推定したい文章を入力してね")
	temp = ""
	temp2 = ""
	while temp2 != "END":
		temp2 = input()
		temp = temp+temp2
	print("推定されたカテゴリ："+a.beiz(a.mm(temp)))
	##print(a.mm(temp))
print("")

temp = input()
while temp != "END":
    print("カテゴリ名")
    a.train(input(),a.mm(temp))
    temp = input()
temp = input()
while temp != "END":
    print("推定したい文章を入力してね")
    temp = input()
    print("推定されたカテゴリ："+a.beiz(a.mm(temp)))
    print(a.mm(temp))

"""