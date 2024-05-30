# -*- coding: utf-8 -*-
import json
import os
import traceback
import threading
import redis
import time
import requests
import re
# 从twitter search中获取信息，加上username等渠道来源到bloomfilter中判断去重，最后翻译中文，最后存入redis(固定长度)和es中。
from urllib import parse
from lib import mysql_lib

from github import Github
# Authentication is defined via github.Auth
from github import Auth
from bs4 import BeautifulSoup
# using an access token
import unicodedata


import datetime

from flask_basicauth import BasicAuth
from flask import Flask, request, make_response
app = Flask(__name__)

rss_scrapy = None

dbRedis = None
redis_host = None
path_and_redis_key = '/marketdata/crypto/news/rssfeed'

appType = os.getenv("appType") if os.getenv("appType") is not None else "github"
userName = os.getenv("userName") if  os.getenv("userName") is not None else "admin"
passWord = os.getenv("passWord") if  os.getenv("passWord") is not None else "Ai_Service_2022"
redis_host = os.getenv("redisHost") if os.getenv("redisHost") is not None else "172.31.46.59"
is_notify = ((os.getenv("isNotify") if os.getenv("isNotify") is not None else "False") == "True")
interval = os.getenv("interval") if  os.getenv("interval") is not None else 21600
maxCount = os.getenv("maxCount") if  os.getenv("maxCount") is not None else 2
sourceTag = os.getenv("sourceTag") if  os.getenv("sourceTag") is not None else "Github"
sourceData = os.getenv("sourceData") if  os.getenv("sourceData") is not None else "llm"
sortBy = os.getenv("sortBy") if  os.getenv("sortBy") is not None else "stars"


def get_redis_conn():
    global dbRedis
    if dbRedis == None:
        #pubIp = commonLib.get_self_public_ip()
        pool = redis.ConnectionPool(host=redis_host, port=6379, db=0, password='mozi2022',decode_responses=True)
        dbRedis = redis.Redis(connection_pool=pool)
    return dbRedis

def lib_bloomfilter_insert(data, port=9510):
    url = 'http://'+redis_host+':'+str(port)+'/lib/bloomfilter'
    reqJsonData = {
        "type": "bloomfilter_insert",
        "data": data
    }
    resp = requests.post(url, auth=('admin', 'Ai_Service_2022'), json=reqJsonData,  timeout=10)
    respJsonData = json.loads(resp.text)
    return respJsonData

def lib_bloomfilter_contains(data, port=9510):
    url = 'http://'+redis_host+':'+str(port)+'/lib/bloomfilter'
    reqJsonData = {
        "type": "bloomfilter_contains",
        "data": data
    }
    resp = requests.post(url, auth=('admin', 'Ai_Service_2022'), json=reqJsonData,  timeout=30)
    respJsonData = json.loads(resp.text)
    return respJsonData['data']



def lib_send_email(subject, content, source):
    url = 'http://'+redis_host+':9520/lib/notification'
    reqJsonData = {
        "type": "email",
        "data": {"subject":subject, "content":content, "source":source}
    }
    resp = requests.post(url, auth=('admin', 'Ai_Service_2022'), json=reqJsonData,  timeout=30)
    print('发送邮件结果:' + str(resp))
    respJsonData = json.loads(resp.text)
    return respJsonData


def remmove_m_char(text, replace_str="   "):
    return text.replace(replace_str, "")

def remove_empty_lines(text):
    pattern = r"\n\s*\n"  # 匹配连续的空行
    return re.sub(pattern, "\n", text)

def remove_markup(text):
    # 去除加粗标签
    text = re.sub(r'\*\*(.*)\*\*', r'\1', text)
    # 去除斜体标签
    text = re.sub(r'_(.*)_', r'\1', text)
    # 去除链接标签
    text = re.sub(r'\[(.*)\]\((.*)\)', r'\1', text)
    return text

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
    clean = re.compile('<.*?>') # 定义正则表达式，匹配所有HTML标签
    text = re.sub(clean, '', text) # 
    text = remove_markup(text)
    text = unicodedata.normalize("NFKD", text)
    text = remove_empty_lines(text)
    text= text.strip()
    text = remmove_m_char(text, replace_str="   ")
    text = remmove_m_char(text, replace_str="----")
    return text

