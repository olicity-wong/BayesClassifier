# -*- coding: utf-8 -*-
import sys
import os
import codecs
import jieba
from numpy import *
import numpy as np
import re
from string import digits



f_root_path = 'F:/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'
f_words_cut_file=f_words_path+'word_cut_all/'
f_common_path=f_words_cut_file+'xbyz_words_common.txt'
# 创建停用词列表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def commonwordslist(filepath):
    commonwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return commonwords

# 去除停用词
stopwords = stopwordslist(f_strpwords_path)

# 公共词
commonwords = commonwordslist(f_common_path)

#按行存储到列表
f = codecs.open("F:\\github\\MyAll\\xbyz_1500.txt",'r',encoding='utf-8')
data = f.readlines()
newdata = []
segmenttest = []
newsegmenttest = []
for line in data:
    newdata.append(line.strip('\r\n'))
for line in newdata:
    segmenttest.append(line.replace('\t',''))

classpositive = []
classnegative = []
classneutral = []

temp1 = []
temp2 = []
temp3 = []

#根据数值判断情感分类
for line in segmenttest:
    if line[0] in ['4', '5']:
        classpositive.append(line[1:])
    if line[0] in ['3']:
        classneutral.append(line[1:])
    if line[0] in ['1', '2']:
        classnegative.append(line[1:])
    if line[0] in ['0']:
        continue
splitpositive = []
splitnegative = []
splitneutral = []



#分词
for line in classpositive:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)


    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp1.append(words)
for line in classneutral:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp2.append(words)
for line in classnegative:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp3.append(words)
#########################################################
#每行的分词放入列表中
i1 = 0
i2 = 0
i3 = 0
for line in temp1:
    splitpositive.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitpositive[i1].append(seg)
    if len(splitpositive[i1]):
        print('not null')
    else:
        splitpositive[i1].append('positive')
    i1 += 1
for line in temp2:
    splitneutral.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitneutral[i2].append(seg)
    if len(splitneutral[i2]):
        print('not null')
    else:
        splitneutral[i2].append('neutral')
    i2 += 1
for line in temp3:
    splitnegative.append([])
    for seg in line :
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitnegative[i3].append(seg)
    if len(splitnegative[i3]):
        print('not null')
    else:
        splitnegative[i3].append('negative')
    i3 += 1

splitdata = splitpositive + splitnegative +splitneutral
listclass = []
for line in splitpositive:
    listclass.append(2)
for line in splitnegative:
    listclass.append(1)
for line in splitneutral:
    listclass.append(0)
print(splitdata)
print(listclass)
######################################################################################
f = codecs.open("F:\\github\\MyAll\\xbyz_500.txt",'r',encoding='utf-8')
data1 = f.readlines()
newdata1 = []
segmenttest1 = []
newsegmenttest1 = []
for line in data1:
    newdata1.append(line.strip('\r\n'))
for line in newdata1:
    segmenttest1.append(line.replace('\t',''))

classpositive1 = []
classnegative1 = []
classneutral1 = []

temp11 = []
temp21 = []
temp31 = []

for line in segmenttest1:
    if line[0] in ['4', '5']:
        classpositive1.append(line[1:])
    if line[0] in ['3']:
        classneutral1.append(line[1:])
    if line[0] in ['1', '2']:
        classnegative1.append(line[1:])
    if line[0] in ['0']:
        continue

splitpositive1 = []
splitnegative1 = []
splitneutral1 = []


for line in classpositive1:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp11.append(words)
for line in classneutral1:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp21.append(words)
for line in classnegative1:
    # 去除标点符号
    sentence = re.sub(r'[^\w\s]', '', line)

    # 去除数字
    remove_digits = str.maketrans('', '', digits)
    sentence = sentence.translate(remove_digits)

    words = jieba.cut(sentence, cut_all=True, HMM=True)
    temp31.append(words)

i1 = 0
i2 = 0
i3 = 0
for line in temp11:
    splitpositive1.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitpositive1[i1].append(seg)
    if len(splitpositive1[i1]):
        print('not null')
    else:
        splitpositive1[i1].append('positive')
    i1 += 1
