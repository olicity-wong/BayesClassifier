# -*- coding: utf-8 -*-
import codecs
import jieba
from numpy import *
import numpy as np
import re
from string import digits

f_root_path = 'C:/Users/91460/Desktop/论文相关/hapi/MyAll/data/'
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


# 数据处理
def process_data(file_path,type):
    # 按行存储到列表"F:\\github\\MyAll\\xbyz_1500.txt"
    f = codecs.open(file_path, 'r', encoding='utf-8')
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
    if type == "test":
        global sentences_list
        sentences_list = train_positive_class_list + train_negative_class_list + train_neutral_class_list
    # 分词
    train_positive_word_cut = word_cut(train_positive_class_list, "positive")
    train_neutral_word_cut = word_cut(train_neutral_class_list, "neutral")
    train_negative_word_cut = word_cut(train_negative_class_list, "negative")

    # 所有句子分词集
    train_all_word_cut = train_positive_word_cut + train_negative_word_cut + train_neutral_word_cut
    # 分类标记集
    train_all_class_list = []
    for line in train_positive_word_cut:
        train_all_class_list.append(2)
    for line in train_negative_word_cut:
        train_all_class_list.append(1)
    for line in train_neutral_word_cut:
        train_all_class_list.append(0)
    print(train_all_word_cut)
    print(train_all_class_list)
    return train_all_word_cut, train_all_class_list


# 分词
def word_cut(train_class_list, type):
    train_word_cut_temp = []
    train_word_cut = []
    train_flag = 0
    for line in train_class_list:
        # 去除标点符号
        sentence = re.sub(r'[^\w\s]', '', line)

        # 去除数字
        remove_digits = str.maketrans('', '', digits)
        sentence = sentence.translate(remove_digits)

        # 分词
        words = jieba.cut(sentence, cut_all=True, HMM=True)
        train_word_cut_temp.append(words)
    for line in train_word_cut_temp:
        train_word_cut.append([])
        for seg in line:
            if seg != '\r\n' and seg not in stop_words and seg not in common_words:
                train_word_cut[train_flag].append(seg)
        if len(train_word_cut[train_flag]):
            train_flag += 1
            continue
        else:
            train_word_cut[train_flag].append(type)
        train_flag += 1
    return train_word_cut


# 贝叶斯模型
class NBayes(object):
    def __init__(self):
        self.vocabulary = []  # 词典
        self.idf = 0
        self.tf = 0  # 训练集的权值矩阵
        self.tfidf = 0
        self.tdm = 0  # p(x|yi)
        self.pcates = {}  # p(yi)类别词典
        self.labels = []  # 对应每个分类的文本
        self.doclength = 0  # 训练集文本数
        self.vocablen = 0  # 词典词长
        self.testset = 0  # 测试集

    def train(self, trainset, classvec):
        self.calc_prob(classvec)  # 计算每个分类在数据集中的概率p(x|yi)
        self.doclength = len(trainset)
        tempset = set()
        [tempset.add(word) for doc in trainset for word in doc]
        self.vocabulary = list(tempset)
        self.vocablen = len(self.vocabulary)
        self.calc_tfidf(trainset)  # 计算词频数据集
        self.calc_tdm()  # 按分类累计向量空间的每维值p(x|yi)

    # 采用极大似然估计计算p(y)
    def calc_prob(self, classvec):
        self.labels = classvec
        labeltemps = set(self.labels)
        for labeltemp in labeltemps:
            self.pcates[labeltemp] = float(self.labels.count(labeltemp)) / float(len(self.labels))

    def calc_tfidf(self, trainset):
        self.idf = np.ones([1, self.vocablen])
        self.tf = np.zeros([self.doclength, self.vocablen])
        for indx in range(self.doclength):
            for word in trainset[indx]:
                self.tf[indx, self.vocabulary.index(word)] += 1  # 这句话的这个词++/词袋模型
            self.tf[indx] /= np.sum(self.tf[indx])
            for singleworld in set(trainset[indx]):
                self.idf[0, self.vocabulary.index(singleworld)] += 1  # 这个词有这句话++
        # self.idf = np.log(self.doclength / self.idf + 1)
        self.idf = np.log(float(self.doclength)) - np.log(self.idf)
        self.tfidf = np.multiply(self.tf, self.idf)

    # 计算条件概率 p(x|y_i)
    def calc_tdm(self):
        self.tdm = np.zeros([len(self.pcates), self.vocablen])  # 类别行*词典列
        sumlist = np.zeros([len(self.pcates), 1])
        for indx in range(self.doclength):
            self.tdm[self.labels[indx]] += self.tfidf[indx]  # 将同一类别的词向量空间值加总
            sumlist[self.labels[indx]] = np.sum(self.tdm[self.labels[indx]])  # 统计每个分类的总值
        self.tdm = self.tdm / sumlist  # 归一化

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
            temp = np.sum(testset * tdm_vect * self.pcates[keyclass])
            if temp > predvalue:
                predvalue = temp
                predclass = keyclass
        return predclass


if __name__ == "__main__":

    nb = NBayes()

    train_data_path = "C:\\Users\\91460\\Desktop\\论文相关\\hapi\\MyAll\\xbyz_1500.txt"
    train_all_word_cut, train_all_class_list = process_data(train_data_path,"train")
    nb.train(train_all_word_cut, train_all_class_list)
    test_data_path = "C:\\Users\\91460\\Desktop\\论文相关\\hapi\\MyAll\\xbyz_500.txt"
    test_all_word_cut, test_all_class_list = process_data(test_data_path,"test")

    save_data_path = "C:\\Users\\91460\\Desktop\\论文相关\\hapi\\MyAll\\xbyz_pre.txt"
    save_data_file = open(save_data_path, 'a+', encoding='UTF-8')
    count = 0
    null_count = 0
    un_null_count = 0
    pre_class_list = []

    for i in range(len(test_all_word_cut)):
        nb.map2vocab(test_all_word_cut[i])
        pre_class_list.append(nb.predict(nb.testset))
        value = str(test_all_class_list[i])
        nbpredict = nb.predict(nb.testset)
        print('bayes_cal:%s' % (nbpredict), '------actual_value:%s' % (value))
        if str(nbpredict) == str(value):
            count += 1
        if str(nbpredict) == "":
            null_count += 1
        if str(nbpredict) != "":
            un_null_count += 1
        # 写文件
        key_value = str(nbpredict) + '\t' + str(sentences_list[i])
        save_data_file.write(key_value)
        print(file=save_data_file)
    save_data_file.close()

    print(pre_class_list)

    print('correct_rate:', count / len(test_all_word_cut))
    print('match_correct_rate:', count / un_null_count)
    print('no_match_rate:', null_count / len(test_all_word_cut))
