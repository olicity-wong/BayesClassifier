import requests
import time
from pyquery import PyQuery as pq
import re
from urllib.parse import urlencode
import datetime

base_url="https://movie.douban.com/subject/30163509/comments?"

user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36 Firefox/23.0'
headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'User-Agnet': user_agent
}

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

#解析html页面
def get_html(url):
    print('crawing ', url) # 输出正在爬取的url
    response = requests.get(url,headers=headers)
    time.sleep(2)  # 暂停10秒
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
    #for page in range(1, int(pagenum)):
    for page in range(1, 6):
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



if __name__=="__main__" :
    main()