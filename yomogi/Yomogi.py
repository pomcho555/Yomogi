"""
This module is MeCab-Wrapper or other POS analyzer for python3.
It makes you ease some tasks on text-processing.
text: take text-type argument following: "Gorge got an apple from a tall tree."
word_list: take list-type argument following: ['apple','orange']
sentences: take list-type argument follwing: ['これはテストです。\n', 'テストのため、文章は短いです。\n']
"""

#Here is public modules
__all__ = ['BoW','separate', 'extract', 'normalize','convert_to_sentences']


class Word():
    def __init__(self, text, POS):
        self.text, self.POS = text, POS

    def __eq__(self, target_word):
        return self.text == target_word.text

    def __add__(self,target_word):
        return self.text + target_word.text


class Word_group():
    def __init__(self):
        self.matrix = {}
        self.word_list = []

    def add_word(self, word):
        if word.text in self.matrix:
            self.matrix = self.matrix.get(word.text, 0) +1
        else:
            self.matrix.update({word.text:{'POS':word.POS,'Cnt':1}})
        #self.word_list.append

    def add_words(self,words):
        words = _filter_list(words)
        for word in words:
            word_object  = Word(word,'名詞')
            self.add_word(word_object)

    def __eq__(self, target_group):
        return self.matrix == target_group.matrix

    def _filter_list(words):
        if isinstance(words[0], list):
            words = [y for x in words for y in x]
        return words

def _count(sentences):
    """
    create BoW
    input 1 or 2-dim list
    """
    bow = {}
    for word in sentences:
        bow[word] = bow.get(word, 0) + 1
    return bow

def _filter_list(sentences):
    if isinstance(sentences[0], list):
        sentences = [y for x in sentences for y in x]
    return sentences

def _assign(bow: dict) -> dict:
    #bowの数だけ単語を複製しないとだめ
    sentences = []
    for word in bow:
        sentences.append([word] * bow.get(word))
    return _filter_list(sentences)


class BoW():
    def __init__(self ,*arg):
        if not arg:
            """make empty BoW object"""
            self.bow = {}
            self.sentences = []
        elif type(arg[0]) == list:
            sentences = _filter_list(arg[0])
            self.sentences = sentences
            self.bow = _count(sentences)
        elif type(arg[0]) == dict:
            self.bow = arg[0]
            self.sentences = _assign(arg[0])



    def __add__(self,target_BoW):
        #excute deep copy to copy dict type object
        import copy
        a = copy.deepcopy(self.sentences)
        b = copy.deepcopy(target_BoW.sentences)
        c=a+b
        #new_bow = BoW(c)
        return BoW(c)

    def __sub__(self,target_BoW):

        try:
            import copy
            a = copy.deepcopy(self.bow)
            b = copy.deepcopy(target_BoW.bow)
            if(len(a)<len(b)):raise TypeException
        except TypeException:
            print('substracted argument must be smaller')
        c={}
        for x in a:
            if x in b:
                if a[x]-b[x]>0:
                    c.update({x:a[x]-b[x]})
                else:
                    pass
        #new_bow = BoW(c)
        return BoW(c)


def separate(sentences):
    pass

def extract(sentences, POS):
    """
    POS:a list of parts of sppech you want to extract
    ex:["名詞","動詞"]
    return 2-dim list, follwing this: [['テスト'], ['テスト', '文章'], ['人生']]
    """
    documents_divided = []
    from yomogi.word_divider import WordDivider
    wd = WordDivider(is_normalize=True, remove_stopwords=True)
    wd.TARGET_CATEGORIES = POS
    documents_divided = []
    for a_line in sentences:
        documents_divided.append(wd.extract_words(a_line))
    return documents_divided

def normalize(sentences: list) -> list:
    from normalize_neologd import normalize_neologd
    return normalize_neologd(sentences)

def convert_to_sentences(text: str) -> str:
    import re
    sentences = re.split('[.。]', text)
    return sentences



if __name__ == '__main__':
    text_path_train_test = 'data/simple.txt'
    from word_divider import make_documents_from_file
    documents = make_documents_from_file(text_path_train_test)
    extracted_list=extract(documents,'名詞')
    bow_test = BoW(extracted_list)
    print(bow_test.bow)
    w_list = [['テスト'], ['テスト', '文章'], ['人生']]
    bow1 = BoW(w_list)
    bow2 = BoW(w_list)
    assert {'テスト':4, '文章':2, '人生':2} == (bow1+bow1).bow
    bow100 = BoW({'テスト':4, '文章':1, '人生':1})
    print(bow100.bow)
    print(bow100.sentences)
    bow3 = BoW()
    for x in range(2):
        bow3 += bow1
    assert {'文章': 2, 'テスト': 4, '人生': 2} == bow3.bow
