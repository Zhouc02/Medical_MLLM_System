<template>
  <div>
    <!--顶部刷新栏-->
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <!--刷新按钮-->
      <el-button @click='updateData' style='background-color: bisque;width: 85px;height: 55px;padding: 0;margin-left: 20px'>刷新列表</el-button>
      <!--新增按钮-->
      <el-button @click='showNewModel' type='success' style='width: 85px;height: 55px;padding: 0;margin-left: 40px'>新增模型</el-button>
      <!--top_p-->
      <el-input v-model='top_p' placeholder='top_p' style='width: 80px;margin-left: auto;margin-right: 10px'></el-input>
      <!--top_p-->
      <el-input v-model='top_k' placeholder='top_k' style='width: 80px;margin-left: 10px;margin-right: 10px'></el-input>
      <!--top_p-->
      <el-input v-model='temperature' placeholder='temperature' style='width: 80px;margin-left: 10px;margin-right: 10px'></el-input>
      <!--更新按钮-->
      <el-button @click='updateParams' type='warning' style='width: 85px;height: 40px;padding: 0;margin-left: 10px;margin-right: 20px'>PKT更新</el-button>
      
      
    </el-col>
    
    <el-dialog
      title="新增模型"
      :visible.sync="dialogVisible"
      width="30%"
    >
      <!-- 输入框 -->
      <el-form ref="newModel" :model="newModel" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="newModel.name" style='width: 400px'></el-input>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="newModel.path" style='width: 400px'></el-input>
        </el-form-item>
      </el-form>
      
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelForm">取消</el-button>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </span>
      
    </el-dialog>
    
    <!--表格区域-->
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='jsonData' style='width: 100%'>
        <el-table-column prop='name' label='名称'></el-table-column>
        <el-table-column prop='path' label='路径'></el-table-column>
        <el-table-column prop='create_time' label='创建时间'></el-table-column>
        <el-table-column prop='create_manager' label='创建人'></el-table-column>
        <!--<el-table-column prop='statu' label='状态'></el-table-column>-->
        <el-table-column prop='statu' label='状态'>
          <template slot-scope="scope">
            <span v-if="scope.row.statu === '已使用'" style='color: green;font-weight: bold'>正在使用</span>
            <span v-else-if="scope.row.statu === '待使用'" style='color: saddlebrown;font-weight: bold'>待使用</span>
            <span v-else>{{scope.row.statu}}</span>
          </template>
        </el-table-column>
        <el-table-column prop='size' label='模型大小(GB)'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type='success' @click='handleSwitch(scope.row)'>切换</el-button>
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
      dialogVisible:false,
      newModel:{
        name:'',
        path:'',
      },
      top_p:'',
      top_k:'',
      temperature:'',
    }
  },
  created() {
    this.fetchData();
  },
  methods:{
    async fetchData(){
      const res = await axios.post('http://10.1.103.48:8426/model/model_list/');
      this.jsonData = res.data;
      const data = {action: 'C'};
      const params = await axios.post('http://10.1.103.48:8426/model/model_params/',data)
      this.top_p = params.data.top_p;
      this.top_k = params.data.top_k;
      this.temperature = params.data.temperature;
      this.$message.success('数据刷新成功');
    },
    submitForm(){
      if(!this.newModel.name||!this.newModel.path)
      {
        this.$message.error("请输入正确的模型信息");
        return;
      }
      const data = {name: this.newModel.name, path: this.newModel.path, create_manager: window.sessionStorage.getItem('id')};
      axios.post('http://10.1.103.48:8426/model/model_add/',data).then(res=>{
        if(res.data.auth == 'Y')
        {
          this.$message.success("添加成功");
          this.dialogVisible = false;
          this.fetchData();
          this.newModel.path='';
          this.newModel.name='';
        }
        else {
          this.$message.error("添加失败");
        }
      });
    },
    cancelForm(){
      this.newModel.name='';
      this.newModel.path='';
      this.dialogVisible=false;
    },
    updateData(){
      this.fetchData();
    },
    showNewModel(){
      this.dialogVisible = true;
    },
    handleSwitch(row){
      if(row.statu == '已使用')
      {
        this.$message.error("该模型正在使用，不能切换");
        return;
      }
      const data = {path: row.path};
      axios.post('http://10.1.103.48:8426/model/model_switch/',data).then(res=>{
        if(res.data.auth === 'Y')
        {
          this.$message.success("切换成功，将在下次系统重启时生效");
          this.fetchData();
        }
        else{
          this.$message.error("切换失败");
        }
      });
    },
    handleDelete(row){
      if (row.statu == '已使用' || row.statu == '待使用')
      {
        this.$message.error("无法删除正在或即将使用的模型！");
        return;
      }
      const data = {path: row.path};
      axios.post('http://10.1.103.48:8426/model/model_delete/',data).then(res=>{
        if(res.data.auth === 'Y')
        {
          this.fetchData();
          this.$message.success("删除成功");
        }
        else
        {
          this.$message.error("删除失败");
        }
      });
    },
    updateParams(){
      if(!this.top_p || !this.top_k || this.temperature)
      {
        this.$message.error("请输入正确的模型超参数");
        return;
      }
      if(this.top_p>=1 || this.top_p<=0 || this.temperature>=10 || this.temperature<=0 || this.top_k<=0)
      {
        this.$message.error('超出数值范围');
        return;
      }
      const data = {action:'U', top_p: this.top_p, top_k:this.top_k, temperature: this.temperature};
      axios.post('http://10.1.103.48:8426/model/model_params/', data).then(res=>{
        if(res.data.auth === 'Y')
        {
          this.fetchData();
        }
        else
        {
          this.$message.error("设置失败");
        }
      });
    },
  },
}
</script>