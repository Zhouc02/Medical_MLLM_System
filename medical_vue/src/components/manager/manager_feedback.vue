<template>
  <div>
    <el-row  style='position: absolute;bottom: 0;right: 0;top: 0;left: 0;'>
      <!--左侧反馈列表-->
      <el-col :span='3' style='height: calc((100vh - 75px));border-right: 2px solid #ccc;'>
        <el-col :span='24' style='text-align: center;border-bottom: 2px solid #ccc'>
          <p style='font-size: 20px;font-family: 微软雅黑,serif;font-weight: bold'>医师反馈列表</p>
        </el-col>
        <el-col :span='24' class='clickable-col' style='border-bottom: 1px solid #ccc;text-align: center' v-for='item in feedback_list' :key='item.id' @click.native='selectFeedback(item)'>
          <p>工号：{{item.id}}<br>姓名：{{item.name}}</p>
        </el-col>
      </el-col>
      <!--右侧对话界面-->
      <el-col :span='21' style='height: calc(100vh - 75px)'>
        <!--顶部医生信息显示-->
        <el-col :span='24' style='height: calc((100vh - 75px)*0.7/9);display: flex;align-items: center;justify-content: center;'>
          <p style='font-size: 19px;font-weight: bold;font-family: 微软雅黑,serif'>{{selectedId}} {{selectedName}}</p>
        </el-col>
        <!--对话内容显示-->
        <el-col :span='24' v-html='generateHTML' style='height: calc((100vh - 75px)*7.3/9)'>
        </el-col>
        <!--聊天输入框-->
        <el-col :span='24' style='height: calc((100vh - 75px)/9);display: flex;align-items: center;justify-content: center'>
          <el-input v-show='button_show' v-model='answer' placeholder='输入回复内容' style='width: 800px;'></el-input>
          <el-button v-show='button_show' @click='AnswerQuestion' style='width: 85px;height: 40px;padding: 0;margin-left: 10px;margin-right: 20px'>发送</el-button>
        </el-col>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data(){
    return{
      button_show:false,
      answer:'',
      feedback_list:[],
      feedback_specific:[],
      generateHTML:'',
      selectedId:'',
      selectedName:'',
      ws:'',
    }
  },
  created() {
    this.fetchData();
  },
  methods:{
    async fetchData(){
      const data = {action: 'C'};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/dialogue_check/',data);
      this.feedback_list = res.data;
    },
    AnswerQuestion(){
      if(!this.answer) {
        this.$message.error("输入内容不能为空！");
        return;
      }
      const data = {action:'I', from_id: window.sessionStorage.getItem('id'), to_id: this.selectedId, content: this.answer};
      // axios.post('http://10.1.103.48:8426/hadoop/dialogue_check/',data).then(res=>{
      //   if(res.data.auth === 'Y')
      //   {
      //     this.searchDialogue();
      //   }
      //   else {
      //     this.$message.error("发送失败");
      //   }
      // });
      this.ws.send(JSON.stringify(data));
      this.answer = '';
      this.searchDialogue();
    },
    searchDialogue(){
      const data = {action:'S', id: this.selectedId}
      axios.post('http://10.1.103.48:8426/hadoop/dialogue_check/',data).then(res=>{
        this.feedback_specific=res.data;
        let i;
        this.generateHTML='';
        for(i=0;i<res.data.length;i++){
          const from_id=res.data[i].from_id;
          const to_id=res.data[i].to_id;
          const content=res.data[i].content;
          const add_time=res.data[i].add_time;
          this.generateHTML+=`<el-col :span='24' style='height: 25px;display: flex;align-items: center;justify-content: center;'>`;
          this.generateHTML+=`<p style='font-size: 14px;font-family:宋体,serif;color: darkgoldenrod'>${add_time}</p>`;
          this.generateHTML+=`</el-col>`;
          if(this.selectedId == from_id)
          {
            this.generateHTML+=`<el-col :span='24' style='height: 40px;display: flex;align-items: center;justify-content: left;'>`;
            this.generateHTML+=`<span style='margin-left: 20px;height: 100%;background-color: aquamarine;border-radius: 10px;line-height: 40px'>&nbsp;&nbsp;${content}&nbsp;&nbsp;</span>`;
          }
          else {
            this.generateHTML+=`<el-col :span='24' style='height: 40px;display: flex;align-items: center;justify-content: right;'>`;
            this.generateHTML+=`<span style='margin-right: 10px;height: 100%;background-color: burlywood;border-radius: 10px;line-height: 40px'>&nbsp;&nbsp;${content}&nbsp;&nbsp;</span>`;
            this.generateHTML+=`<span style='margin-right: 20px;font-size: 19px'>${from_id}</span>`;
          }
          this.generateHTML+=`</el-col>`;
        }
      });
      this.ws = new WebSocket(`ws://10.1.103.48:8426/ws/chat/${this.selectedId}/`);
      this.ws.onmessage = (event) => {
        console.log("manager已经接收到消息");
        // this.searchDialogue();
      }
    },
    selectFeedback(item){
      const clickableCol = this.$el.querySelector('.clickable-col');
      if (clickableCol) {
        clickableCol.classList.add('clicked');
        setTimeout(() => {
          clickableCol.classList.remove('clicked');
        }, 300);
      }
      this.button_show=true;
      this.selectedId = item.id;
      this.selectedName = item.name;
      this.searchDialogue();
    },
  },
}
</script>

<style>
.clicked {
  background-color: #f0f0f0; /* 点击时的背景色 */
  transition: background-color 0.3s ease; /* 背景色过渡效果 */
}
.clickable-col{
  cursor: pointer;
}
</style>