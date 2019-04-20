import jieba
import jieba.analyse
import re
from string import digits

# 定义文件目录
f_root_path = 'C:/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'


# 获取行数
def file_len(fname):
    with open(fname, 'r', encoding='UTF-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# 创建停用词列表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 计算tf-idf
def tf_idf_cut(movie_name, content_type):
    if (content_type == 'positive'):
        score = [4, 5]
    elif (content_type == 'negative'):
        score = [1, 2]
    else:
        score = [3]

    # 输入路径
    file_path = f_content_path + movie_name + '.txt'
    file_input = open(file_path, 'r', encoding='UTF-8')
    list_file_input = file_input.readlines()
    file_lines = file_len(file_path)

    # 输出路径
    f_words_file_path = f_words_path + 'tf_idf/' + movie_name + '_words_' + content_type + '.txt'
    f_words_file = open(f_words_file_path, 'a+', encoding='UTF-8')

    sentence = ''
    for i in (range(file_lines)):
        if (int(list_file_input[i].split('\t')[0]) in score):
            sentence = sentence + ',' + list_file_input[i].split('\t')[1]

    for w, x in jieba.analyse.extract_tags(sentence, topK=500, withWeight=True, allowPOS=()):
        key_value = w + '\t' + 'x'
        f_words_file.write(key_value)
        print(file=f_words_file)
    f_words_file.close()


# 全模式分词
def word_cut(movie_name, content_type):
    if (content_type == 'positive'):
        score = [4, 5]
    elif (content_type == 'negative'):
        score = [1, 2]
    else:
        score = [3]

    # 输出路径
    f_words_file_path = f_words_path + 'word_cut_all/' + movie_name + '_words_' + content_type + '.txt'
    f_words_file = open(f_words_file_path, 'a+', encoding='UTF-8')

    # 输入路径
    file_path = f_content_path + movie_name + '.txt'
    file_input = open(file_path, 'r', encoding='UTF-8')
    list_file_input = file_input.readlines()
    file_lines = file_len(file_path)

    # 拼接句子
    sentence = ''
    for i in (range(file_lines)):
        if (int(list_file_input[i].split('\t')[0]) in score):
            sentence = sentence + ';' + list_file_input[i].split('\t')[1].strip()

    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', sentence)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    # 去除停用词
    stopwords = stopwordslist(f_strpwords_path)

    # 存入字典计数
    words_dict = {}
    words = jieba.cut(sentence, cut_all=True)
    for word in words:
        # 去除停用词
        if word not in stopwords:
            if (word.strip() != ''):
                # print(word)
                if (word in words_dict.keys()):
                    word_count = words_dict.get(word)
                    word_count = word_count + 1
                else:
                    word_count = 1
                word_key_value = {word: word_count}
                words_dict.update(word_key_value)

    # 写入文件
    # 按value排序
    words_list = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
    for kv in words_list:
        key = kv[0]
        value = kv[1]
        key_value = str(key) + '\t' + str(value)
        f_words_file.write(key_value)
        print(file=f_words_file)
    f_words_file.close()


if __name__ == '__main__':
    movie_name = input("电影名：")
    # positive/negative/neutral
    content_type = input("评价类型：")
    # 全部类型
    content_type_list = ['positive', 'negative', 'neutral']
    if (content_type == 'all'):
        for i in (range(3)):
            param_type = content_type_list[i]

            # tf_idf_cut(movie_name)
            word_cut(movie_name, param_type)
    else:
        word_cut(movie_name, content_type)