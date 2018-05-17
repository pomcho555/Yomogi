# Yomogi

Python用の前処理用MeCabラッパーです。

## できること
-単語の統一
-記号・数字の除去
-分かち書き（形態素解析）
-ストップワードの除去
-特定の品詞の抽出
-レンマ化
-BoWのオブジェクトの作成

## できないこと
-ステミング
-単語の分散表現化
-日本語以外の言語処理  
***
## 前提条件
-Python3.5+
-mecab-python3
-Mecab
-mecab-ipadic-neologd

## Get Started,
`git clone https://github.com/pomcho555/Yomogi.git`
`cd <installed directory>`
`pip install -e .`

## BoWオブジェクトとは
BoW(Bag of Words)とは単語の袋の意で、単語とその頻度を格納したデータを指します。
BoWオブジェクトはBoW形式のデータを扱いやすくしたもので、BoWに対して和・差がとれます。
また、dict型とlist型の２つのデータ構造を持つので、柔軟に使えると思います。

## Quick Tutorial
-よもぎをimport
`import yomogi`
-文章のリストを作成
`text = ['よもぎの若葉を干しておいたのちに煎じて飲むと、健胃、腹痛、下痢、貧血、冷え性などに効果がありますよ。']`
-特定の品詞を抽出してそのリストをもらう(前処理付き）
`word_list = yomogi.extract(text, '名詞')`
-BoWオブジェクト化
`bow1 = yomogi.BoW(word_list)`
-BoWの中身をdict型で吐き出す
`print(bow1.bow)`
-BoWの中身をlist型で吐き出す
`print(bow1.sentences)`

***
## 謝辞
このプロジェクトは[nlp_jp_template](https://github.com/kazuhirokomoda/nlp_jp_template)のフォークプロジェクトです。
