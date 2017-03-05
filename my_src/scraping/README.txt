・Inflection2.py	
Wikipediaの同じページに飛ぶ単語群が各文章に入っている場合は ”⚪︎⚪︎って” を付けないようにしたInflectionするファイル。（表記ゆれに対応）
Wikipediaの同じページに飛ぶ単語群の作成方法は以下参照http://qiita.com/yukinoi/items/78d64aeb3afbaadf52b1


・extractFoodRedirects.py
上記の表記ゆれに対応した単語群をフードリストの中にある単語に対してのみ作成するためのファイル。

・easyScraping_onlyExacSameTopic.py
ページ名と検索名が一致する場合のみスクレイピングするためのファイル

・easyScraping_SameTopicANDsameSection.py
ページ名と検索名が同じものは全文スクレイピングする。ページ名と検索名が異なる場合は検索名がページ内のヘッダーに含まれているセクションからのみ文章を抽出する。
主にこれを使います。

・filter_randomSample.py
ほぼ変更は加えてない。

・new_filter4sentences.py
スクレイピングで<h1>と<概要>の見出し、その他の<h2>の各パラグラフの一行目を取ってくる場合にフィルタリングを必要最低限にするために用意したファイル。
この方法でスクレイピングして、かつフィルタリングを強めたものを試してみるべきでした。


・putId4rawWikidata.py				
抽出してきた生のテキストデータにそれぞれのヘッダーの順番と種類、各見出し内でのパラグラフの順番、各パラグラフ内でのセンテンスの順番をIDとして付与するためのファイル。


・scrapingWiki.py

	

・mecabobj.py