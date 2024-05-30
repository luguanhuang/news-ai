import requests,time
from bs4 import BeautifulSoup
import json
import io
import sys
import urllib.request
import cchardet
from lib import mysql_lib
import datetime

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'no-cache'
}

def getHtml(url):
    res = requests.get(url=url,headers=headers)

    con_encoding = cchardet.detect(res.content)['encoding'] 

    print("res.apparent_encoding=", 
        res.apparent_encoding, " con_encoding=", con_encoding)
    print("res.encoding=", res.encoding)
    # res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
    res.encoding=res.apparent_encoding #直接用requests 返回的Response对象的encoding属性调整编码
    html = res.content
    time.sleep(0.7)
    print("status=", res.status_code)
    if res.status_code==200:
        return html

def downsavemysql(title, suburl):
    subres = requests.get(suburl)
    subsoup=BeautifulSoup(subres.content, "html.parser")
    aticleinfo=subsoup.find(class_='content-lock-content')
    sentenceinfo = aticleinfo.select("p")
    content = ""
    for subsen in sentenceinfo:
        # print("subsen=", subsen.get_text())
        content = content + subsen.get_text() + "\n"

    nowtime = datetime.datetime.now()
    # mysql_lib.insert_crawtext("biaticleinfo", title, content, suburl, "lastest data", nowtime)
    mysql_lib.insert_crawtext(table="crawtext",title=title, title_cn="", url=suburl, description=content,  \
                                description_nohtml="", source_tag='news-ai', craw_status="-1-原始抓取", timestamp=nowtime)

def downspecifytag(data, tag, title):
    tmp11 = data.find_all(tag, class_=title)
    if len(tmp11) > 0:
        time.sleep(0.2)
        downsavemysql(tmp11[0].get_text(), 
            "https://www.businessinsider.com"+data['href']);

def downloadbusi():
    res = requests.get("https://www.businessinsider.com/")
    try:
        #latest section data
        soup=BeautifulSoup(res.content, "html.parser")
        # find all tags
        tags = soup.find_all()
        for tag in tags:
        # find all href links
            tmp = tag.find_all(href=True)
            for data in tmp:
                downspecifytag(data, 'h3', "quick-link-title headline-bold")
                downspecifytag(data, 'h3', "tout-title")
                downspecifytag(data, 'h3', "main-tout-title")
                downspecifytag(data, 'h3', "quick-link-title headline-bold")
    except Exception as exc:
        print("There was a problem: %s" %(exc))



