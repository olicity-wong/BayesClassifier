# -*- coding: utf-8 -*-
import codecs
import jieba
from numpy import *
import numpy as np
import re
from string import digits

f_root_path = 'F:/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_stop_words_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'
f_words_cut_file = f_words_path + 'word_cut_all/'
f_common_path = f_words_cut_file + 'xbyz_words_common.txt'


# 创建停用词列表
def stop_words_list(filepath):
    stop_words = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stop_words


def common_words_list(filepath):
    common_words = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return common_words


# 去除停用词
stop_words = stop_words_list(f_stop_words_path)

# 公共词
common_words = common_words_list(f_common_path)

# 按行存储到列表
f = codecs.open("F:\\github\\MyAll\\xbyz_1500.txt", 'r', encoding='utf-8')
data = f.readlines()
train_data = []
for line in data:
    train_data.append(line.strip('\r\n').replace('\t', ''))

train_positive_class_list = []
train_negative_class_list = []
train_neutral_class_list = []

# 根据数值判断情感分类
for line in train_data:
    if line[0] in ['4', '5']:
        train_positive_class_list.append(line[1:])
    if line[0] in ['3']:
        train_neutral_class_list.append(line[1:])
    if line[0] in ['1', '2']:
        train_negative_class_list.append(line[1:])
    if line[0] in ['0']:
        continue

# 分词
train_positive_word_cut_temp = []
train_neutral_word_cut_temp = []
train_negative_word_cut_temp = []

train_positive_word_cut = []
train_neutral_word_cut = []
train_negative_word_cut = []

for line in train_positive_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    train_positive_word_cut_temp.append(words)
for line in train_neutral_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    train_neutral_word_cut_temp.append(words)
for line in train_negative_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    train_negative_word_cut_temp.append(words)

# 每行的分词放入列表中
train_positive_flag = 0
train_neutral_flag = 0
train_negative_flag = 0
# 去除停用词和公共词
for line in train_positive_word_cut_temp:
    train_positive_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            train_positive_word_cut[train_positive_flag].append(seg)
    if len(train_positive_word_cut[train_positive_flag]):
        print('not null')
    else:
        train_positive_word_cut[train_positive_flag].append('positive')
    train_positive_flag += 1
for line in train_neutral_word_cut_temp:
    train_neutral_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            train_neutral_word_cut[train_neutral_flag].append(seg)
    if len(train_neutral_word_cut[train_neutral_flag]):
        print('not null')
    else:
        train_neutral_word_cut[train_neutral_flag].append('neutral')
    train_neutral_flag += 1
for line in train_negative_word_cut_temp:
    train_negative_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            train_negative_word_cut[train_negative_flag].append(seg)
    if len(train_negative_word_cut[train_negative_flag]):
        print('not null')
    else:
        train_negative_word_cut[train_negative_flag].append('negative')
    train_negative_flag += 1

train_all_word_cut = train_positive_word_cut + train_negative_word_cut + train_neutral_word_cut
train_all_class_list = []
for line in train_positive_word_cut:
    train_all_class_list.append(2)
for line in train_negative_word_cut:
    train_all_class_list.append(1)
for line in train_neutral_word_cut:
    train_all_class_list.append(0)
print(train_all_word_cut)
print(train_all_class_list)

f = codecs.open("F:\\github\\MyAll\\xbyz_500.txt", 'r', encoding='utf-8')
data1 = f.readlines()
test_data = []
for line in data1:
    test_data.append(line.strip('\r\n').replace('\t', ''))

test_positive_class_list = []
test_neutral_class_list = []
test_negative_class_list = []


test_positive_word_cut_temp = []
test_neutral_word_cut_temp = []
test_negative_word_cut_temp = []

for line in test_data:
    if line[0] in ['4', '5']:
        test_positive_class_list.append(line[1:])
    if line[0] in ['3']:
        test_neutral_class_list.append(line[1:])
    if line[0] in ['1', '2']:
        test_negative_class_list.append(line[1:])
    if line[0] in ['0']:
        continue

test_positive_word_cut = []
test_neutral_word_cut = []
test_negative_word_cut = []

for line in test_positive_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    test_positive_word_cut_temp.append(words)
for line in test_neutral_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    test_neutral_word_cut_temp.append(words)
for line in test_negative_class_list:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    test_negative_word_cut_temp.append(words)

train_positive_flag = 0
train_neutral_flag = 0
train_negative_flag = 0
for line in test_positive_word_cut_temp:
    test_positive_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            test_positive_word_cut[train_positive_flag].append(seg)
    if len(test_positive_word_cut[train_positive_flag]):
        print('not null')
    else:
        test_positive_word_cut[train_positive_flag].append('positive')
    train_positive_flag += 1
for line in test_neutral_word_cut_temp:
    test_neutral_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            test_neutral_word_cut[train_neutral_flag].append(seg)
    if len(test_neutral_word_cut[train_neutral_flag]):
        print('not null')
    else:
        test_neutral_word_cut[train_neutral_flag].append('neutral')
    train_neutral_flag += 1
