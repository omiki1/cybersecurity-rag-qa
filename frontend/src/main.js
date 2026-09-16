import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// 引入路由
import router from './router'

// Element Plus 及其中文语言包
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// axios 全局配置
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000/' // 服务器请求路径公共部分
axios.defaults.headers.post['Content-Type'] = 'application/json' // post 请求发送 json 数据
axios.defaults.headers.put['Content-Type'] = 'application/json' // put 请求发送 json 数据
axios.interceptors.request.use(cfg=>{
    const token = sessionStorage.getItem('token')
    if (token) cfg.headers.Authorization = `Bearer ${token}`
    return cfg
})
// 创建应用实例
const app = createApp(App)

// 注册路由
app.use(router)

// 注册 Element Plus
app.use(ElementPlus, { locale: zhCn })

// 挂载 axios 到全局，使用 this.$axios 替代原生 axios
app.config.globalProperties.$axios = axios

// 测试阶段：临时移除登录鉴权守卫（恢复方法见 docs/回顾/前端鉴权临时移除与恢复.md）
app.mount('#app')
