<template>
  <div>
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <el-button @click='analyzeHistory' style='background-color: bisque;width: 85px;height: 55px;padding: 0;margin-left: 20px'>刷新历史</el-button>
      <el-button @click='HDFSPage' type='info' style='width: 85px;height: 55px;padding: 0;margin-left: 40px'>HDFS页面</el-button>
    </el-col>
    
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='logJson' style='width: 100%'>
        <el-table-column prop='job_id' label='任务ID'></el-table-column>
        <el-table-column prop='add_time' label='执行时间'></el-table-column>
        <el-table-column prop='type' label='任务类型'></el-table-column>
        <el-table-column prop='result' label='任务结果'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="info" @click="job_check(scope.row)">查看</el-button>
            <el-button type='danger' @click='delete_job(scope.row)'>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
    
    <el-dialog title="Hive任务查看" :visible.sync="hiveShow" width="60%">
      <div style="display: flex; flex-direction: column; height: 100%;">
        <el-col :span="24" style="overflow: auto;height: 50px">
          <pre>{{sql}}</pre>
        </el-col>
      </div>
      <hr/>
      <div style="display: flex; flex-direction: column; height: 100%;">
        <el-col :span="24" style="overflow: auto;height: 500px">
          <pre>{{content}}</pre>
        </el-col>
      </div>
    </el-dialog>
    
    <el-dialog title="MapReduce任务查看" :visible.sync="mrShow" width="60%">
      <div style="display: flex; flex-direction: inherit; height: 100%;">
        <el-col :span="12" style="border-right: 1px solid #ccc; overflow: auto;height: 350px">
          <pre>{{map}}</pre>
        </el-col>
        <el-col :span="12" style="overflow: auto;height: 350px;padding-left: 10px">
          <pre>{{reduce}}</pre>
        </el-col>
      </div>
      <hr/>
      <div style="display: flex; flex-direction: column; height: 100%;">
        <el-col :span="24" style="overflow: auto;height: 100px">
          <pre>{{content}}</pre>
        </el-col>
      </div>
    </el-dialog>
    
    
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data(){
    return{
      logJson:[],
      hiveShow:false,
      mrShow:false,
      sql:'',
      content: '',
      map: '',
      reduce: '',
    }
  },
  created() {
    this.fetchJob();
  },
  methods:{
    async fetchJob(){
      const data = {action: 'L'};
      const res = await axios.post('http://10.1.103.48:8426/hadoop/hive_analysis/',data);
      this.logJson = res.data;
    },
    job_check(row){
      if(row.result == '未完成')
      {
        this.$message.error("无法查看未完成的任务");
        return;
      }
      const data = {action: 'N', job_id: row.job_id};
      axios.post('http://10.1.103.48:8426/hadoop/hive_analysis/',data).then(res=>{
        this.sql = res.data.sql;
        this.content = res.data.content;
        if(row.type == 'Hive')
        {
          this.hiveShow = true;
        }
        else {
          const [map, reduce] = this.sql.split(':::');
          this.map = map;
          this.reduce = reduce;
          this.mrShow = true;
        }
      });
    },
    analyzeHistory(){
      this.fetchJob();
    },
    HDFSPage(){
      window.open('http://10.1.103.48:50070', '_blank');
    },
    delete_job(row){
      const data = {action: 'D', job_id: row.job_id};
      axios.post('http://10.1.103.48:8426/hadoop/hive_analysis/',data).then(res=>{
        if(res.data.auth == 'Y')
        {
          this.$message.success("删除成功");
          this.fetchJob();
        }
        else {
          this.$message.error("删除失败");
        }
      });
    },
  }
}
</script>