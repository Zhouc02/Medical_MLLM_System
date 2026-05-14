<template>
  <div>
    <!--顶部刷新、新增、搜索栏-->
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <!--刷新按钮-->
      <el-button @click='updateData' style='background-color: bisque;width: 85px;height: 55px;padding: 0;margin-left: 20px'>刷新列表</el-button>
      <!--顶部搜索栏，身份证搜索-->
      <el-input v-model='searchKey' placeholder='输入身份证号搜索' style='width: 300px;margin-left: auto;margin-right: 10px'></el-input>
      <!--搜索按钮-->
      <el-button @click='searchForKey' style='width: 85px;height: 55px;padding: 0;margin-left: 10px;margin-right: 20px'>开始搜索</el-button>
    </el-col>
    <!--表格区域-->
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='jsonData' style='width: 100%'>
        <el-table-column prop='token' label='病历编号'></el-table-column>
        <el-table-column prop='name' label='姓名'></el-table-column>
        <el-table-column prop='self_id' label='身份证号'></el-table-column>
        <el-table-column prop='text_path' label='病历报告'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data(){
    return{
      jsonData:[],
      searchKey:'',
    }
  },
  created() {
    this.fetchData();
  },
  methods:{
    async fetchData(){
      const data = {action: 'C'};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/patient_check/',data);
      this.jsonData = res.data;
      this.$message.success("数据刷新成功");
    },
    updateData(){
      this.fetchData();
    },
    handleDelete(row){
      this.$confirm('确定删除该条病历吗？','删除警告',{
        confirmButtonText: '确定',
        cancelButtonText:'取消',
        type: 'warning'
      }).then(()=>{
        // 待模型调试完成后将下列代码取消注释
        // if(row.text_path == '未生成'){
        //   this.$message({
        //     type:'error',
        //     message: '无法删除尚未生成报告的病历'
        //   });
        //   return;
        // }
        const data = {action: 'D', token: row.token}
        axios.post('http://10.1.103.48:8426/hadoop/patient_check/',data).then(res=>{
          if(res.data.auth === 'Y')
          {
            this.$message.success("删除成功");
            this.fetchData();
          }
          else {
            this.$message.error("删除失败");
          }
        });
      }).catch(()=>{
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    searchForKey(){
      if (!this.searchKey||this.searchKey.length<18)
      {
        this.$message.error("请重新输入搜索条件");
        return;
      }
      const data = {self_id: this.searchKey};
      axios.post('http://10.1.103.48:8426/hadoop/patient_search/', data).then(res=>{
        if(res.data[0].token === 'W')
        {
          this.$message.error("没有该病人的记录");
        }
        else {
          this.jsonData=res.data;
        }
      });
    },
  },
}
</script>