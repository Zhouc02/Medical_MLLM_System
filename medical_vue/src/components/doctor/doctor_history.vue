<template>
  <div>
    <!--顶部刷新、新增、搜索栏-->
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <!--顶部搜索栏，身份证搜索-->
      <el-input v-model='searchKey' placeholder='输入身份证号搜索' style='width: 300px;margin-left: 10px'></el-input>
      <!--搜索按钮-->
      <el-button @click='searchForKey' style='width: 85px;height: 40px;padding: 0;margin-left: 10px;'>搜索病史</el-button>
    </el-col>
    <!--表格区域-->
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='jsonData' style='width: 100%'>
        <el-table-column prop='token' label='病历编号'></el-table-column>
        <el-table-column prop='text_path' label='病历报告'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="info" @click="handleCheck(scope.row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
    <el-dialog
      title="病历查看"
      :visible.sync="isModalVisible"
      width="60%"
    >
      <el-col :span='12' style='height: 550px;display: flex;align-items: center;justify-content: center'>
        <img v-if="fileContent1 !== null" :src="fileContent1" alt="Image" style='height: 500px;width: auto' />
      </el-col>
      <el-col :span='12' style='height: 550px;'>
        <el-col :span='24' style='height: 50px;font-size: 20px;font-weight: bold;display: flex;justify-content: left;align-items: center;'>&nbsp;&nbsp;&nbsp;患者主诉</el-col>
        <el-col :span='1' style='height: 100px;'></el-col>
        <el-col :span='22' style='height: 100px;font-size: 17px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{complaint}}</el-col>
        <el-col :span='1' style='height: 100px;'></el-col>
        <el-col :span='24' style='height: 50px;font-size: 20px;font-weight: bold;display: flex;justify-content: left;align-items: center;'>&nbsp;&nbsp;&nbsp;诊断报告</el-col>
        <el-col :span='1' style='height: 350px;'></el-col>
        <el-col :span='22' style='height: 350px;font-size: 17px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{illness}}</el-col>
        <el-col :span='1' style='height: 350px;'></el-col>
      </el-col>
      <el-button @click='closeModal'>取消</el-button>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import JSZip from 'jszip'

export default{
  data(){
    return{
      searchKey:'',
      jsonData:[],
      fileContent1:null,
      fileContent2:null,
      isModalVisible: false,
      complaint:'',
      illness:'',
    }
  },
  methods:{
    searchForKey(){
      if(this.searchKey.length<18)
      {
        this.$message.error("请输入正确的身份证号码");
        return;
      }
      const data = {self_id: this.searchKey};
      axios.post('http://10.1.103.48:8426/hadoop/history_list/',data).then(res=>{
        if(res.data[0].token === 'W')
        {
          this.$message.warning("该患者尚未有任何病历报告");
        }
        else {
          this.jsonData=res.data;
        }
      });
    },
    handleCheck(row){
      if(row.text_path == '未生成')
      {
        this.$message.warning("该病历未生成，无法查看");
      }
      else{
        this.isModalVisible = true;
        const data = {token: row.token};
        axios.post('http://10.1.103.48:8426/hadoop/special_record/', data, { responseType: 'blob' })
          .then(response => {
            const zip = new JSZip();
            // 解压缩 ZIP 文件
            return zip.loadAsync(response.data);
          })
          .then(zip => {
            // 从 ZIP 文件中获取图像和文本文件的内容
            return Promise.all([
              zip.file(`${row.token}.png`).async('base64'),
              zip.file(`${row.token}.txt`).async('text'),
            ]);
          })
          .then(([imageContent, textContent]) => {
            // 更新数据以在页面上显示文件内容
            this.fileContent1 = `data:image/png;base64,${imageContent}`;
            const parsedJson = JSON.parse(textContent);
            this.complaint = parsedJson.complaint;
            this.illness = parsedJson.illness;
            this.fileContent2 = this.complaint+this.illness;
          })
          .catch(error => {
            console.error('获取文件失败：', error);
          });
      }
    },
    closeModal(){
      this.isModalVisible = false;
    },
  },
}

</script>
