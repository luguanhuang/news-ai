import requests,time
from bs4 import BeautifulSoup
import json
import io
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8'
}

def downloadhtml(url, filename):
    # url='https://www.datarobot.com/platform/audit-and-approve/'
    res = requests.get(url=url,headers=headers)
    res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
    html = res.text
    time.sleep(0.7)
    if res.status_code==200:
        print("成功了：{0}".format(url))
        with open(filename,"w",encoding="utf-8")as file:
            #将每页网页的内容存进listpage文件夹中
            file.write(html)

def ParseHtml(filename, titlesize):
    with open(filename, 'r', encoding="utf-8") as f:
        print("%s begin" % filename)
        soup = BeautifulSoup(f, 'html.parser')
        retdata = soup.find_all("div",attrs={"class":"wp-block-column is-vertically-aligned-center is-layout-flow wp-block-column-is-layout-flow"})
        for p in retdata:
            # print("p=", p)
            h1info = p.select(titlesize)
            # print("h4info=", h1info[0].get_text())
            # print("title----------len=", len(h1info))
            print("", h1info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            # print("h4info=", pinfo[0].get_text())
            print("", pinfo[1].get_text())

        retdata = soup.find_all("div",attrs={"class":"wp-block-group is-layout-flow wp-block-group-is-layout-flow"})
        for p in retdata:
            # print("p=", p)
            h5info = p.select("h5")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            print("", pinfo[0].get_text())


        retdata = soup.find_all("div",attrs={"class":"wp-block-media-text__content"})
        for p in retdata:
            h5info = p.select("h2")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            datainfo = len(pinfo)
            for i in range(datainfo):
                print("", pinfo[i].get_text())

        print("%s end" % filename)

# url='https://www.datarobot.com/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("webcontent"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
#         file.write(html)



def Parsewebcontent():
    # 从文件中读取 HTML 或 XML
    downloadhtml("https://www.datarobot.com/", "webcontent1")
    with open('webcontent1', 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        retdata = soup.find_all("div",attrs={"class":"wp-block-group uk-padding-small-left uk-padding-small-right is-layout-constrained wp-block-group-is-layout-constrained"})
        print("basic info begin")
        for p in retdata:
            h4info = p.select("h4")
            # print("h4info=", h4info[0].get_text())
            print("title----------")
            print("", h4info[0].get_text())
            pinfo = p.select("p")
            # print("h4info=", pinfo[0].get_text())
            print("content--------------")
            print("", pinfo[0].get_text())
        print("basic info end")


# url='https://www.datarobot.com/platform/deploy-and-run/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("deployandrun"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
        
#         file.write(html.replace(u'\xa0', u''))

def procdeploymentsaasurl():
    downloadhtml("https://www.datarobot.com/platform/deployment-saas/", "deploymentsaas")
    filename = "deploymentsaas"
    with open(filename, 'r', encoding="utf-8") as f:
        print("%s begin" % filename)
        soup = BeautifulSoup(f, 'html.parser')
        retdata = soup.find_all("h1",attrs={"id":"h-datarobot-ai-platform-deployment-infrastructure"})
        for p in retdata:
            print("title----------")
            print("",p.get_text())
        retdata = soup.find_all("p",attrs={"class":"has-text-align-center uk-text-subtitle"})
        print("content----------")
        print("",retdata[0].get_text())

        retdata = soup.find_all("div",attrs={"class":"wp-block-group uk-container-small uk-margin-xlarge-bottom dr-block-section-title uk-align-center is-layout-constrained wp-block-group-is-layout-constrained"})
        for p in retdata:
            h5info = p.select("h2")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            datainfo = len(pinfo)
            for i in range(datainfo):
                print("", pinfo[i].get_text())

        retdata = soup.find_all("div",attrs={"class":"wp-block-group dr-block-icon-title-text is-vertical is-content-justification-left is-layout-flex wp-container-core-group-layout-2 wp-block-group-is-layout-flex"})
        for p in retdata:
            h5info = p.select("h5")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            datainfo = len(pinfo)
            for i in range(datainfo):
                print("", pinfo[i].get_text())

        retdata = soup.find_all("div",attrs={"class":"wp-block-group dr-block-icon-title-text is-vertical is-content-justification-left is-layout-flex wp-container-core-group-layout-3 wp-block-group-is-layout-flex"})
        for p in retdata:
            h5info = p.select("h5")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            datainfo = len(pinfo)
            for i in range(datainfo):
                print("", pinfo[i].get_text())

        retdata = soup.find_all("div",attrs={"class":"wp-block-group dr-block-icon-title-text is-vertical is-content-justification-left is-layout-flex wp-container-core-group-layout-4 wp-block-group-is-layout-flex"})
        for p in retdata:
            h5info = p.select("h5")
            print("title----------")
            print("", h5info[0].get_text())
            pinfo = p.select("p")
            print("content--------------")
            datainfo = len(pinfo)
            for i in range(datainfo):
                print("", pinfo[i].get_text())

        retdata = soup.find_all("h6",attrs={"class":"wp-block-heading has-text-align-center uk-margin-small-bottom"})
        print("title----------")
        print("", retdata[0].get_text())

        retdata = soup.find_all("p",attrs={"has-text-align-center uk-margin-remove-top"})
        print("content----------")
        print("", retdata[0].get_text())

    # for p in retdata:
    #     h5info = p.select("h6")
    #     print("title----------")
    #     print("", h5info[0].get_text())
    #     pinfo = p.select("p")
    #     print("content--------------")
    #     datainfo = len(pinfo)
    #     for i in range(datainfo):
    #         print("", pinfo[i].get_text())

    print("%s end" % filename)
def ProcDatarobotUrl():
    downloadhtml("https://www.datarobot.com/platform/deploy-and-run/", "deployandrun1")
    ParseHtml("deployandrun1", "h1")

    downloadhtml("https://www.datarobot.com/platform/observe-and-intervene/", "observeandintervene1")
    ParseHtml("observeandintervene1", "h1")

    downloadhtml("https://www.datarobot.com/platform/learn-and-optimize/", "learnandoptimize1")
    ParseHtml("learnandoptimize1", "h1")

    downloadhtml("https://www.datarobot.com/platform/register-and-manage/", "registerandmanage1")
    ParseHtml("registerandmanage1", "h1")

    downloadhtml("https://www.datarobot.com/platform/audit-and-approve/", "auditandapprove1")
    ParseHtml("auditandapprove1", "h1")

    downloadhtml("https://www.datarobot.com/platform/document-and-comply/", "documentandcomply1")
    ParseHtml("documentandcomply1", "h1")


    downloadhtml("https://www.datarobot.com/platform/analyze-and-transform/", "analyzeandtransform1")
    ParseHtml("analyzeandtransform1", "h1")


    # downloadhtml("https://www.datarobot.com/platform/train-and-tune/", "trainandtune")
    ParseHtml("trainandtune", "h1")


    downloadhtml("https://www.datarobot.com/platform/compose-compare/", "composecompare")
    ParseHtml("composecompare", "h2")

    procintegrationsurl()
    procdeploymentsaasurl()

# with open('deployandrun1', 'r', encoding="utf-8") as f:
#     print("deploy and run begin")
#     soup = BeautifulSoup(f, 'html.parser')
#     retdata = soup.find_all("div",attrs={"class":"wp-block-column is-vertically-aligned-center is-layout-flow wp-block-column-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h1info = p.select("h1")
#         # print("h4info=", h1info[0].get_text())
#         print("title----------")
#         print("", h1info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         # print("h4info=", pinfo[0].get_text())
#         print("", pinfo[1].get_text())

#     retdata = soup.find_all("div",attrs={"class":"wp-block-group is-layout-flow wp-block-group-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h5info = p.select("h5")
#         print("title----------")
#         print("", h5info[0].get_text())
#         # print("", h1info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         # # print("h4info=", pinfo[0].get_text())
#         print("", pinfo[0].get_text())

#     retdata = soup.find_all("div",attrs={"class":"wp-block-media-text__content"})
#     for p in retdata:
#         h5info = p.select("h2")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         datainfo = len(pinfo)
#         for i in range(datainfo):
#             print("", pinfo[i].get_text())

#     print("deploy and run end")



# url='https://www.datarobot.com/platform/learn-and-optimize/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("learnandoptimize"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
#         file.write(html.replace(u'\xa0', u''))



# with open('learnandoptimize1', 'r', encoding="utf-8") as f:
#     print("learn and optimize begin")
#     soup = BeautifulSoup(f, 'html.parser')
#     retdata = soup.find_all("div",attrs={"class":"wp-block-column is-vertically-aligned-center is-layout-flow wp-block-column-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h1info = p.select("h1")
#         # print("h4info=", h1info[0].get_text())
#         print("title----------")
#         print("", h1info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         # print("h4info=", pinfo[0].get_text())
#         print("", pinfo[1].get_text())

#     retdata = soup.find_all("div",attrs={"class":"wp-block-group is-layout-flow wp-block-group-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h5info = p.select("h5")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         print("", pinfo[0].get_text())


#     retdata = soup.find_all("div",attrs={"class":"wp-block-media-text__content"})
#     for p in retdata:
#         h5info = p.select("h2")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         datainfo = len(pinfo)
#         for i in range(datainfo):
#             print("", pinfo[i].get_text())

#     print("learn and optimize end")


# url='https://www.datarobot.com/platform/observe-and-intervene/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("observeandintervene"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
#         file.write(html.replace(u'\xa0', u''))


# with open('observeandintervene1', 'r', encoding="utf-8") as f:
#     print("observe and intervene1 begin")
#     soup = BeautifulSoup(f, 'html.parser')
#     retdata = soup.find_all("div",attrs={"class":"wp-block-column is-vertically-aligned-center is-layout-flow wp-block-column-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h1info = p.select("h1")
#         # print("h4info=", h1info[0].get_text())
#         print("title----------")
#         print("", h1info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         # print("h4info=", pinfo[0].get_text())
#         print("", pinfo[1].get_text())

#     retdata = soup.find_all("div",attrs={"class":"wp-block-group is-layout-flow wp-block-group-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h5info = p.select("h5")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         print("", pinfo[0].get_text())


#     retdata = soup.find_all("div",attrs={"class":"wp-block-media-text__content"})
#     for p in retdata:
#         h5info = p.select("h2")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         datainfo = len(pinfo)
#         for i in range(datainfo):
#             print("", pinfo[i].get_text())

#     print("observe and intervene1 end")

# url='https://www.datarobot.com/platform/register-and-manage/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("registerandmanage"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
#         file.write(html.replace(u'\xa0', u''))



# with open('registerandmanage1', 'r', encoding="utf-8") as f:
#     print("observe and intervene1 begin")
#     soup = BeautifulSoup(f, 'html.parser')
#     retdata = soup.find_all("div",attrs={"class":"wp-block-column is-vertically-aligned-center is-layout-flow wp-block-column-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h1info = p.select("h1")
#         # print("h4info=", h1info[0].get_text())
#         print("title----------")
#         print("", h1info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         # print("h4info=", pinfo[0].get_text())
#         print("", pinfo[1].get_text())

#     retdata = soup.find_all("div",attrs={"class":"wp-block-group is-layout-flow wp-block-group-is-layout-flow"})
#     for p in retdata:
#         # print("p=", p)
#         h5info = p.select("h5")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         print("", pinfo[0].get_text())


#     retdata = soup.find_all("div",attrs={"class":"wp-block-media-text__content"})
#     for p in retdata:
#         h5info = p.select("h2")
#         print("title----------")
#         print("", h5info[0].get_text())
#         pinfo = p.select("p")
#         print("content--------------")
#         datainfo = len(pinfo)
#         for i in range(datainfo):
#             print("", pinfo[i].get_text())

#     print("observe and intervene1 end")


# url='https://www.datarobot.com/platform/audit-and-approve/'
# res = requests.get(url=url,headers=headers)
# res.encoding="UTF-8" #直接用requests 返回的Response对象的encoding属性调整编码
# html = res.text
# time.sleep(0.7)
# if res.status_code==200:
#     print("成功了：{0}".format(url))
#     with open("{0}".format("auditandapprove"+str(1)),"w",encoding="utf-8")as file:
#         #将每页网页的内容存进listpage文件夹中
#         file.write(html.replace(u'\xa0', u''))
