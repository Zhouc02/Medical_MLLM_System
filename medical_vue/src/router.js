import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login.vue'

//管理员界面
import managerHome from './components/manager/manager_index.vue'
import managerSystem from './components/manager/manager_system.vue'
import managerStaff from './components/manager/manager_staff.vue'
import managerPatient from './components/manager/manager_patient.vue'
import managerModel from './components/manager/manager_model.vue'
import managerTrain from './components/manager/manager_train.vue'
import managerFeedback from './components/manager/manager_feedback.vue'
import managerAnalysis from './components/manager/manager_analysis.vue'
import managerHive from './components/manager/manager_hive.vue'
import managerMapreduce from './components/manager/manager_mapreduce.vue'
import managerLogistory from './components/manager/manager_logistory.vue'

//医生界面
import doctorHome from './components/doctor/doctor_index.vue'
import doctorCheck from './components/doctor/doctor_check.vue'
import doctorHistory from './components/doctor/doctor_history.vue'
import doctorHelp from './components/doctor/doctor_help.vue'
import doctorFeedback from './components/doctor/doctor_feedback.vue'
import doctorLLM from './components/doctor/doctor_LLM.vue'
import doctorHandbook from './components/doctor/doctor_handbook.vue'
import tempTest from './components/temp_test.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    // 登录重定向
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },

    //管理员路由
    {
      path: '/manager_home', component: managerHome,
      redirect: '/manager_system',
      children: [
        {path: '/manager_system', component: managerSystem},
        {path: '/manager_staff', component: managerStaff},
        {path: '/manager_patient', component: managerPatient},
        {path: '/manager_model', component: managerModel},
        {path: '/manager_train', component: managerTrain},
        {path: '/manager_feedback', component: managerFeedback},
        {path: '/manager_analysis', component: managerAnalysis},
        {path: '/manager_hive', component: managerHive},
        {path: '/manager_mapreduce', component: managerMapreduce},
        {path: '/manager_logistory', component: managerLogistory},
      ]
    },

    //医生路由
    {
      path: '/doctor_home', component: doctorHome,
      redirect: '/doctor_check',
      children:[
        {path: '/doctor_check', component: doctorCheck},
        {path: '/doctor_history', component: doctorHistory},
        {path: '/doctor_help', component: doctorHelp},
        {path: '/doctor_feedback', component: doctorFeedback},
        {path: '/doctor_LLM', component: doctorLLM},
        {path: '/doctor_handbook', component: doctorHandbook},
        {path: '/temp_test', component: tempTest},
      ]
    },

  ],
  // mode:'history'
})

//挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to:将要访问的路径
  // from:跳转来的路径
  // next:放行函数 next()放行  next('/login') 强制跳转
  if (to.path === '/login') return next();
  // 获取token
  const tokenStr = window.sessionStorage.getItem('id');
  if (!tokenStr) return next('/login');
  next()
})
export default router
