import requests as r
from bs4 import BeautifulSoup
import re


def Format(text):
    '''
    格式化爬取的内容
    return:格式化后的text
    '''
    text = str(text)[38:-62] 
    #这个网站爬取下来的content正文前后夹着莫名其妙的无法删去的html标签，只能这样了 
    text = re.sub(r'\s+', '', text).strip()
    replaced = re.sub('<br/>|<p>|</p>','|',text)
    text = replaced.split('|')
    for i in text:
        if len(i)==0:
            text.remove(i)
    return text


def GetNovels(number_begin,quantity,source_url):
    '''
    批量爬取多个小说
    number_begin:起始编号
    quantity:爬取数量
    source_url:小说源地址（介绍中的Source）
    '''
    print('''收到爬取请求，信息：
          number_begin:{}
          quantity:{}
          source_url:{}'''.format(
              number_begin,quantity,source_url))
    
    number = number_begin
    length_all=0

    for now in range(quantity):
        responses = r.get(url='{}/{}.html'.format(source_url,str(number)))
        number+=1
        responses.encoding='utf-8'
        print(responses)

        soup = BeautifulSoup(responses.text, 'html.parser')
        news_items = soup.select('.panel-body')
        news_items = Format(text=news_items)

        print('Log#{}:\nlength:{},\ncontent:{}...{},'.format(number,len(news_items),str(news_items)[:20],str(news_items)[-20:]))

        with open('./t/novels.txt',mode='a',encoding='utf-8') as file:
            file.write('\n\n【第{}章】\n'.format(str(now)))
            for i in news_items:
                file.write(i+'\n')
        
        print('write Done!\n{}%COMPLETED!\n'.format(str(int((now+1)/quantity*100))))
        length_all+=len(news_items)

    print()

def GetSingleNovel(source_url,number,filename,page):
    '''
    爬取单个小说
    source_url:小说源地址（介绍中的Source）
    number:爬取小说的编号
    filename:保存小说的文件名
    page:爬取小说的页码对应的编号
    '''
    responses = r.get(url=source_url)
    responses.encoding='utf-8'
    print(responses)

    soup = BeautifulSoup(responses.text, 'html.parser')
    news_items = soup.select('.panel-body')

    news_items = Format(text=news_items)

    print('Log#{}:\nlength:{},\ncontent:{}...{},'.format(number,len(news_items),str(news_items)[:20],str(news_items)[-20:]))
    with open(filename,mode='a',encoding='utf-8') as file:
        file.write('\n\n【第{}章#{}】\n'.format(str(number),page))
        for i in news_items:
            file.write(i+'\n')
    
def GetNovelLength(source_url):
    '''
    获取小说长度
    source_url:小说源地址（介绍中的Source）
    return:小说长度
    获取小说长度，即字数
    该功能目前尚未在main.py中使用
    '''
    responses = r.get(url=source_url)
    responses.encoding='utf-8'
    print(responses)

    soup = BeautifulSoup(responses.text, 'html.parser')
    news_items = soup.select('.panel-body')

    news_items = Format(text=news_items)

    return len(news_items)