#max_wait_times = 1
#先获取twitter一个小时以前的消息，并将其加入到redis队列和固定列表中，然后每隔一段时间查找一下最新的消息
def fetch_github_task(interval, source_tag,source_data,  sort_by, order, max_fetch):
    global dbRedis,max_wait_times
    
    print("query 字符串:", str( source_data ) )

    while True :
        sequence_order = "3" # 为了重新抓取，所以设置为2
        #max_wait_times = max_wait_times -1
        try:
            result = search_github(query_data=str( source_data ), sort_by=sort_by, order=order, max_count=max_fetch)

            print("避免重复抓取，首先从数据中查询所有url，然后用lib_bloomfilter_insert插入到bloomfilter中")
            url_list = mysql_lib.query_crawtext_by_source_tag(table="crawcontent",source_tag=source_tag)
            for url in url_list:
                lib_bloomfilter_insert(str(url) + "-" + sequence_order)
                
            #同时遍历 result中的key和value
            for key, value in result.items():
                url = "https://github.com/" + key
                if lib_bloomfilter_contains(str(url) + "-" + sequence_order) == True :
                    print("key:{}存在，不放入缓存队列".format(url))
                else:
                    now = datetime.datetime.now()
                    now = now.strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        title= value["description"].split('.')[0] + "." + key
                        content = value["description"] + "\r\n" + value['README.md']
                        # 使用正则表达式 删除 content中的url html标签等
                        content_no_html = remove_html_tags(content)
                        
                        mysql_lib.insert_crawtext(table="crawcontent",title=title, title_cn="", url=url, description=content,  \
                                description_nohtml=content_no_html, source_tag=sourceTag, craw_status="-1-原始抓取", timestamp=now )
                        
                        lib_bloomfilter_insert(str(url) + "-" + sequence_order)
                    except Exception as e:
                        print("处理内容并插入到mysql失败:" + str(e))
                        traceback.print_exc()
                        continue    
            time.sleep(int(interval))
        except Exception as e:
            dbRedis = None
            traceback.print_exc()
            print(e)
            time.sleep( 15 )
            dbRedis = get_redis_conn()


# @app.route(path_and_redis_key, methods=['POST'])
# def market_twitter():
#     dictResult = {'success': 'false', 'msg': 'ok', 'data': ''}
#     try:
#         if request.method == 'POST':
#             a = request.get_data()
#             req_json = json.loads(a)
#             result = 'None'
#             type = req_json['type']
#             if type=='byusername':
#                 is_realtime = req_json['is_realtime']
#                 if is_realtime == "True":
#                     data = req_json['data']
#                     monitor_hours = (int)(req_json['monitor_hours'])
#                     max_fetch = (int)(req_json['max_fetch'])
#                     #result = get_twitter_by_user(data=data, monitorHours=monitor_hours, maxFetch= max_fetch)
#                 else:
#                     result = "不支持的is_realtime:" + is_realtime    
#             elif type=='bykeywords':
#                 is_realtime = req_json['is_realtime']
#                 if is_realtime == "True":
#                     data = req_json['data']
#                     monitor_hours = (int)(req_json['monitor_hours'])
#                     max_fetch = (int)(req_json['max_fetch'])
#                     #result = get_twitter_by_keywords(data=data, monitorHours=monitor_hours, maxFetch= max_fetch)
#                 else:
#                     result = "不支持的is_realtime:" + is_realtime   
#             else:
#                 result = "不支持的Type:" + type

#             dictResult['success'] = 'true'
#             dictResult['data'] = result
#         else:
#             dictResult['success'] = 'false'
#             dictResult['msg'] = '只接受post请求'

#         return json.dumps(dictResult,indent=4,ensure_ascii=False)
#     except Exception as e:
#         traceback.print_exc()
#         dictResult['success'] = 'false'
#         dictResult['msg'] = str(e)
#         return json.dumps(dictResult,indent=4,ensure_ascii=False)
#     finally:
#         print(dictResult)

if __name__ == '__main__':
    # app.config['BASIC_AUTH_FORCE'] = True
    # app.config['BASIC_AUTH_USERNAME'] = userName if userName is not None else "admin"
    # app.config['BASIC_AUTH_PASSWORD'] = passWord if passWord is not None else "Ai_Service_2022"
    # basic_auth = BasicAuth(app)

    #fetch_rss_task = threading.Thread(target=interval_fetch_github_task, args=(interval, sourceData,  sortBy, "desc", maxCount))  
    #fetch_rss_task.start()
    fetch_github_task(interval=interval, source_tag=sourceTag, source_data=sourceData,  sort_by=sortBy, order="desc", max_fetch=maxCount)
    
    #app.run(host="0.0.0.0", port=9250, debug=True)

