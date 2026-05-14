<template>
  <div>
    <el-container style='height: 100%'>
      <!-- 顶部导航栏 -->
      <el-header style='background: rgb(5,104,193); height: 75px'>
        <el-row>
          <el-col :span="2" style='height: 75px;display: flex;justify-content: center;align-items:center'>
            <img src="../../images/logo.png" alt="Logo" style="height: 56px;;border-radius: 20%">
          </el-col>
          <el-col :span="9" style='height: 75px'>
            <div style="line-height: 75px; color: white; text-align: center;font-size: 29px;font-family: '微软雅黑',serif">医学多模态大语言模型辅助诊断系统管理后台</div>
          </el-col>
          <el-col :span='11' style='height: 75px;'>
            <div style="line-height: 75px;text-align: right;font-size: 20px;color: white;font-family: '微软雅黑',serif;margin-right: 10px">管理员：{{name}}，工号：{{ids}}</div>
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
            <el-menu-item index="manager_system" style='height: calc((100vh - 75px) / 7)' >
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_system.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='系统监控'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>系统监控</span>
              </div>
            </el-menu-item>
            <el-menu-item index="manager_staff" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_staff.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='员工管理'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>员工管理</span>
              </div>
            </el-menu-item>
            <el-menu-item index="manager_patient" style='height: calc((100vh - 75px) / 7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_patient.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='患者管理'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>患者管理</span>
              </div>
            </el-menu-item>
            <el-menu-item index="manager_model" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_model.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='模型管理'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>模型管理</span>
              </div>
            </el-menu-item>
            <!--<el-menu-item index="manager_train" style='height: calc((100vh - 75px) / 7)'>-->
            <!--  <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>-->
            <!--    <img src='../../images/manager/manager_train.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='训练管理'/>-->
            <!--    <span style='font-size: 15px;font-family: 微软雅黑,serif'>训练管理</span>-->
            <!--  </div>-->
            <!--</el-menu-item>-->
            <el-menu-item index="manager_feedback" style='height: calc((100vh - 75px) /  7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_feedback.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='系统反馈'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>系统反馈</span>
              </div>
            </el-menu-item>
            <el-menu-item index="manager_analysis" style='height: calc((100vh - 75px) / 7)'>
              <div style='display: flex;align-items: center;height: 100%;flex-direction: column;'>
                <img src='../../images/manager/manager_analysis.png' style='width: 55px;height: 50px;margin-top: 10px;' alt='日志分析'/>
                <span style='font-size: 15px;font-family: 微软雅黑,serif'>日志分析</span>
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