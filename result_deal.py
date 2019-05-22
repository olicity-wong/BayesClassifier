import os

'''
输入文件名，自动将爬取的文件结果进行整合
'''
f_root_path = 'F:/github/MyAll/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'


# 文件名统一
def rename_file(rename_file_path):
    movie_name = os.listdir(rename_file_path)
    for temp in movie_name:
        num = temp.find('_abc123_')
        if (num >= 0):
            new_name = temp[:num]
            print(new_name)
            os.rename(rename_file_path + '/' + temp, rename_file_path + '/' + new_name)


# 获取行数
def file_len(fname):
    with open(fname, "r", encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# 修改分数格式
def score_std(var):
    return {
        'allstar10 rating': 1,
        'allstar20 rating': 2,
        'allstar30 rating': 3,
        'allstar40 rating': 4,
        'allstar50 rating': 5,
        'no score': 0,
    }.get(var, 'error')


# score&content整合
def result_concat(movie_name, content_type):
    f_movie_name = movie_name
    if (content_type == 'h' or content_type == 'l' or content_type == 'm'):
        f_movie_name = movie_name + '_' + content_type

    # 输入路径
    f_star_name = f_scrapy_path + movie_name + '/' + f_movie_name + '_score'
    f_content_name = f_scrapy_path + movie_name + '/' + f_movie_name + '_content'
    if (os.path.exists(f_star_name) and os.path.exists(f_content_name)):
        f_star_read = open(f_star_name, 'r', encoding='UTF-8')
        f_content_read = open(f_content_name, 'r', encoding='UTF-8')
        list_star = f_star_read.readlines()
        list_content = f_content_read.readlines()

        # 输出路径
        f_save = open(f_content_path + "/%s.txt" % (movie_name), "a+", encoding='utf-8')

        star_file_length = file_len(f_star_name)
        content_file_length = file_len(f_content_name)
        if (star_file_length != content_file_length):
            print("数量不一致！！！退出")
            exit(1)
        for i in range(star_file_length):
            score = score_std(list_star[i].strip())
            str_save = str(score) + '\t' + list_content[i].strip()
            f_save.write(str_save)
            print(file=f_save)
        f_save.close()


if __name__ == "__main__":
    param_name_list = ['', 'l', 'm', 'h']
    param_name = input("电影名：")
    # 文件名统一
    rename_file_path = f_scrapy_path + param_name
    rename_file(rename_file_path)
    for i in (range(4)):
        param_type = param_name_list[i]
        print(param_type)
        result_concat(param_name, param_type)
