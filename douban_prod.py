import requests
import time
from pyquery import PyQuery as pq
import re
from urllib.parse import urlencode
import datetime
from http import cookiejar

base_url="https://movie.douban.com/subject/30163509/comments?"


# headers_movie={
#     'Connection': 'keep-alive',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Host': 'movie.douban.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Upgrade-Insecure-Requests:': '1',
# }
#
# headers_login_start = {
#     'Referer': 'https://accounts.douban.com/passport/login',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
# }
# headers_login_click={
#     'Referer': 'https://accounts.douban.com/passport/login',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
# }
# headers_login_basic={
#     'Accept': 'application/json',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Origin': 'https://accounts.douban.com',
#     'Referer': 'https://accounts.douban.com/passport/login',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'

}

global session
session=requests.Session()
session.headers.update(headers)

def save_to_csv(list,type,page):
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S") #获取当前时间
    str_param = type+'_'+str(page)+'_'+nowtime
    with open("F:/scrapyData/fcrs_%s.txt"%(str_param), "w",newline='',encoding='utf-8') as f:
        for info in list:
            #print(info)
            f.writelines([info])
            print(file=f)


def parse_content(html):
    doc = pq(html)  # 得到网页源码
    contents = doc('.comment-item p').items()
    scores = doc('.comment-item h3 .comment-info').items()
    return contents,scores

def get_page_html(page):

    data={
        'start':(page-1)*20,
        'limit':20,
        'status':'P'
    }
    queries=urlencode(data)
    url=base_url+queries
    print("当前位置：",queries)
    html=get_html(url)
    return html

#解析html页面session.headers.update(headers_movie)
def get_html(url):
    print('crawing ', url) # 输出正在爬取的url
    response = session.get(url,headers=headers)
    time.sleep(15)  # 暂停10秒
    return response.text

#获取总的评论的条数
def parse_comment(html):
    doc=pq(html) # 得到网页源码
    num=doc('#content > div > div.article > div.clearfix.Comments-hd > ul > li.is-active > span').text()#获取span标签的内容
    num=re.findall('\d+',num)[0]
    return num

def main():
    print("start")
    index_html=get_html("https://movie.douban.com/subject/30163509/comments?status=P")
    print(parse_comment(index_html))
    total_num=parse_comment(index_html)
    pagenum=int(total_num)/20+1
    for page in range(1, int(pagenum)):
        #10页登陆
        if page%10==0:
            douban_login()
        print(session.cookies.items())
        comment_list=[]
        score_list=[]
        print('page= '+str(page))
        page_html=get_page_html(page)
        if page_html:
            contents,scores=parse_content(page_html)
            for score in scores:
                if( not str(score('span').eq(3)).strip()):
                    score_deal = 'no score'
                    print(score_deal)
                else:
                    score_deal = score('span').eq(2).attr('class')
                    print(score_deal)
                score_list = score_list + [score_deal]
            for content in contents:
                content_deal = content.text()
                print(content_deal)
                comment_list = comment_list + [content_deal]
        save_to_csv(comment_list,'content',page)
        save_to_csv(score_list,'score',page)


def douban_login():
    username = '13031623728'
    password = 'abc123456'
    data = {                    #需要传去的数据
        'ck':'B0hi',
        'name':username,
        'password':password,
        'remember':'false',
        'ticket':''
    }
    # login_start_url='https://www.douban.com/stat.html'
    # login_click_url='https://www.douban.com/stat.html'
    login_basic_url='https://accounts.douban.com/j/mobile/login/basic'

    html = session.post(login_basic_url,data=data,headers=headers)
    print(session.cookies.items())

if __name__=="__main__" :
    douban_login()
    main()