for line in test_negative_word_cut_temp:
    test_negative_word_cut.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stop_words and seg not in common_words:
            test_negative_word_cut[train_negative_flag].append(seg)
    if len(test_negative_word_cut[train_negative_flag]):
        print('not null')
    else:
        test_negative_word_cut[train_negative_flag].append('negative')
    train_negative_flag += 1

test_all_word_cut = test_positive_word_cut + test_negative_word_cut + test_neutral_word_cut
test_all_class_list = []
for line in test_positive_word_cut:
    test_all_class_list.append(2)
for line in test_negative_word_cut:
    test_all_class_list.append(1)
for line in test_neutral_word_cut:
    test_all_class_list.append(0)
print(test_all_class_list)


class NBayes(object):
    def __init__(self):
        self.vocabulary = []  # 词典
        self.vocabularylist = []
        self.idf = 0
        self.tf = 0  # 训练集的权值矩阵
        self.tt = 0
        self.tfidf = 0
        self.tdm = 0  # p(x|yi)
        self.pcates = {}  # p(yi)类别词典
        self.labels = []  # 对应每个分类的文本
        self.doclength = 0  # 训练集文本数
        self.vocablen = 0  # 词典词长
        self.vacabnum = 0 # 词典所有词数量
        self.testset = 0  # 测试集

    def train_set(self, trainset, classvec):
        self.cate_prob(classvec)  # 计算每个分类在数据集中的概率p(x|yi)
        self.doclength = len(trainset)
        tempset = set()
        [tempset.add(word) for doc in trainset for word in doc]
        temp_list = list()
        [temp_list.append(word) for doc in trainset for word in doc]
        self.vocabularylist = temp_list
        self.vacabnum = len(temp_list)
        self.vocabulary = list(tempset)
        self.vocablen = len(self.vocabulary)
        self.calc_wordfreq(trainset)  # 计算词频数据集
        self.build_tdm()  # 按分类累计向量空间的每维值p(x|yi)

    def cate_prob(self, classvec):
        self.labels = classvec
        labeltemps = set(self.labels)
        for labeltemp in labeltemps:
            self.pcates[labeltemp] = float(self.labels.count(labeltemp)) / float(len(self.labels))

    def calc_wordfreq(self, trainset):
        self.idf = np.zeros([1, self.vocablen])
        self.tf = np.zeros([1, self.vocablen])
        self.tt = np.zeros([self.doclength, self.vocablen])
        tf_tmp = np.zeros([1, self.vocablen])
        for indx in range(self.doclength):
            for word in trainset[indx]:
                tf_tmp[0, self.vocabulary.index(word)] += 1     #统计词频
            for word in trainset[indx]:
                self.tt[indx, self.vocabulary.index(word)] += 1     # 这句话的这个词++
            for singleworld in set(trainset[indx]):
                self.idf[0, self.vocabulary.index(singleworld)] += 1    # 这个词有这句话++
        self.tf = tf_tmp/self.vacabnum
        self.idf = np.log(self.doclength / self.idf + 1)
        self.tfidf = self.tf*self.idf*10000
        # self.tt = self.tt * self.tfidf


    def build_tdm(self):
        self.tdm = np.zeros([len(self.pcates), self.vocablen])  # 类别行*词典列
        sumlist = np.zeros([len(self.pcates), 1])
        for indx in range(self.doclength):
            self.tdm[self.labels[indx]] += self.tt[indx]  # 将同一类别的词向量空间值加总
            sumlist[self.labels[indx]] = np.sum(self.tdm[self.labels[indx]])  # 统计每个分类的总值
        self.tdm = self.tdm / sumlist

    def map2vocab(self, testdata):
        self.testset = np.zeros([1, self.vocablen])
        for word in testdata:
            if word in self.vocabulary:
                self.testset[0, self.vocabulary.index(word)] += 1

    def predict(self, testset):
        if np.shape(testset)[1] != self.vocablen:
            print('输入错误')
            exit(0)
        predvalue = 0
        predclass = ''
        for tdm_vect, keyclass in zip(self.tdm, self.pcates):
            temp = np.sum(testset * self.tfidf[0] * tdm_vect * self.pcates[keyclass])
            if temp > predvalue:
                predvalue = temp
                predclass = keyclass
        return predclass


count = 0
nb = NBayes()
pre_class_list = []
nb.train_set(train_all_word_cut, train_all_class_list)
for i in range(len(test_all_word_cut)):
    nb.map2vocab(test_all_word_cut[i])
    pre_class_list.append(nb.predict(nb.testset))
    value = str(test_all_class_list[i])
    nbpredict = nb.predict(nb.testset)
    print('bayes_cal:%s' % (nbpredict), '------actual_value:%s' % (value))
    if str(nbpredict) == str(value):
        count += 1
# print (listclass)
print(pre_class_list)

print('match_rate:', count / len(test_all_word_cut))
