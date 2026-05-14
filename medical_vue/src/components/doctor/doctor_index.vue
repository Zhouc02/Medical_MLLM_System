<template>
  <div>
    <el-container style='height: 100%'>
      <!-- 顶部导航栏 -->
      <el-header style='background: rgb(5,104,193); height: 75px'>
        <el-row>
          <el-col :span="2" style='height: 75px;display: flex;justify-content: center;align-items:center'>
            <img src="../../images/logo.png" alt="Logo" style="height: 56px;;border-radius: 20%">
          </el-col>
          <el-col :span="8" style='height: 75px'>
            <div style="line-height: 75px; color: white; text-align: center;font-size: 29px;font-family: '微软雅黑',serif">医学多模态大语言模型辅助诊断系统</div>
          </el-col>
          <el-col :span='12' style='height: 75px;'>
            <div style="line-height: 75px;text-align: right;font-size: 20px;color: white;font-family: '微软雅黑',serif;margin-right: 10px">医师：{{name}}，工号：{{ids}}</div>
          </el-col>
          <el-col :span='2' style='height: 75px;display: flex;justify-content: right;align-items:center;'>
            <el-button type="info" @click="logout" style='height: 49px;margin-right: 10px'>退出</el-button>
          </el-col>
        </el-row>
      </el-header>
      
      <el-container>
        <!-- 左侧功能区 -->
        <el-aside width="200px" style='position: absolute;bottom: 0;top: 75px;'>
          <!-- 这里可以放置左侧功能区列表的内容 -->
          <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleMenuSelect" style="height: calc(100vh - 75px); overflow-y: auto;">
            <el-menu-item index="doctor_check" style='height: calc((100vh - 75px) / 7)' >
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/doctor/doctor_check.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='辅助诊断'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>辅助诊断</span>
              </div>
            </el-menu-item>
            <el-menu-item index="doctor_history" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/doctor/doctor_history.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='患者病史'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>患者病史</span>
              </div>
            </el-menu-item>
            <el-menu-item index="doctor_help" style='height: calc((100vh - 75px) / 7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/doctor/doctor_help.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='医师互助'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>医师互助</span>
              </div>
            </el-menu-item>
            <el-menu-item index="doctor_feedback" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_feedback.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='系统反馈'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>系统反馈</span>
              </div>
            </el-menu-item>
            <el-menu-item index="doctor_handbook" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/doctor/doctor_note.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='操作手册'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>操作手册</span>
              </div>
            </el-menu-item>
            <!-- 添加其他菜单项 -->
          </el-menu>
        </el-aside>
        
        <!-- 页面主体内容 -->
        <el-main style='left: 200px;position: absolute;bottom: 0;top: 75px;right: 0;'>
          <!-- 这里可以放置页面主体内容的组件 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data(){
    return{
      ids: window.sessionStorage.getItem('id'),
      name: window.sessionStorage.getItem('name')
    }
  },
  methods:{
    logout() {
      window.sessionStorage.clear();
      this.$router.push("/login");
    },
    handleMenuSelect(index){
      this.$router.push({ path: `/${index}` });
    }
  }
}
</script>
<style>


</style>