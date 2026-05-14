<template>
  <div>
    <el-row style='position: absolute;bottom: 0;right: 0;top: 0;left: 0;'>
      <!--左侧X光图片显示区域-->
      <el-col :span='7' style='height: calc(100vh - 75px);border-right: 2px solid #ccc;'>
        <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex; align-items: center;justify-content: center;height: 80px;font-weight: bold;font-size: 25px;font-family: 微软雅黑,serif'>
          自动诊断
        </el-col>
        <el-col :span='24' style='border: 1px red solid;height: calc(70vh - 75px - 80px);display: flex;justify-content: center;align-items: center'>
          <img v-if="imageURL" :src="imageURL" alt='预览图片' style='width: 400px;height: auto'>
        </el-col>
        <!--诊断报告自动显示区域-->
        <el-col :span='24' v-html='html2' style='border: 1px black solid;height: 30vh;overflow: auto'></el-col>
      </el-col>
      <!--中间电子病历区域-->
      <el-col :span='10' style='height: calc(100vh - 75px);border-right: 2px solid #ccc;'>
        <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex; align-items: center;justify-content: center;height: 80px;font-weight: bold;font-size: 25px;font-family: 微软雅黑,serif'>
          电子病历
        </el-col>
        <!--姓名、性别、出生年月、年龄、身份证号、病历号-->
        <el-col :span='24' style='height: 20px'></el-col>
        <el-col :span='6' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>姓名：{{name}}</el-col>
        <el-col :span='4' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>性别：{{gender}}</el-col>
        <el-col :span='14' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>病历编号：{{token}}</el-col>
        <el-col :span='24' style='height: 20px'></el-col>
        <el-col :span='4' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>年龄：{{age}}岁</el-col>
        <el-col :span='11' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>身份证号：{{self_id}}</el-col>
        <el-col :span='9' style='height: 23px;font-size: 18px;display: flex; align-items: center;justify-content: center;'>出生年月：{{year}}年{{month}}月{{day}}日</el-col>
        <el-col :span='24' style='height: 15px;border-bottom: 1px black solid'></el-col>
        <!--患者主诉自动显示区域-->
        <el-col :span='24' style='border-bottom: 1px black solid;height: 550px'>
          <el-col :span='24' style='height: 50px;font-size: 20px;font-weight: bold;display: flex;justify-content: left;align-items: center;'>&nbsp;&nbsp;&nbsp;患者主诉</el-col>
          <el-col :span='1' style='height: 100px;border-bottom: 2px dashed #ccc'></el-col>
          <el-col :span='22' v-html='html' style='height: 100px;border-bottom: 2px dashed #ccc'></el-col>
          <el-col :span='1' style='height: 100px;border-bottom: 2px dashed #ccc'></el-col>
          <el-col :span='24' style='height: 50px;font-size: 20px;font-weight: bold;display: flex;justify-content: left;align-items: center;'>&nbsp;&nbsp;&nbsp;诊断报告</el-col>
          <!--诊断报告-->
          <el-col :span='1' v-show='!showEdit' style='height: 350px;'></el-col>
          <el-col :span='22' v-show='!showEdit' style='height: 350px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{output}}</el-col>
          <el-col :span='1' v-show='!showEdit' style='height: 350px;'></el-col>
          <!--隐藏的修改区域-->
          <el-col :span='24' v-show='showEdit' style='height: 350px'>
            <el-form>
              <el-form-item>
                <el-input type='textarea' :rows='10' v-model="output" placeholder="请输入患者主诉" style='resize: none;'></el-input>
              </el-form-item>
            </el-form>
          </el-col>
        
        </el-col>
        <el-col :span='24' style='height: calc(100vh - 75px - 80px - 55px - 46px - 550px);display: flex; align-items: center;justify-content: center;'>
          <el-button v-show='!showEdit' @click='editRecord' type='primary'>编辑病历</el-button>
          <el-button v-show='!showEdit' @click='generateRecord' type='success'>提交病历</el-button>
          <el-button v-show='showEdit' @click='updateRecord' type='success'>确认修改</el-button>
        </el-col>
      </el-col>
      <!--右侧AI对话区域-->
      <el-col :span='7' style='height: calc(100vh - 75px);border-right: 2px solid #ccc;'>
        <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex; align-items: center;justify-content: center;height: 80px;font-weight: bold;font-size: 25px;font-family: 微软雅黑,serif'>
          模型询诊
        </el-col>
        <!--对话区域-->
        <el-col :span='24' ref="contentContainer" v-html='outputHTML' style='height: calc(100vh - 75px - 80px - 105px);border-bottom: 1px solid black;overflow: auto;'>
          <el-col :span='24' style='height: 15px;border: 1px red solid'></el-col>
        </el-col>
        <el-col :span='24' style='height: calc(100vh - 75px - 80px - 55px - 46px - 550px);display: flex; align-items: center;justify-content: center;'>
          <el-input v-model='answer' placeholder='输入询问内容' style='width: 350px;'></el-input>
          <el-button @click='AnswerQuestion' style='width: 80px;height: 40px;padding: 0;'>发送</el-button>
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
      token:'',
      name:'',
      imageURL:'',
      output:'',
      output2:'',
      outputHTML:'',
      answer:'',
      self_id:'',
      year:'',
      month:'',
      day:'',
      age:'',
      gender:'',
      showEdit:false,
      complaint:'',
      html:'',
      html2:'',
    }
  },
  created() {
//     this.token = window.sessionStorage.getItem('token');
//     this.name = window.sessionStorage.getItem('patient');
//     this.imageURL = window.sessionStorage.getItem('imageURL');
//     this.self_id = window.sessionStorage.getItem('self_id');
//     this.complaint = window.sessionStorage.getItem('complaint');
//     this.outputHTML += `<el-col :span='24' style='height: 15px;display: flex;align-items: center;justify-content: right;'>
// </el-col>`;
//     this.resolveID();
//     setTimeout(() => {
//       this.submitRecord();
//       this.autoTalkWithAI();
//     }, 500);
  },
  watch: {
    outputHTML(newContent) {
      // 监听outputHTML变化，触发滚动到底部的方法
      this.$nextTick(() => {
        this.scrollContentToBottom();
      });
    },
  },
  mounted() {
    // 初始化时滚动到底部
    this.scrollContentToBottom();
  },
  methods:{
    async autoTalkWithAI(){
      const data = {auto_generate: 'Y', token: this.token, query: this.gender+'，'+this.age+"岁。"};
      const response = await axios.post('http://10.1.103.48:8426/model/patient_talk/',data);
      const answer = response.data.output;
      let i;
      for(i=0;i<answer.length;i++)
      {
        this.output2+=answer[i];
      }
      const data2 = {text: this.output2};
      const res = await axios.post('http://10.1.103.48:8426/model/ner_predict/',data2);
      let html = "";
      let lastIndex = 0;
      const d = JSON.parse(res.data);
      for (let i = 0; i < d.length; i++) {
        const entity = d[i];
        const start = entity.begin;
        const end = entity.end;
        const type = entity.type;
        const value = entity.value;
        html += this.complaint.slice(lastIndex, start);
        html += `<span class="highlight ${type}"><span class="value">${value}</span></span>`;
        lastIndex = end;
      }
      html += this.complaint.slice(lastIndex);
      this.html2 = html;
    },
    async resolveID(){
      this.year=this.self_id.substr(6,4);
      this.month=this.self_id.substr(10,2);
      this.day=this.self_id.substr(12,2);
      this.age=new Date().getFullYear()-parseInt(this.year,10);
      const genderCode = parseInt(this.self_id.substr(16,1),10);
      this.gender=genderCode%2===0?'女':'男';
    },
    async submitRecord(){
      const data = {text: this.complaint};
      const res = await axios.post('http://10.1.103.48:8426/model/ner_predict/',data);
      let html = "";
      let lastIndex = 0;
      const d = JSON.parse(res.data);
      for (let i = 0; i < d.length; i++) {
        const entity = d[i];
        const start = entity.begin;
        const end = entity.end;
        const type = entity.type;
        const value = entity.value;
        html += this.complaint.slice(lastIndex, start);
        html += `<span class="highlight ${type}"><span class="value">${value}</span></span>`;
        lastIndex = end;
      }
      html += this.complaint.slice(lastIndex);
      this.html = html;
    },
    editRecord(){
      this.showEdit = true;
    },
    generateRecord(){
      const data = {token: this.token, id: window.sessionStorage.getItem('id'), record: {complaint: this.complaint, illness: this.output}};
      axios.post('http://10.1.103.48:8426/hadoop/patient_generate/',data).then(res=>{
        if(res.data.auth==='Y')
        {
          this.$message.success("病历上传成功");
          try {
            this.$router.push('/doctor_home');
          } catch (e) {
            console.log(e);
            console.log("无法跳转");
          }
        }
        else {
          this.$message.error("服务器内部错误，请稍后再试");
        }
      });
    },
    updateRecord(){
      this.showEdit = false;
    },
    scrollContentToBottom() {
      const container = this.$refs.contentContainer;
      this.$nextTick(() => {
        container.scrollTop = container.scrollHeight;
      });
    },
    AnswerQuestion(){
      if(!this.answer)
      {
        this.$message.error("询问内容不能为空");
        return;
      }
      this.outputHTML+=`<el-col :span='24' style='display: flex;align-items: center;justify-content: right;'>
            <span style='margin-right: 10px;height: 100%;background-color: burlywood;border-radius: 10px;'>&nbsp;&nbsp;${this.answer}&nbsp;&nbsp;</span>
          </el-col>`;
      this.outputHTML+=`<el-col :span='24' style='height: 15px;display: flex;align-items: center;justify-content: right;'></el-col>`;
      const data = {auto_generate: 'N', token: this.token, query: this.answer};
      axios.post('http://10.1.103.48:8426/model/patient_talk/',data).then(res=>{
        const chat = res.data.output;
        this.outputHTML+=`<el-col :span='24' style='display: flex;align-items: center;justify-content: left;'>
            <span style='margin-left: 10px;height: 100%;background-color: aquamarine;border-radius: 10px;'>&nbsp;&nbsp;${chat}&nbsp;&nbsp;</span>
          </el-col>`;
        this.outputHTML+=`<el-col :span='24' style='height: 15px;display: flex;align-items: center;justify-content: right;'></el-col>`;
      });
      this.answer='';
    },
  },
}

