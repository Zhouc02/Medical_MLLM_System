# -*- coding = utf-8 -*-
import json
import hashlib
import os
import random
import string
import subprocess
import uuid
from io import BytesIO
from zipfile import ZipFile

import redis
from datetime import datetime

import torch
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from pyhdfs import HdfsClient
from pymysql.converters import escape_string

import global_config
from Medical_LLM.settings import mysql_pool


@csrf_exempt
def login(request):
    if request.method == 'POST':
        request_params = json.loads(request.body.decode('utf-8'))
        name = request_params.get('username')
        password = request_params.get('password')
        connection = mysql_pool.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id, password, auth from staff where name = '{}';".format(name))
                result = cursor.fetchall()
                if result:
                    hex_pass = hashlib.md5()
                    hex_pass.update(password.encode())
                    password = hex_pass.hexdigest()
                    if result[0][1] == password:
                        data = {'id': result[0][0], 'name': name, 'auth': result[0][2]}
                        now = datetime.now()
                        add_time = now.strftime("%Y.%m.%d %H:%M")
                        if result[0][2] == 'D':
                            global_config.send_log(f"doctor|{name}|Login|{add_time}")
                        else:
                            global_config.send_log(f"system|{name}|Login|{add_time}")
                    else:
                        data = {'id': '', 'name': '', 'auth': 'W'}
                else:
                    data = {'id': '', 'name': '', 'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def manager_check(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from staff;")
                result = cursor.fetchall()
                data = [{'id': id, 'name': name, 'auth': '管理员' if auth == 'A' else '医师'} for
                        id, name, password, auth in result]
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def manager_add(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        name = request_params.get('name')
        password = request_params.get('password')
        auth = request_params.get('auth')
        hex_pass = hashlib.md5()
        hex_pass.update(password.encode())
        password = hex_pass.hexdigest()
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(
                    "insert into staff(name,password,auth) values ('{}', '{}', '{}');".format(name, password, auth))
                connection.commit()
                if result > 0:
                    data = {'auth': 'Y'}
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|manager_add|{name}|{add_time}")
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def manager_delete(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        id = request_params.get('id')
        try:
            with connection.cursor() as cursor:
                result = cursor.execute("delete from staff where id = {};".format(id))
                connection.commit()
                if result > 0:
                    data = {'auth': 'Y'}
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|manager_delete|{id}|{add_time}")
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def manager_update(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        id = request_params.get('id')
        name = request_params.get('name')
        password = request_params.get('password')
        auth = request_params.get('auth')
        hex_pass = hashlib.md5()
        hex_pass.update(password.encode())
        password = hex_pass.hexdigest()
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(
                    "update staff set name = '{}', password = '{}', auth = '{}' where id = {};".format(name, password,
                                                                                                       auth, id))
                connection.commit()
                if result > 0:
                    data = {'auth': 'Y'}
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|manager_update|{id}|{add_time}")
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        name = request.POST.get('name')
        self_id = request.POST.get('self_id')
        image_file = request.FILES.get('image')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        token = f'{timestamp}_{get_random_string(length=6)}'
        fs = FileSystemStorage(location='images')
        file_name = f'{token}.png'
        fs.save(file_name, image_file)
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(
                    "insert into patient values ('{}', '{}', '{}', 'N');".format(token, name, self_id))
                connection.commit()
                redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                                 password='12345678')
                redis_client.set(token, "Ready")
                if result > 0:
                    data = {'token': token}
                else:
                    data = {'token': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def generate(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        token = request_params.get('token')
        record = request_params.get('record')
        id = request_params.get('id')
        image_path = f"/public/home/medical_2324/Medical_LLM/images/{token}.png"
        record_path = f"/public/home/medical_2324/Medical_LLM/records/{token}.txt"
        with open(record_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(record))
        hdfs = HdfsClient(hosts='localhost:50053')  # 50070
        hdfs.copy_from_local(image_path, f'/backup/images/{token}.png')
        hdfs.copy_from_local(record_path, f'/backup/record/{token}.txt')
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        redis_client.delete(token)
        try:
            with connection.cursor() as cursor:
                result = cursor.execute("update patient set text_path='Y' where token='{}';".format(token))
                connection.commit()
                if result > 0:
                    data = {'auth': 'Y'}
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"doctor|{id}|{token}|{add_time}")
                    torch.cuda.empty_cache()
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def history_list(request):
    if request.method == 'POST':
        param = json.loads(request.body.decode('utf-8'))
        self_id = param.get('self_id')
        print(self_id)
        connection = mysql_pool.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("select token, text_path from patient where self_id = '{}';".format(self_id))
                result = cursor.fetchall()
                if result:
                    data = [{'token': token, 'text_path': '已生成' if text_path == 'Y' else '未生成'} for
                            token, text_path in result]
                else:
                    data = [{'token': 'W'}]
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def special_record(request):
    if request.method == 'POST':
        param = json.loads(request.body.decode('utf-8'))
        token = param.get('token')
        image_path = f"/public/home/medical_2324/Medical_LLM/images/{token}.png"
        record_path = f"/public/home/medical_2324/Medical_LLM/records/{token}.txt"
        with open(image_path, 'rb') as file1, open(record_path, 'rb') as file2:
            content1 = file1.read()
            content2 = file2.read()
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zipfile:
            zipfile.writestr(f'{token}.png', content1)
            zipfile.writestr(f'{token}.txt', content2)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="multiple_files.zip"'
        return response


@csrf_exempt
def patient_check(request):
    if request.method == 'POST':
        request_params = json.loads(request.body.decode('utf-8'))
        action = request_params.get('action')
        connection = mysql_pool.connection()
        if action == 'C':
            try:
                with connection.cursor() as cursor:
                    cursor.execute("select token,name,self_id,text_path from patient;")
                    result = cursor.fetchall()
                    data = [{'token': token, 'name': name, 'self_id': self_id,
                             'text_path': '已生成' if text_path == 'Y' else '未生成'} for
                            token, name, self_id, text_path in result]
                    return HttpResponse(json.dumps(data), status=200)
            finally:
                connection.close()
        elif action == 'D':
            token = request_params.get('token')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("select text_path from patient where token='{}';".format(token))
                    result = cursor.fetchall()
                    if result[0][0] == 'N':
                        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                                         password='12345678')
                        redis_client.delete(token)
                        result = cursor.execute("delete from patient where token='{}';".format(token))
                        connection.commit()
                        if result > 0:
                            os.remove(f'/public/home/medical_2324/Medical_LLM/images/{token}.png')
                            now = datetime.now()
                            add_time = now.strftime("%Y.%m.%d %H:%M")
                            global_config.send_log(f"system|patient_check_delete|{token}|{add_time}")
                            data = {'auth': 'Y'}
                        else:
                            data = {'auth': 'W'}
                        return HttpResponse(json.dumps(data), status=200)
                    else:
                        result = cursor.execute("delete from patient where token = '{}';".format(token))
                        connection.commit()
                        if result > 0:
                            os.remove(f'/public/home/medical_2324/Medical_LLM/images/{token}.png')
                            os.remove(f'/public/home/medical_2324/Medical_LLM/records/{token}.txt')
                            hdfs = HdfsClient(hosts='localhost:50053')
                            hdfs.delete(f'/backup/images/{token}.png')
                            hdfs.delete(f'/backup/record/{token}.txt')
                            now = datetime.now()
                            add_time = now.strftime("%Y.%m.%d %H:%M")
                            global_config.send_log(f"system|patient_check_delete|{token}|{add_time}")
                            data = {'auth': 'Y'}
                        else:
                            data = {'auth': 'W'}
                        return HttpResponse(json.dumps(data), status=200)
            finally:
                connection.close()
        else:
            return HttpResponse(json.dumps({'auth': 'W'}), status=200)


@csrf_exempt
def redis_clear(request):
    if request.method == 'POST':
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, password='12345678')
        count_before = redis_client.dbsize()
        redis_client.flushall()
        count_after = redis_client.dbsize()
        data = {'count': count_before - count_after}
        now = datetime.now()
        add_time = now.strftime("%Y.%m.%d %H:%M")
        global_config.send_log(f"system|redis_clear|{count_before - count_after}|{add_time}")
        return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def manager_search(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        id = request_params.get('id')
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id, name, auth from staff where id = {};".format(int(id)))
                result = cursor.fetchall()
                if result:
                    data = [{'id': id, 'name': result[0][1], 'auth': '管理员' if result[0][2] == 'A' else '医师'}]
                else:
                    data = [{'auth': 'W'}]
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def patient_search(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_params = json.loads(request.body.decode('utf-8'))
        self_id = request_params.get("self_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute("select token, name,self_id,text_path from patient where self_id='{}'".format(self_id))
                result = cursor.fetchall()
                if result:
                    data = [{'token': token, 'name': name, 'self_id': self_id,
                             'text_path': '已生成' if text_path == 'Y' else '未生成'}
                            for token, name, self_id, text_path in result]
                else:
                    data = [{'token': 'W'}]
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def dialogue_check(request):
    if request.method == 'POST':
        request_params = json.loads(request.body.decode('utf-8'))
        connection = mysql_pool.connection()
        action = request_params.get('action')
        try:
            if action == 'C':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select distinct from_id,name from feedback, staff where feedback.from_id=staff.id and staff.auth='D';")
                    result = cursor.fetchall()
                    if result:
                        data = [{'id': from_id, 'name': name} for from_id, name in result]
                        return HttpResponse(json.dumps(data), status=200)
            elif action == 'S':
                doctor_id = request_params.get('id')
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select * from feedback where from_id={} or to_id={};".format(int(doctor_id), int(doctor_id)))
                    result = cursor.fetchall()
                    if result:
                        data = [{'from_id': from_id, 'to_id': to_id, 'content': content, 'add_time': add_time}
                                for from_id, to_id, content, add_time in result]
                        return HttpResponse(json.dumps(data), status=200)
            elif action == 'I':
                from_id = request_params.get('from_id')
                to_id = request_params.get('to_id')
                content = request_params.get('content')
                now = datetime.now()
                add_time = now.strftime("%Y年%m月%d日%H:%M")
                with connection.cursor() as cursor:
                    result = cursor.execute(
                        "insert into feedback values ({},{},'{}','{}');".format(int(from_id), int(to_id), content,
                                                                                add_time))
                    connection.commit()
                    if result > 0:
                        data = {'auth': 'Y'}
                    else:
                        data = {'auth': 'W'}
                    return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def doctor_help(request):
    if request.method == 'POST':
        request_params = json.loads(request.body.decode('utf-8'))
        connection = mysql_pool.connection()
        action = request_params.get('action')
        try:
            if action == 'C':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select name,content,add_time from staff,doctor_help where staff.id=doctor_help.from_id;")
                    result = cursor.fetchall()
                    if result:
                        data = [{'name': name, 'content': content, 'add_time': add_time} for name, content, add_time in
                                result]
                        return HttpResponse(json.dumps(data), status=200)
            elif action == 'I':
                from_id = request_params.get('from_id')
                content = request_params.get('content')
                now = datetime.now()
                add_time = now.strftime("%Y年%m月%d日%H:%M")
                with connection.cursor() as cursor:
                    result = cursor.execute(
                        "insert into doctor_help values ({},'{}','{}');".format(int(from_id), content, add_time))
                    connection.commit()
                    if result > 0:
                        data = {'auth': 'Y'}
                    else:
                        data = {'auth': 'W'}
                    return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def log_list(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        action = params.get('action')
        hdfs = HdfsClient(hosts='localhost:50053')
        if action == 'C':
            logs = hdfs.listdir('/django')
            data = []
            for log in logs:
                status = hdfs.get_file_status('/django/' + log)
                size = status.length / 1024
                data.append({'log_name': log, 'log_size': size})
            return HttpResponse(json.dumps(data), status=200)
        elif action == 'S':
            log_name = params.get('log_name')
            with hdfs.open('/django/' + log_name) as file:
                content = file.read().decode('utf-8')
            data = {'content': content}
            return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def hive_analysis(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        action = params.get('action')
        hdfs = HdfsClient(hosts='localhost:50053')
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        connection = mysql_pool.connection()
        if action == 'C':  # 初始化分析环境，仅Hive使用
            log_name = params.get('log_name')
            try:
                hdfs.copy_to_local(f'/django/{log_name}', f'/public/home/medical_2324/Medical_LLM/logs/{log_name}')
                letters = string.ascii_letters
                table_name = ''.join(random.choice(letters) for _ in range(8))
                table_name = f'logbase{table_name}'
                # 创建临时Hive表，将日志导入临时Hive表中，并在Redis设置标识符，表示有临时表的存在
                redis_client.set('hive_table', table_name)
                subprocess.run(
                    f'hive -e "use logger; create table {table_name}(type string,executor string,content string,add_time string) row format delimited fields terminated by \'|\';"',
                    shell=True, check=True)
                subprocess.run(
                    f'hive -e "use logger; load data local inpath \'/public/home/medical_2324/Medical_LLM/logs/{log_name}\' into table {table_name};"',
                    shell=True, check=True)
                os.remove(f'/public/home/medical_2324/Medical_LLM/logs/{log_name}')
                data = {'table_name': table_name}
                return HttpResponse(json.dumps(data), status=200)
            except subprocess.CalledProcessError as e:
                data = {'table_name': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        elif action == 'S':  # 提交SQL，仅Hive使用
            sql = params.get('sql')
            job_id = str(uuid.uuid4())[:20]
            now = datetime.now()
            add_time = now.strftime("%Y年%m月%d日%H:%M")
            with connection.cursor() as cursor:
                result = cursor.execute(
                    "insert into log_analysis(job_id, add_time, result, content, type) values ('{}','{}','N','N','Hive');".format(
                        job_id, add_time))
                connection.commit()
            if result:
                # 找个时间修改为异步执行
                global_config.submit_job(sql, job_id)
                data = {'job_id': job_id}
                add_time = now.strftime("%Y.%m.%d %H:%M")
                global_config.send_log(f"system|Hive_analysis|{job_id}|{add_time}")
                connection.close()
                return HttpResponse(json.dumps(data), status=200)
        elif action == 'R':  # 轮询结果，Hive和MapReduce通用
            job_id = params.get('job_id')
            with connection.cursor() as cursor:
                cursor.execute("select result, content from log_analysis where job_id='{}';".format(job_id))
                result = cursor.fetchall()
                data = {'result': result[0][0], 'content': result[0][1]}
                connection.close()
                return HttpResponse(json.dumps(data), status=200)
        elif action == 'X':  # 关闭环境，仅Hive使用
            # 从Redis中找到临时Hive表，将其删除，然后删除Redis标识符
            hive_table = redis_client.get("hive_table")
            subprocess.run(f'hive -e "use logger; drop table {hive_table};"', shell=True, check=True)
            redis_client.delete("hive_table")
            data = {'auth': 'Y'}
            return HttpResponse(json.dumps(data), status=200)
        elif action == 'L':  # Hive和MapReduce通用
            with connection.cursor() as cursor:
                cursor.execute("select job_id,add_time,type,result from log_analysis;")
                result1 = cursor.fetchall()
                data = [{'job_id': job_id, 'add_time': add_time, 'type': types,
                         'result': '未完成' if result == 'N' else '已结束' if result == 'Y' else '执行错误'}
                        for job_id, add_time, types, result in result1]
                connection.close()
                return HttpResponse(json.dumps(data), status=200)
        elif action == 'N':  # 前端需要进行type的判断，查询具体的命令和结果，Hive和MapReduce通用
            job_id = params.get('job_id')
            with connection.cursor() as cursor:
                cursor.execute("select content, hive_sql from log_analysis where job_id='{}';".format(job_id))
                result = cursor.fetchall()
                data = {'content': result[0][0], 'sql': result[0][1]}
                connection.close()
                return HttpResponse(json.dumps(data), status=200)
        elif action == 'D':  # Hive和MapReduce通用
            job_id = params.get('job_id')
            with connection.cursor() as cursor:
                result = cursor.execute("delete from log_analysis where job_id='{}';".format(job_id))
                connection.commit()
                if result:
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|analysis_delete|{job_id}|{add_time}")
                    data = {'auth': 'Y'}
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def mapreduce_analysis(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        action = params.get('action')
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        hdfs = HdfsClient(hosts='localhost:50053')
        connection = mysql_pool.connection()
        if action == 'C':
            log_name = params.get('log_name')
            hdfs.copy_to_local(f'/django/{log_name}', f'/public/home/medical_2324/Medical_LLM/logs/{log_name}')
            letters = string.ascii_letters
            file_name = ''.join(random.choice(letters) for _ in range(8))
            file_name = f'django-{file_name}.log'
            # 创建临时文件，重命名再上传，Redis设置标识符
            redis_client.set('hdfs_file', file_name)
            os.rename(f'/public/home/medical_2324/Medical_LLM/logs/{log_name}',
                      f'/public/home/medical_2324/Medical_LLM/logs/{file_name}')
            hdfs.copy_from_local(f'/public/home/medical_2324/Medical_LLM/logs/{file_name}', f'/{file_name}')
            os.remove(f'/public/home/medical_2324/Medical_LLM/logs/{file_name}')
            data = {'auth': 'Y'}
            connection.close()
            return HttpResponse(json.dumps(data), status=200)
        elif action == 'S':
            mapper = params.get('map')
            reducer = params.get('reduce')
            file_name = redis_client.get('hdfs_file')
            with open('/public/home/medical_2324/Medical_LLM/logs/mapper.py', 'w', encoding='utf-8') as f:
                f.write(mapper)
            with open('/public/home/medical_2324/Medical_LLM/logs/reducer.py', 'w', encoding='utf-8') as f:
                f.write(reducer)
            job_id = str(uuid.uuid4())[:20]
            sql = mapper + ':::' + reducer
            now = datetime.now()
            add_time = now.strftime("%Y年%m月%d日%H:%M")
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into log_analysis(job_id, add_time, result, content, type) values ('{}','{}','N','N','MapReduce');".format(
                        job_id, add_time))
                connection.commit()
            # 找个时间改成异步执行
            try:
                subprocess.run(f'hadoop jar /public/home/medical_2324/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
                                            -D stream.non.zero.exit.is.failure=false \
                                            -D mapred.map.tasks=1 \
                                            -D mapred.reduce.tasks=1 \
                                            -files /public/home/medical_2324/Medical_LLM/logs/mapper.py,/public/home/medical_2324/Medical_LLM/logs/reducer.py \
                                            -input /{file_name} \
                                            -output /mapreduce/temp \
                                            -mapper "python mapper.py" \
                                            -reducer "python reducer.py"', shell=True, text=True, check=True,
                               capture_output=True)
                with hdfs.open('/mapreduce/temp/part-00000') as file:
                    content = file.read().decode('utf-8')
                hdfs.delete('/mapreduce', recursive=True)
                sql = escape_string(sql)
                with connection.cursor() as cursor:
                    cursor.execute(
                        "update log_analysis set result='Y', content = '{}',hive_sql='{}' where job_id = '{}';".format(
                            content, sql, job_id))
                    connection.commit()
            except subprocess.CalledProcessError as e:
                content = e.stderr
                with connection.cursor() as cursor:
                    cursor.execute(
                        "update log_analysis set result='W', content = '{}',hive_sql='{}' where job_id = '{}';".format(
                            content, sql, job_id))
                    connection.commit()
            finally:
                connection.close()
            data = {'job_id': job_id}
            add_time = now.strftime("%Y.%m.%d %H:%M")
            global_config.send_log(f"system|MapReduce_analysis|{job_id}|{add_time}")
            return HttpResponse(json.dumps(data), status=200)
        elif action == 'X':
            file_name = redis_client.get('hdfs_file')
            hdfs.delete(f'/{file_name}')
            os.remove('/public/home/medical_2324/Medical_LLM/logs/mapper.py')
            os.remove('/public/home/medical_2324/Medical_LLM/logs/reducer.py')
            redis_client.delete('hdfs_file')
            data = {'auth': 'Y'}
            return HttpResponse(json.dumps(data), status=200)
