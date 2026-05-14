<template>
  <div>
    <!--顶部-->
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <el-button @click='updateLog' style='background-color: bisque;width: 85px;height: 55px;padding: 0;margin-left: 20px'>刷新日志</el-button>
      <el-button @click='analysisHistory' type='success' style='width: 85px;height: 55px;padding: 0;margin-left: 40px'>分析历史</el-button>
      <el-button @click='HDFSPage' type='info' style='width: 85px;height: 55px;padding: 0;margin-left: 40px'>HDFS页面</el-button>
    </el-col>
    <!--表格区域-->
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='logJson' style='width: 100%'>
        <el-table-column prop='log_name' label='日志名'></el-table-column>
        <el-table-column prop='log_size' label='日志大小(KB)'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="info" @click="log_check(scope.row)">查看</el-button>
            <el-button type="success" @click="hive_analysis(scope.row)">Hive分析</el-button>
            <el-button type='warning' @click='mr_analysis(scope.row)'>MR分析</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
    
    <el-dialog title="日志查看" :visible.sync="showContent" width="60%">
      <div style="display: flex; flex-direction: column; height: 100%;">
        <el-col :span="24" style="overflow: auto;height: 610px;">
          <pre>{{content}}</pre>
        </el-col>
      </div>
    </el-dialog>
    
  </div>
</template>

<script>
import axios from 'axios'

export default{
  data(){
    return{
      logJson:[],
      content:'',
      showContent:false,
    }
  },
  created() {
    this.fetchLog();
  },
  methods:{
    async fetchLog(){
      const data = {action: 'C'};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/log_list/', data);
      this.logJson = res.data;
    },
    hive_analysis(row){
      window.sessionStorage.setItem('log_name', row.log_name);
      this.$router.push('/manager_hive');
    },
    mr_analysis(row){
      window.sessionStorage.setItem('log_name', row.log_name);
      this.$router.push('/manager_mapreduce');
    },
    analysisHistory(){
      this.$router.push('/manager_logistory')
    },
    HDFSPage(){
      window.open('http://10.1.103.48:50070', '_blank');
    },
    updateLog(){
      this.fetchLog();
      this.$message.success("刷新成功");
    },
    log_check(row){
      const data = {action: 'S', log_name: row.log_name};
      axios.post('http://10.1.103.48:8426/hadoop/log_list/',data).then(res=>{
        this.content = decodeURIComponent(res.data.content);
        this.showContent = true;
      });
    },
  },
}
</script>