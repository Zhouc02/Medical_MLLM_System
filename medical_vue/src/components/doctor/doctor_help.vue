<template>
  <div>
    <el-row  style='position: absolute;bottom: 0;right: 0;top: 0;left: 0;'>
      <el-col :span='24' style='height: calc(100vh - 75px)'>
        <!--顶部显示-->
        <el-col :span='24' style='height: calc((100vh - 75px)*0.7/9);display: flex;align-items: center;justify-content: center;;border-bottom: 1px solid #ccc'>
          <p style='font-size: 19px;font-weight: bold;font-family: 微软雅黑,serif'>医师互助区</p>
        </el-col>
        <!--对话内容显示-->
        <el-col :span='24' v-html='generateHTML' style='height: calc((100vh - 75px)*7.3/9);overflow: auto'>
        </el-col>
        <!--聊天输入框-->
        <el-col :span='24' style='height: calc((100vh - 75px)/9);display: flex;align-items: center;justify-content: center;border-top: 1px solid #ccc'>
          <el-input v-model='answer' placeholder='输入反馈内容' style='width: 800px;'></el-input>
          <el-button @click='AnswerQuestion' style='width: 85px;height: 40px;padding: 0;margin-left: 10px;margin-right: 20px'>发送</el-button>
        </el-col>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'

export default{
  data(){
    return{
      answer:'',
      generateHTML:'',
      ws:'',
    }
  },
  created() {
    this.fetchData();
  },
  methods:{
    async fetchData(){
      const data = {action: 'C'};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/doctor_help/',data);
      let i;
      this.generateHTML='';
      for(i=0;i<res.data.length;i++) {
        const name = res.data[i].name;
        const content = res.data[i].content;
        const add_time = res.data[i].add_time;
        this.generateHTML+=`<el-col :span='24' style='height: 25px;display: flex;align-items: center;justify-content: center;'>`;
        this.generateHTML+=`<p style='font-size: 14px;font-family:宋体,serif;color: darkgoldenrod'>${add_time}</p>`;
        this.generateHTML+=`</el-col>`;
        if (name == window.sessionStorage.getItem('name'))
        {
          this.generateHTML+=`<el-col :span='24' style='height: 40px;display: flex;align-items: center;justify-content: right;'>
            <span style='margin-right: 10px;height: 100%;background-color:aquamarine;border-radius: 10px;line-height: 40px'>&nbsp;&nbsp;${content}&nbsp;&nbsp;</span>
          </el-col>`;
        }
        else{
          this.generateHTML+=`<el-col :span='24' style='height: 40px;display: flex;align-items: center;justify-content: left;'>
            <span style='margin-left: 10px;font-size: 19px'>${name}</span>
            <span style='margin-left: 10px;height: 100%;background-color: burlywood;border-radius: 10px;line-height: 40px'>&nbsp;&nbsp;${content}&nbsp;&nbsp;</span>
          </el-col>`;
        }
      }
      this.ws = new WebSocket(`ws://10.1.103.48:8426/ws/chat2/doctors/`);
      this.ws.onmessage = (event) => {
        this.fetchData();
      }
    },
    AnswerQuestion(){
      if(!this.answer)
      {
        this.$message.error("请输入对话内容");
        return;
      }
      const data = {action:'I', from_id: window.sessionStorage.getItem('id'), content: this.answer};
      // axios.post('http://10.1.103.48:8426/hadoop/doctor_help/',data).then(res=>{
      //   if(res.data.auth === 'Y')
      //   {
      //     this.fetchData();
      //   }
      //   else {
      //     this.$message.error("发送失败");
      //   }
      // });
      this.ws.send(JSON.stringify(data));
      this.answer = '';
      this.fetchData();
    },
  },
}

</script>