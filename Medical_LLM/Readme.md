Django后端说明：

数据库：职工表staff：

    id,name,password,auth

数据库：患者信息patient：

    token,name,self_id,text_path

系统Admin路径：

    system_urls/

说明文档路径：

    docs/

日志格式说明：

    type,executor,content,add_time

Hadoop路径作用：

    hadoop/login/ 登录，传入 name,password 返回 id,name,auth
    hadoop/manager_check 查看所有职工，返回id,name,auth
    hadoop/manager_add 添加员工，传入name,password,auth 返回 auth=Y/W
    hadoop/manager_delete 删除员工，传入id 返回 auth=Y/W
    hadoop/manager_update 修改员工，传入id,name,password,auth 返回auth=Y/W
    hadoop/manager_search 搜索员工，传入id 返回 id,name,auth
    hadoop/patient_pic 上传图片，传入name,self_id,image 返回token
    hadoop/patient_generate 上传最终病历，传入token, record 返回auth=Y/W
    hadoop/history_list 患者历史病历记录，传入self_id 返回 token,text_path
    hadoop/special_record 患者详细历史记录，传入token 返回 image,record (zip)
    hadoop/patient_check 患者管理，传入action=C/D
            如果是C 查看,则返回token,name,self_id,text_path
            如果是D 删除,则同时传入token 返回auth=Y/W
    hadoop/patient_search 查找患者，传入self_id 返回token,name,self_id,text_path
    hadoop/redis_clear Redis清理，返回 count
    hadoop/dialogue_check 查询反馈列表 传入action=C/S/I
            如果是C 查看列表，返回id,name
            如果是S 查看详细对话 传入医生的id 返回from_id,to_id,content,add_time
            如果是I 插入对话 传入from_id,to_id,content, 数据库插入from_id,to_id.content,add_time 返回auth=Y/W
    hadoop/doctor_help 医师互助 传入action=C/I
            如果是C，查看消息，返回name,content,add_time
            如果是I 插入对话 传入from_id,content, 返回auth=Y/W
    hadoop/log_list 查看日志 传入action=C/S
            如果是C，查看日志列表，返回log_name,log_size
            如果是S，查看日志详细内容，传入log_name，返回content
    hadoop/hive_analysis Hive分析 传入action=C/S/G/R/X/L/D
            如果是C，传入log_name，返回table_name
            如果是S，传入sql，返回job_id，紧接着前端不断轮询action=R,传入job_id，每次返回result,content
            如果是X，删除Hive表，返回auth=Y/W，如果是L，返回job_id,add_time,types,result，N查询content和sql, D删除，传入job_id，返回auth
    hadoop/mapreduce_analysis MapReduce分析 传入action=C/S/X/N
            如果是C，传入log_name，创建环境，将log下载本地重命名再上传HDFS，Redis记住重命名的log，本地删除log，返回auth=Y/W
            如果是S，传入map和reduce，返回job_id，然后前端使用hive_analysis action=R轮询，传入job_id,每次返回result,content
            如果是X，删除结果，返回auth=Y/W

MLLM路径作用：

    model/patient_talk 聊天接口，传入auto_generate,token,query 返回output
    model/system_monitor 系统监控 返回allocated,cached,mem,cpu,count
    model/cached_clear 模型缓存清理 返回clear_alloc,clear_cached
    model/model_list 查看模型列表 返回name,path,create_time,create_manager,statu,size
    model/model_switch 切换模型 传入path 返回auth=Y/W
    model/ner_predict 实体提取，传入text 返回result=[{value, type, begin, end}]
    model/model_add 增加模型，传入name,path,create_manager 返回auth=Y/W
    model/model_delete 删除模型，传入path，返回auth=Y/W
    model/model_params 超参数修改，传入action = C/U 传入top_p,top_k,temperature 返回auth=Y/W