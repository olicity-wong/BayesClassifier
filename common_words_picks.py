# 定义文件目录
f_root_path = 'E:/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'
f_words_cut_path = f_words_path + 'word_cut_all/'

def get_common_words(movie_name):
    positive_file_path = f_words_cut_path + movie_name + '_words_positive.txt'
    neutral_file_path = f_words_cut_path + movie_name + '_words_neutral.txt'
    negative_file_path = f_words_cut_path + movie_name + '_words_negative.txt'
    f_save = open(f_words_cut_path + "%s_words_common.txt" % (movie_name), "a+", encoding='utf-8')
    f_positive_read = open(positive_file_path, 'r', encoding='UTF-8')
    f_neutral_read = open(neutral_file_path, 'r', encoding='UTF-8')
    f_negative_read = open(negative_file_path, 'r', encoding='UTF-8')
    positive_words = f_positive_read.readlines()
    neutral_words = f_neutral_read.readlines()
    negative_words = f_negative_read.readlines()
    common_words = set()
    for word in positive_words:
        if word in neutral_words:
            common_words.add(word)
        if word in negative_words:
            common_words.add(word)
    for word in neutral_words:
        if word in negative_words:
            common_words.add(word)
    print(common_words)
    for word in common_words:
        f_save.write(word.strip('\r\n'))
        print(file=f_save)
    f_save.close()
if __name__ == "__main__":
    movie_name = input("电影名：")
    get_common_words(movie_name)