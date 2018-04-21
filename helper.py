#coding:utf-8
import os,sys
import pickle
import jieba
def init():
    print('Hello World!')

def create_lookup_tables(input_data):
    vocab = set(input_data)
    # 文字到数字的映射
    vocab_to_int = {word: idx for idx, word in enumerate(vocab)}
    # 数字到文字的映射
    int_to_vocab = dict(enumerate(vocab))
    return vocab_to_int, int_to_vocab


def token_lookup():
    symbols = ['。', '，', '“', "”", '；', '！', '？', '（', '）', '——', '\n']
    tokens = ["P", "C", "Q", "T", "S", "E", "M", "I", "O", "D", "R"]
    return dict(zip(symbols, tokens))

def load_data():
    path = "dataset"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            with open(path + "/" + file) as fin:
                for line in fin:
                    line = line.strip()
                    if len(line) > 0 and line.find(u'作曲') == -1 and line.find(u'作词') == -1:
                        seg_list = jieba.cut(line, cut_all=True, HMM=False)
                        for c in seg_list:
                            s.append(c)
                        s.append('#')
                s.append('$')
    print("load done!")
    #print(seg_list)
    #print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    #s = str(s).decode('string_escape')
    #print(list(s[:10]))
    return s

def preprocess_and_save_data(text, token_lookup, create_lookup_tables):
    token_dict = token_lookup()

    #for key, token in token_dict.items():
    #    text = text.replace(key, '{}'.format(token))

    vocab_to_int, int_to_vocab = create_lookup_tables(text)
    for c in int_to_vocab:
        print(int_to_vocab[c])
    #print(int_to_vocab)
    int_text = [vocab_to_int[word] for word in text]

    pickle.dump((int_text, vocab_to_int, int_to_vocab, token_dict), open('preprocess.p', 'wb'))


def load_preprocess():
    return pickle.load(open('preprocess.p', mode='rb'))


def save_params(params):
    pickle.dump(params, open('params.p', 'wb'))


def load_params():
    return pickle.load(open('params.p', mode='rb'))

if __name__ == '__main__':
    s = load_data()
    preprocess_and_save_data(s, token_lookup, create_lookup_tables)