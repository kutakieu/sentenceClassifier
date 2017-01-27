import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import re
import MeCab
from os import listdir
from os.path import isfile, join

ssl._create_default_https_context = ssl._create_unverified_context

template = ["トーク","投稿記録","アカウント作成","ログイン","ページ","ノート","閲覧","履歴表示","メインページ","コミュニティ・ポータル","最近の出来事","新しいページ","最近の更新","おまかせ表示","練習用ページ","アップロード (ウィキメディア・コモンズ)","ヘルプ","井戸端","お知らせ","バグの報告","寄付","ウィキペディアに関するお問い合わせ","ブックの新規作成","PDF 形式でダウンロード","印刷用バージョン","コモンズ","リンク元","関連ページの更新状況","ファイルをアップロード","特別ページ","この版への固定リンク","ページ情報","ウィキデータ項目","このページを引用","العربية","Asturianu","Azərbaycanca","Žemaitėška","Беларуская","Български","Brezhoneg","Català","Čeština","Cymraeg","Dansk","Deutsch","English","Esperanto","Español","Eesti","Euskara","فارسی","Suomi","Français","Galego","עברית","हिन्दी","Հայերեն","Bahasa Indonesia","Íslenska","Italiano","Basa Jawa","ಕನ್ನಡ","한국어","Latina","Limburgs","Lietuvių","Македонски","Bahasa Melayu","Nederlands","Norsk bokmål","Polski","Português","Русский","Scots","Sámegiella","Slovenčina","Svenska","Tagalog","Türkçe","Українська","Tiếng Việt","中文","粵語","リンクを編集","個人設定","UTC","クリエイティブ・コモンズ 表示-継承ライセンス","利用規約","プライバシー・ポリシー","ウィキペディアについて","免責事項","開発者","Cookie statement","モバイルビュー","案内","検索","検証可能","参考文献や出典","出典を追加","編集","英語版","表","話","編","歴"]

# print(template)
wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger("-Ochasen")
#正規表現で[数字]の引用部分を取り除く
remove_squareBracket = re.compile(r'\[.*?\]')
remove_brackets = re.compile(r'(（.*）|\(.*?\))')
#正規表現で句読点などを取り除く
# remove_punctuation = re.compile('(\.(?![0-9]+)|、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|[0-9]+(?![0-9]+)|\,|#|＃|!|:|\'|\")')#   '.'は少数点じゃない物だけ取り除く
remove_punctuation = re.compile('(、|。|・|（|）|「|」|『|』|[|]|\(|\)|/|\\|[0-9]+(?![0-9]+)|\,|#|＃|!|:|\'|\")')#   '.'は少数点じゃない物だけ取り除く

# ----main routine----

start = time.time()
lists = []
# 読み込むファイル記述してください(空白行終わりで)
# fin = open("../data/food.txt" , encoding = "utf-8")
path2files = "/Users/tAku/Nextremer/mecab_dictionary/foodLists_copy/"
files = [f for f in listdir(path2files) if isfile(join(path2files, f))]
# for _file in ["/Users/tAku/Nextremer/data/foodList.txt"]:
#     if re.search(".txt",_file) != None:
#         print(_file)
#         list_tmp = []
#         food_list = open(path2files + _file, encoding="utf-8")
#         #list_tmp = food_list.readlines().split('\n')
#         lists.append(food_list)
# for _list in lists:
#     for food in _list:
#         print(food.replace('\n',""))
# exit()

