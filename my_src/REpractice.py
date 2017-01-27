import MeCab
import re

#punctuation = ["、","。","(",")","[","]","「","」","・"]

punctuation = [r'、*', r'。*', r'(*', r')*', r'[*', r']*', r'「*', r'」*', r'・*']

m = MeCab.Tagger("-Owakati")
#text = "「出汁」、タレ、香味油の3要素から成るスープ料理としての側面（そくめん）も大きい。円周率は3.14である。漢字表記は拉麺、老麺[2]または柳麺。別名は中華そばおよび支那そば・南京そば[31][4]などである(うそ!)。"
text = "＠参加者の関係：英会話教室の友人\nF107：＊＊＊の町というのはちいちゃくって、城壁がこう町全体をぐるっと回ってて、それが城壁の上を歩いても１時間ぐらいですよね。\nF023：１時間かからないぐらいだね。\n＜笑い＞\nF107：ほいであちしなんかとびつかれちゃったよ。\nＸ：うそ。\n＜笑い＞（はー）\n＠ＥＮＤ"
print(text)
print("\n\n")
#text = re.sub(r'\[[0-9]\]',r'',text)
#[数字]　を取り除く
#remove_squareBracket = re.compile(r'\[[0-9]*\]')
#text = remove_squareBracket.sub("",text)
#print(text)

#remove_punctuation = re.compile(r'(、' | '。)')
# remove_punctuation = re.compile('(、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|\.(?![0-9]+)|\,|#|＃|!)')
#remove_punctuation = re.compile('(、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|\.(?![0-9]+)|\,|#|＃|!)')
#remove_punctuation = re.compile('(\.(?![0-9]+)|、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|[0-9]+(?![0-9]+)|\,|#|＃|!)')#   '.'は少数点じゃない物だけ取り除く
remove_at = re.compile(r'(^＠.+\n|＠ＥＮＤ|％ｃｏｍ.*\n)')   #remove ＠参加者F107：女性３０代後半、愛知県幡豆郡出身、愛知県幡豆郡在住　AND　＠ＥＮＤ　AND ％ｃｏｍ
remove_punctuation2 = re.compile(r'(＠|＊+|、|。)')   #remove punctuation
remove_ForM = re.compile(r'(F.+：|M.+：|Ｘ.*：)')   #remove F107：
remove_FMxxx = re.compile(r'(F[0-9]{3}|M[0-9]{3})')     #remove F109さんは...などのF109
remove_brackets = re.compile(r'(（.*）|＜.*＞)')    #remove （うん、うん）＜笑い＞
remove_alphabet = re.compile(r'[A-Z](?![A-Za-z]+)')     #remove A小学校...などのA



# text = remove_at.sub("", text)
# text = remove_ForM.sub("", text)
# text = remove_punctuation2.sub(" ", text)
# text = remove_brackets.sub("",text)
text = remove_brackets.sub("",remove_punctuation2.sub(" ",remove_ForM.sub("",remove_at.sub("",text))))

print(text)

morphemes = m.parse(text).split(' ')

mypath_out = "/Users/tAku/Nextremer/data/"
path = "/Users/tAku/Nextremer/data/hanashi_kotoba_raw/data002.txt"

fin = open(path, encoding = "utf-8")
text = fin.readlines()
# text = remove_at.sub("", text)
# text = remove_ForM.sub("", text)
text = remove_punctuation2.sub(" ", text)
# text = remove_brackets.sub("",text)
# lines = remove_brackets.sub("",remove_punctuation2.sub(" ",remove_ForM.sub("",remove_at.sub("",lines))))
for line in text:
    #line = remove_punctuation2.sub(" ", line)
    print(line)
