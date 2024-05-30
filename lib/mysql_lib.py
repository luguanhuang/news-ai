# import pymysql.cursors
# import requests
# import json
# import traceback

# from pymysql.converters import escape_string


# connection = None
# import logging
# logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def get_mysql_conn():
#     ip="localhost" 
#     global connection
#     try:
#         if connection == None:
#             dbName = 'crawlinfo'
#             connection = pymysql.connect(host=ip, port=3306, user='lgh', password='123456',use_unicode=True,
#                                         db=dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,autocommit=True)
#         return connection
#     except Exception as e:
#         traceback.print_exc()
#         logger.error(e)
#     #finally:
#         #return None

# def close_conn():
#     global connection
#     try:
#         if connection != None:
#             connection.close()
#     except Exception as e:
#         traceback.print_exc()
#         logger.error(e)
#     finally:
#         connection = None


# def insert_crawtext(table, title, content, url, type, timestamp):
#     insert_sql = """ INSERT INTO `{5}`( `title`, `content`,`url`, `type`, `timestamp`) VALUES ("{0}","{1}","{2}","{3}","{4}") """
#     insert_sql = insert_sql.format(escape_string(title), escape_string(content), escape_string(url), type,  timestamp, table)
#     logger.info("insert_crawtext:" + str(title))
#     connection = get_mysql_conn()
    
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(insert_sql)
#         connection.commit()
#     except Exception as e:
#         logger.error(insert_sql)
#         logger.error(e)
       

# #查询crawltext表中根据source_tag查询到所有url数据
# def query_crawtext_by_source_tag(table,source_tag):
#     connection = get_mysql_conn()
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT url FROM `{1}` WHERE source_tag = '{0}'".format(source_tag, table)
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             return result
#     except Exception as e:
#         logger.error(e)
#         return None




import pymysql.cursors
import requests
import json
import traceback

from pymysql.converters import escape_string


connection = None
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_mysql_conn():
    ip="bj-cdb-87yhecte.sql.tencentcdb.com" 
    global connection
    try:
        if connection == None:
            dbName = 'crawler'
            connection = pymysql.connect(host=ip, port=63565, user='crawler', password='crawler_ai_2024',use_unicode=True,
                                        db=dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,autocommit=True)
        return connection
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
    #finally:
        #return None

def close_conn():
    global connection
    try:
        if connection != None:
            connection.close()
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
    finally:
        connection = None

def query_crawtext_by_news_title(table, title):
    connection = get_mysql_conn()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT title FROM `{1}` WHERE title = '{0}'".format(escape_string(title), table)
            logger.info("query_crawtext_by_news_title:" + sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        logger.error("query_crawtext_by_news_title:"+e)
        # logger.error(e)
        return None

def insert_crawtext(table, title, title_cn, url, description, description_nohtml, source_tag, craw_status, timestamp):
    resdata = query_crawtext_by_news_title(table, title)
    cnt = 0
    if resdata is not None:
        cnt = len(resdata)

    insert_sql = ""
    if (cnt > 0):
        insert_sql = """ update `{7}` set url='{0}', description='{1}', description_nohtml='{2}', source_tag='{3}', craw_status='{4}', update_date='{5}' where title='{6}'"""
        insert_sql = insert_sql.format(escape_string(url), escape_string(description), escape_string(description_nohtml),  escape_string(source_tag),craw_status, timestamp, escape_string(title), table)
    else:

        insert_sql = """ INSERT INTO `{8}`( `title`, `title_cn`, `url`, `description`, `description_nohtml`, `source_tag`, `craw_status`, `timestamp`) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}") """
        insert_sql = insert_sql.format(escape_string(title), escape_string(title_cn), escape_string(url), escape_string(description), escape_string(description_nohtml),  escape_string(source_tag),craw_status, timestamp,table)

        # insert_sql = """ INSERT INTO `{7}`( `title`, `description`, `video_url`, `source_tag`, `create_date`, `update_date`, `id`) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}") """
        # insert_sql = insert_sql.format(escape_string(title), escape_string(description), escape_string(video_url), escape_string(source_tag),create_date, update_date, video_id, table)
    
    logger.info("insert_crawtext:" + insert_sql)
    connection = get_mysql_conn()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_sql)
        connection.commit()
    except Exception as e:
        logger.error(insert_sql)
        logger.error(e)
       

#查询crawltext表中根据source_tag查询到所有url数据
def query_crawtext_by_source_tag(table,source_tag):
    connection = get_mysql_conn()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT url FROM `{1}` WHERE source_tag = '{0}'".format(source_tag, table)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        logger.error(e)
        return None