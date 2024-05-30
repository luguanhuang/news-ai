import datetime
import techcrunch
import businessinsider
import configparser
import os

if __name__ == '__main__':
    # print("112")
    i=1
    while True:
        conf = configparser.ConfigParser() # 类的实例化
        curpath = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(curpath,'config.ini')

        conf.read(path,encoding="utf-8")
        poll_interval = conf['CrawlerInfo']['poll_interval']
        print("poll_interval=", poll_interval)
        businessinsider.downloadbusi()
        techcrunch.Parsetechcrunchcontent()
        techcrunch.Parsetechcrunchcategory()

        time.sleep(poll_interval)