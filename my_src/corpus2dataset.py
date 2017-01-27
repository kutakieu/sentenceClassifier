import re
from os import listdir
from os.path import isfile, join
import MeCab

m = MeCab.Tagger("-Owakati")
punctuation = ["、","。","(",")","[","]","「","」","・","\n"," "]
#正規表現で句読点などを取り除く

remove_punctuation = re.compile('(\.(?![0-9]+)|、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|[0-9]+(?![0-9]+)|\,|#|＃|!)')#   '.'は少数点じゃない物だけ取り除く
remove_at = re.compile(r'(^＠.+\n|＠ＥＮＤ|％ｃｏｍ.*\n)')   #remove ＠参加者F107：女性３０代後半、愛知県幡豆郡出身、愛知県幡豆郡在住　AND　＠ＥＮＤ
remove_punctuation2 = re.compile(r'(＠|＊+|、|。|・)')   #remove punctuation
remove_ForM = re.compile(r'(F.+：|M.+：|Ｘ.*：)')   #remove F107：
remove_brackets = re.compile(r'(（.*）|＜.*＞|【.*】)')    #remove （うん、うん）＜笑い＞【地名】など
remove_FMxxx = re.compile(r'(F[0-9]{3}|M[0-9]{3})')     #remove F109さんは...などのF109
remove_alphabet = re.compile(r'[ａ-ｚＡ-Ｚ]+')     #remove A小学校...などのA

mypath_in = "/Users/tAku/Nextremer/nuc/"
mypath_out = "/Users/tAku/Nextremer/data/"
mypath_out_each_file_raw = "/Users/tAku/Nextremer/data/hanashi_kotoba_raw/"
mypath_out_each_file_modified = "/Users/tAku/Nextremer/data/hanashi_kotoba_modified/"

lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
        'shift_jis', 'shift_jis_2004','shift_jisx0213',
        'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
        'iso2022_jp_ext','latin_1', 'ascii')

filenames = [f for f in listdir(mypath_in) if isfile(join(mypath_in, f))]

dataset_name = "hanashi_kotoba_dataset.txt"
fout = open(mypath_out + dataset_name, "w", encoding = "utf-8")

count = 0
for filename in filenames:
     if re.search(".txt",filename) != None:
         for encoding in lookup:
             try:
                 fin = open(mypath_in + filename, encoding = encoding)
                 lines = fin.readlines()
                 fin.close()
                 print(filename + " : " + encoding)
                 fout_eachFile = open(mypath_out_each_file_modified + filename, "w", encoding = "utf-8")
                 #lines = remove_brackets.sub("",remove_punctuation2.sub(" ",remove_ForM.sub("",remove_at.sub("",lines))))
                 for line in lines:
                     line = remove_alphabet.sub("",remove_FMxxx.sub(" ",remove_brackets.sub("",remove_punctuation2.sub(" ",remove_ForM.sub("",remove_at.sub("",line))))))
                     morphemes = m.parse(line).split(' ')
                     for morpheme in morphemes:
                         if morpheme in punctuation:
                             continue;
                         else:
                             fout_eachFile.write(morpheme + ' ')
                             fout.write(morpheme + " ")

                 break
             except:
                 continue
