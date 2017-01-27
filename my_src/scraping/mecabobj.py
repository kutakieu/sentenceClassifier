'''
Created on 2016/08/16

@author: yuta.hayakawa
'''
import MeCab
tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')#bug用
fin = open('../../data/Verbutf.csv',encoding='utf-8')
lines = fin.readlines()
fin.close()
'''
morpheme
mecabのメタ情報を持った形態素を表現するクラス
オブジェクト指向的に情報にアクセスする。
各メタ情報については下記参照
http://taku910.github.io/mecab/#usage-tools

field

all:mecabをシェル上で起動した時と同様のStringを返す。
surface:文中で登場する形。MeCabのparseToNode().surfaceと同じ
feature:形態素の情報をまとめたもの。MeCabのparseToNode().featureと同じ
category:品詞
detail1:品詞細分類1
detail2:品詞細分類2
detail3:品詞細分類3
conjugtype:活用型
conjugation:活用形
original:原形
reading:読み
pronunciation:発音

'''
class morpheme:
    def __init__(self,surface,feature):
        self.all = surface + "\t" + feature
        self.surface = surface
        self.feature = feature
        feature = feature.split(',')
        self.category = feature[0]
        self.detail1 = feature[1]
        self.detail2 = feature[2]
        self.detail3 = feature[3]
        self.conjugtype = feature[4]
        self.conjugation = feature[5]
        self.base = feature[6]
        if len(feature) >7:
            self.reading = feature[7]
            self.pronunciation = feature[8]
        else:
            self.reading = self.pronunciation = "*"

    def conjugate(self,conj):
        for line in lines:
            if ','+self.base+',' in line and ','+self.conjugtype+',' in line and ','+conj+',' in line:
                self.surface = line.split(',')[0]
                self.conjugation = conj
                self.reading = line.split(',')[11]
                self.pronunciation = line.split(',')[12]
                return True
        return False
'''
mecabtxt

morphemeのリストとして、テキストを保持する。
listを継承しているため各morphemeにはindexでアクセスできる

field

text:テキストをそのまま返す
wakati:分かち書きをして返す

　
'''
class mecabtxt(list):
    def __init__(self,text):
        self.wakati = ''
        node = tagger.parseToNode(text)
        while node:
            if not node.surface in "":
                self.append(morpheme(node.surface,node.feature))
            node = node.next
    def text(self):
        txt = ''
        for mor in self:
            txt += mor.surface
        return txt

    def wakachi(self):
        wakati = ''
        for mor in self:
            wakati += mor.surface + " "
        return wakati

    def extend(self,txt):
        mors = mecabtxt(txt)
        for mor in mors:
            super().append(mor)
    def index(self,txt):
        i = 0
        for mor in self:
            if mor.surface in txt:
                return i
            i += 1
    def indexes(self,txt):
        i = 0
        indexes = []
        for mor in self:
            if mor.surface in txt:
               indexes.append(i)
            i += 1
        return indexes
    def insert(self,i,txt):
        mors = mecabtxt(txt)
        for mor in mors:
            super().insert(i,mor)
            i += 1
