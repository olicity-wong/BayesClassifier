import os

# 打乱顺序取1500与500
import file_random

read_file = 'F:\\github\\MyAll\\xbyz.txt'
write_file1 = 'F:\\github\\MyAll\\xbyz_1500.txt'
write_file2 = 'F:\\github\\MyAll\\xbyz_500.txt'

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
list_train = file_random.sample(range(0, 2000), 1500)
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
