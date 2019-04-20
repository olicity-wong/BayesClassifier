'''
豆瓣影评爬虫
功能：根绝输入的电影名称与id和评论类型进行爬取，并将结果保存至本地文件
'''
import os
import requests
import time
from pyquery import PyQuery as pq
from urllib.parse import urlencode
import datetime
import shutil

# 定义文件目录
f_root_path = 'C:/data/'
f_scrapy_path = f_root_path + 'scrapy_data/'
f_content_path = f_root_path + 'content_data/'
f_strpwords_path = f_root_path + 'aux_data/stop_words.txt'
f_words_path = f_root_path + 'words_data/'

base_url = "https://movie.douban.com/subject/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'

}
session = requests.Session()
session.headers.update(headers)


# 保存文件
def save_to_file(list, type, page, movie_name, content_type):
    # 文件名添加时间，已区分，防止覆盖
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")  # 获取当前时间
    str_param = type + '_abc123_' + str(page) + '_' + nowtime
    # 创建该电影目录
    dir_path = f_scrapy_path + movie_name
    if (os.path.exists(dir_path)):
        # shutil.rmtree(dir_path)
        print('exists')
    else:
        os.mkdir(dir_path)
    if (content_type.strip() in ['h', 'm', 'l']):
        file_name = dir_path + '/' + movie_name + "_" + content_type + "_%s.txt" % (str_param)
    else:
        file_name = dir_path + '/' + movie_name + "_%s.txt" % (str_param)
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        for info in list:
            # print(info)
            f.writelines([info])
            print(file=f)


# 获取评论与分数
def parse_content(html):
    doc = pq(html)  # 得到网页源码
    contents = doc('.comment-item p').items()
    scores = doc('.comment-item h3 .comment-info').items()
    return contents, scores


# 拼接url
def get_page_html(page, movie_id, content_type):
    data = {
        'start': (page - 1) * 20,
        'limit': 20,
        'status': 'P',
    }
    data_l = {
        'percent_type': 'l'
    }
    data_h = {
        'percent_type': 'h'
    }
    data_m = {
        'percent_type': 'm'
    }
    if (content_type == 'l'):
        data.update(data_l)
    elif (content_type == 'h'):
        data.update(data_h)
    elif (content_type == 'm'):
        data.update(data_m)
    else:
        print('nothing')
    movie_url = base_url + movie_id + '/comments?'
    # &percent_type=h/m/l
    queries = urlencode(data)
    url = movie_url + queries
    print("当前位置：", queries)
    html = get_html(url)
    return html


# 解析html页面
def get_html(url):
    print('crawing ', url)  # 输出正在爬取的url
    response = session.get(url, headers=headers)
    time.sleep(1)  # 暂停1秒
    return response.text


# 爬虫主体
def main(movie_name, movie_id, content_type):
    print("start=======================")

    # 评论list
    comment_list = []
    # 分数list
    score_list = []
    # 标记失败次数
    fail_count = 0
    # 标记是否失败过
    global fail_flag

    # 只爬取前25页
    for page in range(1, int(26)):
        fail_flag = 0
        # #30页登陆
        # if page%30==0:
        #     douban_login()
        print(session.cookies.items())

        print('page= ' + str(page))
        page_html = get_page_html(page, movie_id, content_type)
        if page_html:
            contents, scores = parse_content(page_html)
            for score in scores:
                if (not str(score('span').eq(3)).strip()):
                    score_deal = 'no score'
                    print(score_deal)
                else:
                    score_deal = score('span').eq(2).attr('class')
                    print(score_deal)
                score_list = score_list + [score_deal]
            for content in contents:
                content_deal = content.text()
                print(content_deal)
                # 打印空
                if (not str([content_deal]).strip()):
                    fail_flag = 1
                comment_list = comment_list + [content_deal]
            if (fail_flag == 1):
                doc = pq(page_html)
                print("当前页为：" + page)
                print("当前时间为：" + datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))
                fail_count = fail_count + 1
                print("当前失败次数为：" + fail_count)
                # 重新登陆尝试
                print("正在尝试重新登陆。。。。。")
                douban_login()
                fail_flag = 0
                if (fail_count > 50):
                    print("失败次数已超过制定次数，保存文件退出")
                    # 打印当前错误网页源码，以应对反爬
                    print(doc)
                    save_to_file(comment_list, 'content', page, content_type)
                    save_to_file(score_list, 'score', page, content_type)
                    exit(1)
        ##100页存一个文件
        # if page%26==0:
        #    save_to_file(comment_list,'content',page)
        #    save_to_file(score_list,'score',page)
        #    comment_list=[]
        #    score_list=[]
    save_to_file(comment_list, 'content', page, movie_name, content_type)
    save_to_file(score_list, 'score', page, movie_name, content_type)


# cookie模拟登陆
def douban_login(username, password):
    # 7Lew
    data = {  # 需要传去的数据
        'ck': 'B0hi',
        'name': username,
        'password': password,
        'remember': 'false',
        'ticket': ''
    }
    login_basic_url = 'https://accounts.douban.com/j/mobile/login/basic'
    html = session.post(login_basic_url, data=data, headers=headers)
    print(session.cookies.items())


if __name__ == "__main__":
    # 飞驰人生：30163509
    # 后来的我们：26683723
    # 神奇动物：格林德沃之罪：26147417
    # 地球最后的夜晚：26633257
    # 西虹市首富：27605698
    # 邪不压正：26366496

    movie_name = input("电影名：")

    movie_id = input("电影id：")

    # username = '13031623728'
    # password = 'abc123456'
    username = input("用户名：")
    password = input("密码：")

    # percent_type=h/m/l/all
    content_type = input("爬取评论类型：")
    # 全部类型
    content_type_list = ['aaa', 'l', 'm', 'h']
    if (content_type == 'all'):
        for i in (range(4)):
            param_type = content_type_list[i]

            # 模拟登陆
            douban_login(username, password)

            main(movie_name, movie_id, param_type)
