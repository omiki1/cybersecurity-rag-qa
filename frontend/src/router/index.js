// 路由配置文件
import { createRouter, createWebHistory } from 'vue-router'

// 定义路由配置对象 --- 数组
// 测试阶段：临时移除登录路由与鉴权 meta（恢复方法见 docs/回顾/前端鉴权临时移除与恢复.md）
const routes = [
    {
        path: '/',
        redirect: '/login', // 首页进入先登录或注册（鉴权暂未强制拦截，未写守卫）
    },
    {
        // 预览用：登录页背景效果（鉴权守卫已临时移除，此路由不强制登录）
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
    },
    {
        path: '/chat', // RAG 对话页
        name: 'Chat',
        component: () => import('../views/Chat.vue'),
    },
]

// 创建路由实例 --- 使用 history 模式（访问路径中无 # 号）
const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 导出路由实例
export default router
