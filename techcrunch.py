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

def downloadhtml(url, filename):
    res = requests.get(url=url,headers=headers)
    res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
    html = res.text
    time.sleep(0.7)
    if res.status_code==200:
        print("成功了：{0}".format(url))
        with open(filename,"w",encoding="utf-8")as file:
            #将每页网页的内容存进listpage文件夹中
            file.write(html)

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
        # print("成功了：{0}".format(url))
        # with open(filename,"w",encoding="utf-8")as file:
        #     #将每页网页的内容存进listpage文件夹中
        #     file.write(html)

def Parsetechcrunchcontent():
    res = requests.get("https://www.techcrunch.com")
    try:
        soup=BeautifulSoup(res.content, "html.parser")
        #latest section data
        latest=soup.find(class_='river--homepage')
        #article timestamp
        article_time_stamp=latest.find_all('time', class_="river-byline__time")

        #article title
        article_title=latest.find_all('h2', class_='post-block__title')
        for data in article_title:
            print("data=", data.get_text())
            ainfo = data.select("a")
            for i in ainfo:
                print("a=", i['href'])
                time.sleep(0.2)
                subres = requests.get(i['href'])
                subsoup=BeautifulSoup(subres.content, "html.parser")
                #latest section data
                aticleinfo=subsoup.find(class_='article-content')
                sentenceinfo = aticleinfo.select("p")
                content = ""
                for subsen in sentenceinfo:
                    # print("subsen=", subsen.get_text())
                    content = content + subsen.get_text() + "\n"

                nowtime = datetime.datetime.now()
                # mysql_lib.insert_crawtext("tcaticleinfo", data.get_text(), content, i['href'], "lastest data", nowtime)

                mysql_lib.insert_crawtext(table="crawtext",title=data.get_text(), title_cn="", url=i['href'], description=content,  \
                                    description_nohtml="", source_tag='web3', craw_status="-1-原始抓取", timestamp=nowtime)
    except Exception as exc:
        print("There was a problem: %s" %(exc))

def downsavemysql(title, suburl):
    subres = requests.get(suburl)
    subsoup=BeautifulSoup(subres.content, "html.parser")
    aticleinfo=subsoup.find(class_='article-content')
    sentenceinfo = aticleinfo.select("p")
    content = ""
    for subsen in sentenceinfo:
        # print("subsen=", subsen.get_text())
        content = content + subsen.get_text() + "\n"

    nowtime = datetime.datetime.now()
    mysql_lib.insert_crawtext(table="crawtext",title=title, title_cn="", url=suburl, description=content,  \
                                description_nohtml="", source_tag='news-ai', craw_status="-1-原始抓取", timestamp=nowtime)

def downspecifytag(title, href):
    time.sleep(0.2)
    downsavemysql(title, href);

def Parsetechcrunchcategory():
    res = requests.get("https://techcrunch.com/category/startups/")
    try:
        soup=BeautifulSoup(res.content, "html.parser")
        # find all tags
        tags = soup.find_all()
        for tag in tags:
        # find all href links
            # retdata = soup.find_all("div",attrs={"class":"wp-block-group uk-padding-small-left uk-padding-small-right is-layout-constrained wp-block-group-is-layout-constrained"})
            tmp = tag.find_all("a", attrs={"class":"post-block__title__link"}, href=True)
            for data in tmp:
                downspecifytag(data.get_text(), data['href'])
                # print("url=", data['href'], " title=", data.get_text())

    except Exception as exc:
        print("There was a problem: %s" %(exc))


if __name__ == '__main__':
    Parsetechcrunchcontent()
    Parsetechcrunchcategory()