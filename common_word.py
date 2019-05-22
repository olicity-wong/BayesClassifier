import os

# 定义文件目录
f_root_path = 'F:\github\MyAll\data'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'
f_words_cut_file = f_words_path + 'word_cut_all/'

f_positive_path = f_words_cut_file + 'xbyz_words_positive.txt'
f_negative_path = f_words_cut_file + 'xbyz_words_negative.txt'
f_neutral_path = f_words_cut_file + 'xbyz_words_neutral.txt'
f_common_path = f_words_cut_file + 'xbyz_words_common.txt'

f_positive_read = open(f_positive_path, 'r', encoding='UTF-8')
f_negative_read = open(f_negative_path, 'r', encoding='UTF-8')
f_neutral_read = open(f_neutral_path, 'r', encoding='UTF-8')
f_common_read = open(f_common_path, 'a+', encoding='UTF-8')

words_positive = f_positive_read.readlines()
words_negative = f_negative_read.readlines()
words_neutral = f_neutral_read.readlines()

words_positive_1 = []
words_neagtive_1 = []
words_neutral_1 = []

for word in words_positive:
    words_positive_1.append(word.split('\t')[0])
for word in words_negative:
    words_neagtive_1.append(word.split('\t')[0])
for word in words_neutral:
    words_neutral_1.append(word.split('\t')[0])

common_words = []

for word in words_positive_1:
    if word in words_neagtive_1:
        if word in words_neutral_1:
            common_words.append(word)

for word in common_words:
    if word != '' and word != '\r\n':
        f_common_read.write(word)
        print(file=f_common_read)
f_common_read.close()