punctuation = ["、","。","(",")","[","]","「","」","・"]
# outputのパス記述してくださいs
# fnot = open("/Users/tAku/Nextremer/mecab_dictionary/foodLists/notFoundList.txt" , "w" , encoding = "utf-8")
temp = []
words2search = []
i = 0
count = 1
opener = urllib.request.build_opener()
file4dataset = open("/Users/tAku/Nextremer/data/dataset.txt", "w", encoding="utf-8")
for _file in ["/Users/tAku/Nextremer/data/foodList.txt"]:
    if re.search(".txt",_file) != None:
        fin = open(_file, encoding="utf-8")
        print(_file)
        lines = fin.readlines()
        for line in lines:
            line = line[:-1]    # 最後の文字(改行)を取る
            u = "https://ja.wikipedia.org/wiki/" + urllib.parse.quote(line.encode("utf-8"))
            try:
                opener.open(u)
                print(line)
            except Exception as e:
                print(line + " is not found")
                continue

            # outputのパス記述してください
            # fou = open('../data/wikidata_copy/'+line + '.txt','w', encoding = 'utf-8')
            count = count + 1
            html = opener.open(u).read()
            soup = BeautifulSoup(html, "lxml")

            text = soup.findAll(("p", "dd", "a")) # 指定タグ内のテキスト全てをリスト格納
            if line != (soup.title.string.split(" ")[0]): # ページのタイトルと検索語が一致するか確認
                 print(soup.title.string.split(" ")[0] + "|" + line + ":トピックと検索語が異なります")

            #ページ内のリンクもcorpusに追加する場合
            # for part in text:
            #     if part.name in "a":
            #         lines = part.get_text().split("\n")
            #         for line in lines:
            #             # リンクのある句をtempに追加する（tempにまだ含まれてなくて、スペースなどでもなく、templateに含まれる句でない場合）
            #             if line in temp or line in [""," ", "　", "\n"] or line in template:
            #                 continue
            #             else:
            #                 temp.append(line)

            for part in text:
                if part.name in ["p", "dd"]:
                    lines = part.get_text()
                    lines = remove_squareBracket.sub("",lines)
                    lines = remove_brackets.sub("",lines)
                    lines = remove_punctuation.sub(" ", lines)
                    #wikiから抽出してきた文章の中にtempに追加した句が含まれている場合のみその句を正式に新たに追加検索する句として追加する。
                    for line in temp:
                        if line in lines and line not in words2search:
                            #この新しい句の候補がもともとのfood list に含まれているかを調べる。
                            flag = False
                            for _list in lists:
                                if line in _list:
                                    flag = True
                                    break
                            if flag == False:
                                words2search.append(line)

                    for line in lines.split("\n"):
                        morphemes = wakati.parse(line).split(' ')
                        for morpheme in morphemes:
                            file4dataset.write(morpheme + " ")
        fin.close()
    # break
# print("\n\nsearch new words. total : " + str(len(words2search)) + " words\n\n")
# for new_word in words2search:
#     u = "https://ja.wikipedia.org/wiki/" + urllib.parse.quote(new_word.encode("utf-8"))
#     try:
#         opener.open(u)
#         print(new_word)
#     except Exception as e:
#         print(new_word + " is not found")
#         continue
#     html = opener.open(u).read()
#     soup = BeautifulSoup(html, "lxml")
#     text = soup.findAll(("p", "dd")) # 指定タグ内のテキスト全てをリスト格納
#     if new_word != (soup.title.string.split(" ")[0]): # ページのタイトルと検索語が一致するか確認
#          print(soup.title.string.split(" ")[0] + "|" + new_word + ":トピックと検索語が異なります")
#     for part in text:
#         if part.name in ["p", "dd"]:
#             lines = part.get_text()
#             lines = remove_squareBracket.sub("",lines)
#             lines = remove_brackets.sub("",lines)
#             lines = remove_punctuation.sub(" ", lines)
#
#             for line in lines.split("\n"):
#                 morphemes = wakati.parse(line).split(' ')
#                 for morpheme in morphemes:
#                     file4dataset.write(morpheme + " ")

file4dataset.close()
f_newWords = open("../data/new_words.txt", "w", encoding="utf-8")
count = 0
for line in words2search:
    f_newWords.write(line+"\n")
    count += 1
    # print(line)
print(count)
elapsed_time = time.time() - start
print("ElapsedTime:" + str(elapsed_time) + "[sec]")
