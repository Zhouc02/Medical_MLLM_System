import argparse
import logging
from datetime import datetime

import django
import redis
from django.apps import AppConfig
from sat.model import AutoModel
from sat.model.mixins import CachedAutoregressiveMixin
from transformers import AutoTokenizer

import global_config
from Medical_LLM.settings import mysql_pool
from VisualGLM.finetune_visualglm import FineTuneVisualGLMModel


class SelfAppConfig(AppConfig):
    name = 'Medical_LLM'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        connection = mysql_pool.connection()
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True,
                                         password='12345678')
        model_status = redis_client.get('switch_model')
        with connection.cursor() as cursor:
            # 如果有标志位，找出R对应的路径
            if model_status == 'R':
                print("========================++++++++++++++正在执行模型切换++++++++++++++========================")
                cursor.execute("select path from model where statu ='R';")
                result = cursor.fetchall()
                path = result[0][0]
                redis_client.delete('switch_model')
                # 将之前有Y标志位的model设置为N
                cursor.execute("select path from model where statu = 'Y';")
                result = cursor.fetchall()
                Y_path = result[0][0]
                cursor.execute("update model set statu = 'N' where path = '{}';".format(Y_path))
                connection.commit()
                # 将现在要切换的model的标志位设置为Y
                cursor.execute("update model set statu = 'Y' where path = '{}';".format(path))
                connection.commit()
            else:
                # 如果没有标志位
                cursor.execute("select path from model where statu='Y'")
                result = cursor.fetchall()
                if result:
                    path = result[0][0]
        print("========================++++++++++++++正在初始化医学多模态大语言模型++++++++++++++========================")
        self.model, self.model_args = AutoModel.from_pretrained(
            path,
            args=argparse.Namespace(
                fp16=True,
                skip_init=True,
                use_gpu_initialization=True,
                device='cuda'
            )
        )
        self.model = self.model.eval()
        self.model.add_mixin('auto-regressive', CachedAutoregressiveMixin())
        self.tokenizer = AutoTokenizer.from_pretrained("./VisualGLM/THUDM/chatglm-6b",
                                                       trust_remote_code=True)
        now = datetime.now()
        add_time = now.strftime("%Y.%m.%d %H:%M")
        global_config.send_log(f"system|boot|{path}|{add_time}")
        print(
            "========================++++++++++++++医学多模态大语言模型初始化完毕++++++++++++++========================")
        print("========================++++++++++++++Django，启动！++++++++++++++========================")
