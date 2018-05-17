# -*- coding: utf-8 -*-

# imports
import MeCab
from urllib.request import urlopen

# local imports
from yomogi.normalize_neologd import *

"""
WordDivider: Divide Japanese into words
ref. http://tyamagu2.xyz/articles/ja_text_classification/
ref. http://testpy.hatenablog.com/entry/2016/10/05/004949
"""

class WordDivider:
    INDEX_CATEGORY = 0
    INDEX_SUB_CATEGORY = 1
    INDEX_ROOT_FORM = 6
    TARGET_CATEGORIES = ["名詞"] #["名詞", "動詞", "形容詞", "副詞", "連体詞", "感動詞"]
    REMOVE_SUB_CATEGORIES = ["非自立"]

    def __init__(self, dictionary="mecabrc", is_normalize=False, remove_stopwords=False):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)
        self.tagger.parse("")
        self.is_normalize = is_normalize
        self.stopwords = []
        self.remove_stopwords = remove_stopwords


    def set_stopwords(self):
        slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
        slothlib_file = urlopen(slothlib_path)
        slothlib_stopwords = [line.decode("utf-8").strip() for line in slothlib_file]
        slothlib_stopwords = [ss for ss in slothlib_stopwords if not ss==u'']
        return slothlib_stopwords


    def extract_words(self, text):
        if not text:
            return []

        if self.remove_stopwords:
            self.stopwords = self.set_stopwords()

        words = []
        tmp_append = {'POS': '', 'surface':''}
        # normalize text before MeCab processing
        if self.is_normalize:
            text = normalize_neologd(text)

        node = self.tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')
            print(features)
            #print(tmp_append)
            if features[self.INDEX_CATEGORY] in self.TARGET_CATEGORIES and features[self.INDEX_SUB_CATEGORY] not in self.REMOVE_SUB_CATEGORIES:
                if features[self.INDEX_ROOT_FORM] == "*":
                    word_to_append = node.surface
                else:
                    #combine two words to compounds
                    if tmp_append['POS'] == '名詞':
                        print('pass')
                        try:
                            del(words[-1])
                        except IndexError:
                            print(words,'cause KeyError')
                        word_to_append = tmp_append['surface'] + node.surface
                        print(word_to_append)
                    else:
                        # prefer root form
                        word_to_append = features[self.INDEX_ROOT_FORM]

                # remove stopwords
                if not self.remove_stopwords or word_to_append not in self.stopwords:
                    words.append(word_to_append)
            tmp_append.update({'POS':features[self.INDEX_CATEGORY],'surface':node.surface})
            node = node.next

        return words


def make_documents_from_file(file_path):
    documents = []
    with open(file_path, encoding='utf-8') as a_file:
        for a_line in a_file:
            documents.append(a_line)
    return documents


text_path_train_test = 'data/train_test_simple.txt'
text_path_train_test = 'data/simple.txt'


if __name__ == '__main__':

    documents = make_documents_from_file(text_path_train_test)
    #assert ['これはテストです。\n', 'テストのため、文章は短いです。\n', '人生は何かを成し遂げるにはあまりにも短い。\n'] == documents

    wd = WordDivider(is_normalize=True, remove_stopwords=True)
    documents_divided = []
    with open(text_path_train_test, encoding='utf-8') as a_file:
        for a_line in a_file:
            documents_divided.append(wd.extract_words(a_line))
            print(documents_divided)
    #assert [['テスト'], ['テスト', '文章'], ['人生']] == documents_divided
    print('divide')
    print(documents_divided)
    from yomogi.Yomogi import BoW
    BoW = BoW(documents_divided)
    print(BoW.bow)
