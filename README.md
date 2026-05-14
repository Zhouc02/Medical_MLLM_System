# 简易医学多模态大语言模型辅助诊断系统

> [!IMPORTANT]
> 该项目由于年代久远，缺失部分内容，故无法直接完整运行！
> 若需完整运行，需自行更改部分代码并进行调试！
> 但是用于应付课程或许有用？

## 简要介绍
本项目实现简易的前后端医学辅助诊断系统，包含多种功能，核心功能为：上传医学影像，模型自主诊断，对诊断结果文本进行实体识别。其它功能详情可见[Medical_LLM->README.md](./Medical_LLM/README.md)。

本项目着手开发时距离ChatGPT3发布仅过去一年，当时根本没有什么Agent的概念，在这方面那时也没什么可参考的前后端项目。本项目主要包含Django后端与Vue前端，分别在[Medical_LLM](./Medical_LLM)文件夹及[medical_vue](./medical_vue)文件夹中。

本项目所采用的大模型为[XrayGLM](https://github.com/WangRongsheng/XrayGLM)，但可以更换为其它更先进的医疗/其它领域的多模态大模型；命名实体识别部分为当初实验室自行开发设计，故在此不给出，可自行寻找适合的中文医学命名实体识别模型。

## 主要框架
Django、Vue、MySQL、Redis、Flume、Hadoop、Hive（后三者非必要，只影响少部分功能）。

## 环境配置
> [!NOTE]
> 以下环境配置为三年后试图将其复活而自行尝试的过程，不一定能完美运行！

### Python
```bash
conda create -n medical
conda install python=3.9
micromamba install pytorch==1.12.0 torchvision cudatoolkit==11.6 -c pytorch -c conda-forge
micromamba install mkl==2024.0
micromamba install pyarrow
pip install SwissArmyTransformer==0.3.7
pip install bitsandbytes==0.39.0
pip install django djangorestframework django-cors-headers pymysql DBUtils redis psutil GPUtil
pip install transformers==4.33.0
micromamba install libaio
micromamba install libnuma
pip install numpy==1.20
pip install pandas==1.2
pip install Pillow
micromamba install torchvision -c pytorch -c conda-forge
pip install deepspeed==0.9.0
pip install datasets==2.10.1
pip uninstall -y numpy pandas pyarrow datasets
micromamba install -c conda-forge pyarrow=11.0.0
pip install numpy==1.24.3 pandas==1.5.3 datasets==2.10.1
micromamba install scipy channels
micromamba install daphne
micromamba uninstall pyarrow
micromamba install -c conda-forge pyarrow=11.0.0
pip install numpy==1.24.3 pandas==1.5.3 datasets==2.10.1
```
我印象中deepspeed库需要自行编译为CUDA版本，当然如果你使用其它的模型可能不需要。

### MySQL
这里给出一个快速部署过程，免安装，不用可以直接删除，注意路径自行修改。
```bash
wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.44-linux-glibc2.12-x86_64.tar.gz
tar -zxvf mysql-5.7.44-linux-glibc2.12-x86_64.tar.gz
mv mysql-5.7.44-linux-glibc2.12-x86_64 mysql
cd mysql
mkdir data logs
vim my.cnf
export LD_LIBRARY_PATH=/root/anaconda3/envs/medical/lib:$LD_LIBRARY_PATH
./bin/mysqld --initialize --user=root --basedir=/opt/mysql --datadir=/opt/mysql/data
./bin/mysqld_safe --user=root &
./bin/mysql -uroot -p -S /opt/mysql/mysql.sock
```
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '12345678' WITH GRANT OPTION;
FLUSH PRIVILEGES;
create database medical;
use medical;
source /opt/mysql/medical.sql;
quit;
```
### Redis
同样免安装快速部署，但需要自行编译。
```bash
wget https://download.redis.io/releases/redis-6.2.14.tar.gz
tar -zxvf redis-6.2.14.tar.gz
mv redis-6.2.14 redis
cd redis
make
vim redis.conf
./src/redis-server ./redis.conf
```
### 前端
前端采用Vue2设计，由于脱离Vue开发已久，这里不再详细讲述如何安装node.js，需要的脚手架应该都在[medical_vue](./medical_vue)下的`package.json`和`package-lock.json`中。
## 模型下载
### MLLM

需要的XrayGLM模型可以从官方提供的huggingface中下载，下载到`Medical_LLM/VisualGLM/model/checkpoint/XrayGLM-3000/3000`中：
```bash
wget https://huggingface.co/wangrongsheng/XrayGLM-3000/resolve/main/3000/mp_rank_00_model_states.pt
```
镜像下载链接：
```bash
wget https://hf-mirror.com/wangrongsheng/XrayGLM-3000/resolve/main/3000/mp_rank_00_model_states.pt
```
其次，由于采用了[ChatGLM-6B](https://github.com/zai-org/ChatGLM-6B)的分词，需要下载一些东西到`Medical_LLM/VisualGLM/THUDM/chatglm-6b`中，至于是什么我没有时间翻找，应该在`https://huggingface.co/zai-org/chatglm-6b/tree/main`中。

如果你想使用更先进的模型，请根据实际情况修改`Medical_LLM/Medical_LLM/apps.py`的`ready()`函数，该函数的作用是当Django启动时同时后台挂载模型。然后根据模型的对话API，修改`Medical_LLM/MLLM/views.py`的`talk()`函数。
### NER
还请自行寻找合适的中文医学命名实体识别模型，然后根据实际情况修改`Medical_LLM/MLLM/views.py`的`ner_predict()`函数。
> [!WARNING]
> 代码里存在大量的硬编码路径和IP，需要根据你的实际情况修改！

如果你能搞定上面这些步骤，那么就可以使用`python manage.py runserver`启动Django了。
## 使用须知
> [!CAUTION]
> 任何辅助诊断类模型都有可能输出与事实不符的内容！

本项目的license遵从XrayGLM。
## 致谢
感谢[ChatGLM-6B](https://github.com/zai-org/ChatGLM-6B)、[VisualGLM-6B](https://github.com/zai-org/VisualGLM-6B)和[XrayGLM](https://github.com/WangRongsheng/XrayGLM)在当年的开创性工作。
