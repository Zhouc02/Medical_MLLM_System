# -*- coding = utf-8 -*-
# ========全局参数与方法设置=======
import logging
import os
import subprocess

import pymysql
from dbutils.pooled_db import PooledDB

native_ip_address = 'localhost'

# mysql数据库设置
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = '12345678'
mysql_database = 'medical'

# 模型参数设置
LLM_max_length = 2048
LLM_top_p = 0.4
LLM_top_k = 100
LLM_temperature = .8


def get_model_size(path, model_size_list):
    fileList = os.listdir(path)  # 获取path目录下所有文件
    for filename in fileList:
        pathTmp = os.path.join(path, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 判断是否为目录
            get_model_size(pathTmp, model_size_list)  # 是目录就继续递归查找
        elif os.path.isfile(pathTmp):  # 判断是否为文件
            filesize = os.path.getsize(pathTmp)  # 如果是文件，则获取相应文件的大小
            model_size_list.append(filesize)  # 将文件的大小添加到列表
    return model_size_list


def send_log(message):
    logger = logging.getLogger('my_app_logger')
    logger.info(message)


def submit_job(sql, job_id):
    mysql_pool = PooledDB(pymysql, 5, host=mysql_host,
                          user=mysql_user,
                          password=mysql_password,
                          db=mysql_database)
    connection = mysql_pool.connection()
    try:
        result = subprocess.run(f'hive -e "use logger;{sql}"', shell=True,
                                check=True, capture_output=True, text=True)
        content = result.stdout
        with connection.cursor() as cursor:
            cursor.execute(
                "update log_analysis set result='Y', content = '{}',hive_sql='{}' where job_id = '{}';".format(content, sql, job_id))
            connection.commit()
    except subprocess.CalledProcessError as e:
        content = e.stderr
        with connection.cursor() as cursor:
            cursor.execute(
                "update log_analysis set result='W', content = '{}',hive_sql='{}' where job_id = '{}';".format(content, sql, job_id))
            connection.commit()
    finally:
        connection.close()
