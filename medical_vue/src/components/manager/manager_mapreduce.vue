<template>
  <div>
    <!--提示区域-->
    <el-col :span='24' style='padding-left: 20px;display: flex;align-items:center;font-size: 17px;height: 60px;position: absolute;top: 0;left: 0;right: 0'>
      <strong>当前使用日志：</strong>{{log_name}}
    </el-col>
    
    <!--MapReduce代码区域-->
    <el-col :span=12 style='height: 300px;position: absolute;left: 0;right: 0;top: 60px;border-right: 1px solid #ccc'>
      <codemirror v-model="map" :options="editorOptions" style='height: 100%;width: 100%'></codemirror>
    </el-col>
    <el-col :span=12 style='height: 300px;position: absolute;right: 0;top: 60px'>
      <codemirror v-model="reduce" :options="editorOptions" style='height: 100%;width: 100%'></codemirror>
    </el-col>
    
    <!--结果显示区域-->
    <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex;justify-content: left;height: 400px;padding-top: 10px;padding-left: 20px;position: absolute;left: 0;right: 0;top: 360px;overflow: auto'>
      {{status}}
      <pre>{{content}}</pre>
    </el-col>
    
    <!--按钮区域-->
    <el-col :span='24' style='position: absolute;left: 0;right: 0;top: 760px;height: calc(100vh - 760px - 75px);display: flex;align-items: center'>
      <el-button type='warning' @click="clearSQL" style='font-size: 15px;margin-left: auto;margin-right: 20px'>清空</el-button>
      <el-button type="primary" @click="submitSQL" style='font-size: 15px;margin-right: 20px'>提交</el-button>
      <el-button type="danger" @click="exitSQL" style='font-size: 15px;margin-right: 20px'>退出</el-button>
    </el-col>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror-lite';
import 'codemirror/theme/paraiso-light.css'
import 'codemirror/mode/python/python';
import axios from 'axios'

export default {
  components: {
    codemirror,
  },
  data(){
    return{
      log_name:'',
      map:'',
      reduce:'',
      content:'',
      table_name:'',
      status:'尚未提交任务',
      editorOptions: {
        mode: 'python', // 设置编辑器模式为 SQL
        theme: 'paraiso-light', // 设置编辑器主题
        lineNumbers: true,
      },
    }
  },
  created() {
    this.log_name=window.sessionStorage.getItem('log_name');
    this.initializeEnv();
  },
  methods:{
    async initializeEnv(){
      if(!this.log_name)
      {
        this.$message.error("发生错误");
        return;
      }
      const data = {action: 'C', log_name: this.log_name};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/mapreduce_analysis/', data);
      if (res.data.auth == 'Y')
        this.$message.success("初始化环境成功");
      else this.$message.error("初始化环境失败");
    },
    submitSQL(){
      if(!this.map || !this.reduce)
      {
        this.$message.error("请编写map和reduce程序");
        return;
      }
      this.status='已提交，正在执行';
      this.content = '';
      const data ={action:'S', map:this.map, reduce:this.reduce};
      axios.post('http://10.1.103.48:8426/hadoop/mapreduce_analysis/',data).then(res=>{
        const job_id = res.data.job_id;
        this.RollCheck(job_id);
      });
    },
    RollCheck(job_id){
      const data = {action: 'R', job_id: job_id};
      axios.post('http://10.1.103.48:8426/hadoop/hive_analysis/',data).then(res=>{
        if(res.data.result == 'N')
        {
          setTimeout(()=>{
            this.RollCheck(job_id);
          },2000);
        }
        else {
          this.status='';
          this.content = res.data.content;
        }
      });
    },
    clearSQL(){
      this.map='';
      this.reduce='';
    },
    exitSQL(){
      const data ={action: 'X'};
      axios.post('http://10.1.103.48:8426/hadoop/mapreduce_analysis/', data).then(res=>{
        if (res.data.auth == 'Y')
        {
          this.$message.success("已清除临时环境");
          this.$router.push('/manager_analysis');
        }
        else this.$message.error("无法清除临时环境");
      });
    },
  },
}
</script>