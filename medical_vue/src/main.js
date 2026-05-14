import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'
// 导入全局样式表
import './assets/css/global.css'

// JwChat 组件
import JwChat from 'jwchat'
Vue.use(JwChat)

import axios from 'axios'
import Print from './utils/vue-print-nb/src'
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts

Vue.use(Print)
// 配置请求的根路径
axios.defaults.baseURL = 'http://10.1.103.48:8426/'
// 挂载到vue
Vue.prototype.$http = axios

Vue.use(ElementUI);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