</script>

<style>
.highlight {
  position: relative;
  padding: 0 5px;
  border-radius: 4px;
}

.value {
  font-weight: bold;
  font-size: 18px;
  white-space: nowrap;
}

.type {
  position: absolute;
  top: 10px;
  /* 调整与 value 的距离 */
  left: 50%;
  /* 使类型值居中 */
  transform: translateX(-50%);
  /* 使类型值居中 */
  font-size: 12px;
  white-space: nowrap;
  /* 添加此行以避免换行 */
}
.药物 {
  background-color: rgba(173,139,115, 0.4);
  color: #AD8B73;
}

.辅助检查 {
  background-color: rgba(149,225,211, 0.4);
  color: #95E1D3;
}

.治疗方案 {
  background-color: rgba(183,153,255, 0.4);
  color: #B799FF;
}

.症状 {
  background-color: rgba(243,129,129, 0.4);
  color: #F38181;
}

.生理器官 {
  background-color: rgba(104,185,132, 0.4);
  color: #68B984;
}

.疾病与诊断 {
  background-color: rgba(17,109,110, 0.4);
  color: #116D6E;
}

.实验室检查 {
  background-color: rgba(236,229,199, 0.4);
  color: #ECE5C7;
}

.科室 {
  background-color: rgba(255,205,168, 0.4);
  color: #FFCDA8;
}

.指标值 {
  background-color: rgba(190,109,183, 0.4);
  color: #BE6DB7;
}

.人群 {
  background-color: rgba(17,106,123, 0.4);
  color: #116A7B;
}

.等级程度 {
  background-color: rgba(96,108,93, 0.4);
  color: #606C5D;
}

.时间 {
  background-color: rgba(229,88,7, 0.4);
  color: #E55807;
}



</style>