for line in temp21:
    splitneutral1.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitneutral1[i2].append(seg)
    if len(splitneutral1[i2]):
        print('not null')
    else:
        splitneutral1[i2].append('neutral')
    i2 += 1
for line in temp31:
    splitnegative1.append([])
    for seg in line:
        if seg != '\r\n' and seg not in stopwords and seg not in commonwords:
            splitnegative1[i3].append(seg)
    if len(splitnegative1[i3]):
        print('not null')
    else:
        splitnegative1[i3].append('negative')
    i3 += 1

splitdata1 = splitpositive1 + splitnegative1 +splitneutral1
listclass1 = []
for line in splitpositive1:
    listclass1.append(2)
for line in splitnegative1:
    listclass1.append(1)
for line in splitneutral1:
    listclass1.append(0)
print(listclass1)
##############################################################################
class NBayes(object):
    def __init__(self):
        self.vocabulary = []    #词典
        self.idf = 0
        self.tf = 0             #训练集的权值矩阵
        self.tdm = 0            #p(x|yi)
        self.Pcates = {}        #p(yi)类别词典
        self.labels = []        #对应每个分类的文本
        self.doclength = 0      #训练集文本数
        self.vocablen = 0       #词典词长
        self.testset = 0        #测试集

    def train_set(self,trainset,classvec):
        self.cate_prob(classvec)    #计算每个分类在数据集中的概率p(x|yi)
        self.doclength = len(trainset)
        tempset = set()
        [tempset.add(word) for doc in trainset for word in doc]
        self.vocabulary = list(tempset)
        self.vocablen = len(self.vocabulary)
        self.calc_wordfreq(trainset)    #计算词频数据集
        self.build_tdm()            #按分类累计向量空间的每维值p(x|yi)

    def cate_prob(self,classvec):
        self.labels = classvec
        labeltemps = set(self.labels)
        for labeltemp in labeltemps:
            self.Pcates[labeltemp] = float(self.labels.count(labeltemp))/float(len(self.labels))

    def calc_wordfreq(self,trainset):
        self.idf = np.zeros([1,self.vocablen])
        self.tf = np.zeros([self.doclength,self.vocablen])
        for indx in range(self.doclength):
            for word in trainset[indx]:
                self.tf[indx,self.vocabulary.index(word)] += 1
            for singleworld in set(trainset[indx]):
                self.idf[0,self.vocabulary.index(singleworld)] += 1
        self.idf = np.log10(self.doclength/self.idf+1)

    def build_tdm(self):
        self.tdm = np.zeros([len(self.Pcates),self.vocablen])   #类别行*词典列
        sumlist = np.zeros([len(self.Pcates),1])
        for indx in range(self.doclength):
            self.tdm[self.labels[indx]] += self.tf[indx]      #将同一类别的词向量空间值加总
            sumlist[self.labels[indx]] = np.sum(self.tdm[self.labels[indx]])    #统计每个分类的总值
        self.tdm = (self.tdm/sumlist)*self.idf

    def map2vocab(self,testdata):
        self.testset = np.zeros([1,self.vocablen])
        for word in testdata:
            if word in self.vocabulary:
                self.testset[0,self.vocabulary.index(word)] += 1

    def predict(self,testset):
        if np.shape(testset)[1] != self.vocablen:
            print ('输入错误')
            exit(0)
        predvalue = 0
        predclass = ''
        for tdm_vect,keyclass in zip(self.tdm,self.Pcates):
            temp = np.sum(testset*tdm_vect*self.Pcates[keyclass])
            if temp > predvalue:
                predvalue = temp
                predclass = keyclass
        return predclass

count=0
nb = NBayes()
newlistclass = []
nb.train_set(splitdata,listclass)
for i in range(len(splitdata1)):
    nb.map2vocab(splitdata1[i])
    newlistclass.append(nb.predict(nb.testset))
    #print('listclass1[i]:'+str(listclass1[i]))
    value = str(listclass1[i])
    nbpredict=nb.predict(nb.testset)
    print('bayes_cal:%s'%(nbpredict),'------actual_value:%s'%(value))
    if str(nbpredict) == str(value):
        count += 1
#print (listclass)
print (newlistclass)

print ('match_rate:',count/len(splitdata1))