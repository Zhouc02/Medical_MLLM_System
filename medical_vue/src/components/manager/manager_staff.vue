<template>
  <div>
    <!--顶部刷新、新增、搜索栏-->
    <el-col :span='24' style='display: flex;align-items:center;width: 100%;height: 70px;position: absolute;top: 0;left: 0;right: 0'>
      <!--刷新按钮-->
      <el-button @click='updateData' style='background-color: bisque;width: 85px;height: 55px;padding: 0;margin-left: 20px'>刷新列表</el-button>
      <!--添加员工按钮-->
      <el-button @click='showAddEmployeeDialog' type='success' style='width: 85px;height: 55px;padding: 0;margin-left: 40px'>新增员工</el-button>
      <!--顶部搜索栏，根据工号搜索-->
      <el-input v-model='searchKey' placeholder='输入工号搜索' style='width: 300px;margin-left: auto;margin-right: 10px'></el-input>
      <!--搜索按钮-->
      <el-button @click='searchForKey' style='width: 85px;height: 55px;padding: 0;margin-left: 10px;margin-right: 20px'>开始搜索</el-button>
      <!-- 添加员工的弹出框 -->
      <el-dialog
        title="新增员工"
        :visible.sync="dialogVisible"
        width="30%"
      >
        <!-- 输入框 -->
        <el-form ref="employeeForm" :model="employeeForm" label-width="80px">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="employeeForm.name" style='width: 400px'></el-input>
          </el-form-item>
          <el-form-item label="职位" prop="auth">
            <el-select v-model="employeeForm.auth" placeholder="请选择职位" style='width: 400px'>
              <el-option label="管理员" value="A"></el-option>
              <el-option label="医师" value="D"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="employeeForm.password" style='width: 400px'></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input type="password" v-model="employeeForm.confirmPassword" style='width: 400px'></el-input>
          </el-form-item>
        </el-form>
        
        <!-- 提交和取消按钮 -->
        <span slot="footer" class="dialog-footer">
        <el-button @click="cancelForm">取消</el-button>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </span>
      </el-dialog>
    </el-col>
    <!--表格区域-->
    <el-col :span='24' style='width: 100%;height: calc(100vh - 145px);position: absolute;left: 0;right: 0;bottom: 0'>
      <el-table :data='jsonData' style='width: 100%'>
        <el-table-column prop='id' label='工号'></el-table-column>
        <el-table-column prop='name' label='姓名'></el-table-column>
        <el-table-column prop='auth' label='职位'></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
    <!--更改员工信息-->
    <el-dialog
      title="员工信息更改"
      :visible.sync="updateVisible"
      width="30%"
    >
      <!-- 输入框 -->
      <el-form ref="updateForm" :model="updateForm" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="updateForm.name" style='width: 400px'></el-input>
        </el-form-item>
        <el-form-item label="职位" prop="auth">
          <el-select v-model="updateForm.auth" placeholder="请选择职位" style='width: 400px'>
            <el-option label="管理员" value="A"></el-option>
            <el-option label="医师" value="D"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="新密码" prop="password">
          <el-input type="password" v-model="updateForm.password" style='width: 400px'></el-input>
        </el-form-item>
      </el-form>
      <!-- 提交和取消按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelUpdateForm">取消</el-button>
        <el-button type="primary" @click="submitUpdateForm">提交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data(){
    return{
      searchKey: '',
      jsonData: [],
      dialogVisible: false,
      updateVisible: false,
      employeeForm:{
        name: '',
        auth: 'A',
        password: '',
        confirmPassword: ''
      },
      updateId:'',
      updateForm:{
        name:'',
        auth:'',
        password:'',
      },
    }
  },
  created() {
    this.fetchData();
  },
  methods:{
    async fetchData(){
      const res = await axios.post('http://10.1.103.48:8426/hadoop/manager_check/');
      this.jsonData = res.data;
      this.$message.success("数据刷新成功");
    },
    searchForKey(){
      if (!this.searchKey||this.searchKey.length<5)
      {
        this.$message.error("请重新输入搜索条件");
        return;
      }
      const data = {id: this.searchKey};
      axios.post('http://10.1.103.48:8426/hadoop/manager_search/', data).then(res=>{
        if(res.data[0].auth === 'W')
        {
          this.$message.error("未找到该员工");
        }
        else {
          this.jsonData=res.data;
        }
      });
    },
    handleEdit(row){
      this.updateVisible=true;
      this.updateId=row.id;
      this.updateForm.name=row.name;
      if(row.auth == '管理员') this.updateForm.auth='A';
      else this.updateForm.auth='D';
    },
    handleDelete(row){
      this.$confirm('确定删除该员工吗？','删除警告',{
        confirmButtonText: '确定',
        cancelButtonText:'取消',
        type: 'warning'
      }).then(()=>{
        if(row.id == window.sessionStorage.getItem('id')){
          this.$message({
            type:'error',
            message: '无法自己删除自己'
          });
          return;
        }
        const data = {id: row.id}
        axios.post('http://10.1.103.48:8426/hadoop/manager_delete/',data).then(res=>{
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
    updateData(){
      this.fetchData();
    },
    showAddEmployeeDialog(){
      this.dialogVisible = true;
    },
    submitUpdateForm(){
      const data = {
        id: this.updateId,
        name: this.updateForm.name,
        auth: this.updateForm.auth,
        password: this.updateForm.password
      };
      axios.post('http://10.1.103.48:8426/hadoop/manager_update/', data).then(res=>{
        if(res.data.auth === 'Y')
        {
          this.$message.success("更改成功");
          this.updateVisible=false;
          this.cancelUpdateForm();
          this.fetchData();
        }
        else {
          this.$message.error("更改失败，请重新检查数据");
        }
      });
    },
    submitForm(){
      if (!this.employeeForm.password || !this.employeeForm.confirmPassword) {
        this.$message.error('密码不能为空');
        return;
      }
      if(this.employeeForm.password !== this.employeeForm.confirmPassword)
      {
        this.$message.error("两次密码不同！");
        return;
      }
      if(this.employeeForm.password.length<6)
      {
        this.$message.error("密码长度不能少于六位！");
        return;
      }
      if (this.employeeForm.name.length < 2) {
        this.$message.error('姓名长度不能少于两位');
        return;
      }
      const data = {
        name: this.employeeForm.name,
        password: this.employeeForm.password,
        auth: this.employeeForm.auth
      };
      axios.post('http://10.1.103.48:8426/hadoop/manager_add/', data).then(res=>{
        if(res.data.auth === 'Y')
        {
          this.$message.success("添加成功");
          this.cancelForm();
          this.dialogVisible=false;
          this.fetchData();
        }
        else {
          this.$message.error("添加失败，请检查输入数据");
        }
      })
    },
    cancelUpdateForm(){
      this.updateForm.name='';
      this.updateForm.auth='';
      this.updateForm.password='';
      this.updateId='';
      this.updateVisible=false;
    },
    cancelForm(){
      this.employeeForm.name='';
      this.employeeForm.auth='A';
      this.employeeForm.password='';
      this.employeeForm.confirmPassword='';
      this.dialogVisible=false;
    }
  },
}
</script>