# -*- coding = utf-8 -*-
import json
import ast
import os
import shutil
import subprocess
from datetime import datetime

import psutil
import redis
import torch
import GPUtil
from django.apps import apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import global_config
from VisualGLM.model.chat import chat
from Medical_LLM.settings import mysql_pool
from pyhdfs import HdfsClient


@csrf_exempt
def talk(request):
    if request.method == 'POST':
        request_params = json.loads(request.body.decode('utf-8'))
        auto_generate = request_params.get('auto_generate')
        token = request_params.get('token')
        query = request_params.get('query')
        Model_Config = apps.get_app_config('Medical_LLM')
        model = Model_Config.model
        tokenizer = Model_Config.tokenizer
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        top_p = redis_client.get('top_p')
        top_k = redis_client.get('top_k')
        temperature = redis_client.get('temperature')
        pic = f"/public/home/medical_2324/Medical_LLM/images/{token}.png"
        if auto_generate == 'Y':
            auto_query = [f'{query}请诊断存在哪些病症？']
            with torch.no_grad():
                auto_history = None
                auto_cache_image = None
                auto_output = []
                for auto_ask in auto_query:
                    try:
                        auto_response, auto_history, auto_cache_image = chat(
                            pic,
                            model,
                            tokenizer,
                            auto_ask,
                            history=auto_history,
                            image=auto_cache_image,
                            max_length=global_config.LLM_max_length,
                            top_p=float(top_p),
                            temperature=float(temperature),
                            top_k=int(top_k),
                            english=False,
                            invalid_slices=[]
                        )
                    except Exception as e:
                        print(e)
                    pic = None
                    auto_output.append(auto_response.split('答：')[-1].strip())
                data = {'output': auto_output}
                torch.cuda.empty_cache()
                return HttpResponse(json.dumps(data), status=200)
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, password='12345678')
        history = redis_client.get(token)
        if history == "Ready":
            history = None
        else:
            history = ast.literal_eval(history)
        with torch.no_grad():
            response, history, cache_image = chat(
                pic,
                model,
                tokenizer,
                query,
                history=history,
                image=None,
                max_length=global_config.LLM_max_length,
                top_p=float(top_p),
                temperature=float(temperature),
                top_k=int(top_k),
                english=False,
                invalid_slices=[]
            )
            redis_client.set(token, str(history))
            data = {'output': response.split('答：')[-1].strip()}
            return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def monitor(request):
    if request.method == 'POST':
        gpu_allocated_memory = torch.cuda.memory_allocated() / (1024 ** 3)  # GPU分配
        gpu_cached_memory = torch.cuda.memory_cached() / (1024 ** 3)  # GPU缓存
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_info = process.memory_info().rss / (1024 ** 3)  # 内存占用
        cpu_percent = process.cpu_percent(interval=1)  # CPU占用
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, password='12345678')
        count_history = redis_client.dbsize()  # Redis主键数量
        gpus = GPUtil.getGPUs()
        gpu = gpus[0]
        gpu_total = gpu.memoryTotal  # GPU显存总大小
        gpu_free = gpu.memoryFree  # GPU显存可用大小
        gpu_used = gpu.load * 100  # GPU使用率
        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024 ** 3)  # 内存总大小
        available_memory = memory.available / (1024 ** 3)  # 内存可用大小

        try:
            redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, password='12345678')
            redis_current = 1
        except Exception as e:
            redis_current = 0

        try:
            connection = mysql_pool.connection()
            mysql_current = 1
        except Exception as e:
            mysql_current = 0

        try:
            hdfs = HdfsClient(hosts='localhost:50053')
            hdfs_current = 1
        except Exception as e:
            hdfs_current = 0

        data = {'allocated': gpu_allocated_memory, 'cached': gpu_cached_memory, 'mem': memory_info, 'cpu': cpu_percent,
                'count': count_history, 'gpu_total': gpu_total, 'gpu_free': gpu_free, 'gpu_used': gpu_used,
                'total_mem': total_memory,
                'avail_mem': available_memory, 'redis_c': redis_current, 'mysql_c': mysql_current, 'hdfs_c': hdfs_current}
        return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def clear(request):
    if request.method == 'POST':
        before_allocated_memory = torch.cuda.memory_allocated() / (1024 ** 3)
        before_cached_memory = torch.cuda.memory_cached() / (1024 ** 3)
        torch.cuda.empty_cache()
        after_allocated_memory = torch.cuda.memory_allocated() / (1024 ** 3)
        after_cached_memory = torch.cuda.memory_cached() / (1024 ** 3)
        diff_allocated = before_allocated_memory - after_allocated_memory
        diff_cached = before_cached_memory - after_cached_memory
        data = {'clear_alloc': diff_allocated, 'clear_cached': diff_cached}
        return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def model_list(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from model;")
                result = cursor.fetchall()
                if result:
                    data = [{'name': name, 'path': path, 'create_time': create_time, 'create_manager': create_manager,
                             'statu': '已使用' if statu == 'Y' else '待使用' if statu == 'R' else '未使用',
                             'size': round(sum(global_config.get_model_size(path, model_size_list=[])) / (1024 ** 3),
                                           2)}
                            for name, path, create_time, create_manager, statu in result]
                    return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def model_switch(request):
    if request.method == 'POST':
        connection = mysql_pool.connection()
        request_param = json.loads(request.body.decode('utf-8'))
        path = request_param.get('path')
        try:
            with connection.cursor() as cursor:
                # 首先找出是否存在其它的待使用模型
                cursor.execute("select path from model where statu='R';")
                result = cursor.fetchall()
                # 如果有，将其转为N
                if result:
                    cursor.execute("update model set statu = 'N' where path = '{}';".format(result[0][0]))
                # 如果没有，将传入的模型路径设为R，同时Redis设置标志位
                redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                                 password='12345678')
                redis_client.set('switch_model', 'R')
                result = cursor.execute("update model set statu = 'R' where path = '{}';".format(path))
                connection.commit()
                if result > 0:
                    now = datetime.now()
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|model_switch|{path}|{add_time}")
                    data = {'auth': 'Y'}
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def ner_predict(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        text = params.get('text')
        text = text.replace(" ", "")
        result = subprocess.run(
            f'/public/home/medical_2324/.conda/envs/NER/bin/python3 /public/home/medical_2324/Medical_LLM/torch_ner/source/ner_predict.py {text}',
            shell=True, text=True, check=True, capture_output=True)
        result = result.stdout
        data = result
        return HttpResponse(json.dumps(data), status=200)


@csrf_exempt
def model_add(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        name = params.get('name')
        path = params.get('path')
        create_manager = params.get('create_manager')
        now = datetime.now()
        add_time = now.strftime("%Y年%m月%d日%H:%M")
        connection = mysql_pool.connection()
        try:
            with connection.cursor() as cursor:
                result = cursor.execute("insert into model values('{}','{}','{}',{},'N');".format(name, path, add_time,
                                                                                                  int(create_manager)))
                connection.commit()
                if result > 0:
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|model_add|{path}|{add_time}")
                    data = {'auth': 'Y'}
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def model_delete(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        path = params.get('path')
        connection = mysql_pool.connection()
        now = datetime.now()
        try:
            with connection.cursor() as cursor:
                result = cursor.execute("delete from model where path='{}';".format(path))
                connection.commit()
                if result > 0:
                    add_time = now.strftime("%Y.%m.%d %H:%M")
                    global_config.send_log(f"system|model_delete|{path}|{add_time}")
                    shutil.rmtree(path)
                    data = {'auth': 'Y'}
                else:
                    data = {'auth': 'W'}
                return HttpResponse(json.dumps(data), status=200)
        finally:
            connection.close()


@csrf_exempt
def model_params(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        action = params.get('action')
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        if action == 'U':
            top_p = params.get('top_p')
            top_k = params.get('top_k')
            temperature = params.get('temperature')
            try:
                redis_client.set('top_p', top_p)
                redis_client.set('top_k', top_k)
                redis_client.set('temperature', temperature)
                data = {'auth': 'Y'}
            except Exception as e:
                data = {'auth': 'W'}
            return HttpResponse(json.dumps(data), status=200)
        elif action == 'C':
            top_p = redis_client.get('top_p')
            top_k = redis_client.get('top_k')
            temperature = redis_client.get('temperature')
            data = {'top_p': top_p, 'top_k': top_k, 'temperature': temperature}
            return HttpResponse(json.dumps(data), status=200)
