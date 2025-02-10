import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios';
Vue.config.productionTip = false;

// 引入 Element UI
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(Element);

// 引入Echarts
import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import Navbar from './components/Navbar.vue' // 引入Navbar组件
// 全局注册Navbar组件
Vue.component('Navbar', Navbar);

// 请求拦截器，自动添加 Authorization 头部
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 设置路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.path !== '/login' && !token) {
    // 如果没有 token，跳转到登录页面
    next('/login');
  } else {
    next();
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
