import os

# 打乱顺序取1500与500
import random


# 定义文件目录
f_root_path = 'C:/Users/91460/Desktop/论文相关/hapi/MyAll/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'
f_words_cut_file = f_words_path + 'word_cut_all/'

movie = input("电影名：")
read_file = f_content_path + '%s.txt' % (movie)
write_file1 = f_content_path + '%s_1500.txt' % (movie)
write_file2 = f_content_path + '%s_500.txt' % (movie)

f_read = open(read_file, 'r', encoding='UTF-8')
list_f_read = f_read.readlines()
print(len(list_f_read))

list_train = []
# 生成随机数
# for i in range(1500):
#    num = random.randint(1, 2000)
#    list_train.append(num)
# print(len(list_train))
# print(list_train)
list_train = random.sample(range(0, 2000), 1500)
print(len(list_train))
print(list_train)

list_tmp = []
for i in range(0, 2000):
    list_tmp.append(i)
print(len(list_tmp))
print(list_tmp)

list_test = []
for a in list_tmp:
    if a not in list_train:
        list_test.append(a)
print(len(list_test))
print(list_test)

f_write1 = open(write_file1, 'w', encoding='UTF-8')
f_write2 = open(write_file2, 'w', encoding='UTF-8')
count1 = 0
for i in list_train:
    num = int(i)
    line = list_f_read[num]
    f_write1.write(line)
    count1 = count1 + 1
f_write1.close()
print(count1)
count2 = 0
for i in list_test:
    num = int(i)
    line = list_f_read[num]
    f_write2.write(line)
    count2 = count2 + 1
f_write2.close()
print(count2)
