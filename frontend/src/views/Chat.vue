<template>
    <div class="chat-container">
        <!-- 左侧历史记录栏 -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-logo">
                    <el-icon :size="22"><ChatDotRound /></el-icon>
                    <span class="sidebar-title">网络安全问答系统</span>
                </div>
                <el-button class="new-chat-btn" type="primary" size="small" round @click = 'newChat'>
                    <el-icon :size="16"><Plus /></el-icon>
                    <span>新对话</span>
                </el-button>
            </div>

            <div class="sidebar-search">
                <el-input
                    v-model="searchKeyword"
                    placeholder="搜索历史记录..."
                    :prefix-icon="Search"
                    size="small"
                    clearable
                />
            </div>

            <div class="history-list">
                <div
                    v-for="(item, index) in historyList"
                    :key="index"
                    class="history-item"
                    :class="{ active: item.active }"
                    @click="conversationLog(item.historyId)"
                >
                    <el-icon :size="16" class="history-icon"><ChatLineSquare /></el-icon>
                    <div class="history-content">
                        <span class="history-title">{{ item.title }}</span>
                        <span class="history-time">{{ item.time }}</span>
                    </div>
                    <el-dropdown
                        trigger="click"
                        placement="bottom-start"
                        @click.stop
                        @command="(command) => handleMenuCommand(command, item.historyId)"
                    >
                        <el-icon :size="14" class="history-more"><MoreFilled /></el-icon>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item command="delete">
                                    <el-icon :size="14"><Delete /></el-icon>
                                    <span>删除</span>
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </div>

            <div class="sidebar-footer">
                <div class="user-info">
                    <el-avatar :size="32" class="user-avatar">{{ username.charAt(0).toUpperCase() }}</el-avatar>
                    <span class="user-name">{{ username }}</span>
                  <span class="user-name">{{ email }}</span>
                </div>
                <el-button class="logout-btn" size="small" type="danger" plain @click="handleLogout">
                    <el-icon :size="14"><SwitchButton /></el-icon>
                    <span>退出登录</span>
                </el-button>
            </div>
        </aside>

        <!-- 右侧主聊天区域 -->
        <main class="main-area">
            <!-- 赛博朋克城市背景：仅对话进行时展示（新建对话空状态不展示，避免与 UI 重叠） -->
            <div class="cp-bg" v-if="messages.length > 0">
                <div class="cp-rings">
                    <div class="cp-ring cp-ring-a"></div>
                    <div class="cp-ring cp-ring-b"></div>
                    <div class="cp-ring cp-ring-c"></div>
                    <div class="cp-ring cp-core"></div>
                </div>
                <div class="cp-sweep"></div>
                <div class="cp-city">
                    <div class="bldg b1"></div>
                    <div class="bldg b2"></div>
                    <div class="bldg b3"></div>
                    <div class="bldg b4"></div>
                    <div class="bldg b5"></div>
                    <div class="bldg b6"></div>
                    <div class="bldg b7"></div>
                    <div class="bldg b8"></div>
                    <div class="bldg b9"></div>
                    <div class="bldg b10"></div>
                    <div class="bldg b11"></div>
                </div>
            </div>
            <!-- 顶部标题栏 -->
            <header class="chat-header">
                <div class="header-left">
                    <el-icon :size="20" class="header-icon"><ChatDotRound /></el-icon>
                    <span class="header-title">AI 智能对话</span>
                </div>
                <div class="header-right">
                    <el-tooltip content="清空对话" placement="bottom">
                        <el-button class="header-btn" :icon="Delete" circle size="small" />
                    </el-tooltip>
                </div>
            </header>

            <!-- 消息显示区域 -->
            <div class="message-area" ref="messageAreaRef" @scroll="handleScroll">
                <div v-if="messages.length === 0" class="empty-state">
                    <div class="empty-icon">
                        <el-icon :size="64"><ChatDotRound /></el-icon>
                    </div>
                    <h2 class="empty-title">你好，{{ username }}</h2>
                  <h2 class="empty-title">{{ email }}</h2>
                    <p class="empty-desc">有什么我可以帮助你的吗？</p>
                    <div class="quick-prompts">
                        <div
                            v-for="(prompt, idx) in quickPrompts"
                            :key="idx"
                            class="prompt-chip"
                            @click="question = prompt.text"
                        >
                            <el-icon :size="14"><Sunny /></el-icon>
                            <span>{{ prompt.text }}</span>
                        </div>
                    </div>
                </div>

                <div
                    v-for="(item, index) in messages"
                    :key="index"
                    class="message-item"
                    :class="item.role"
                >
                    <div class="message-avatar">
                        <el-avatar :size="36" v-if="item.role === 'user'">
                            {{ username.charAt(0).toUpperCase() }}
                        </el-avatar>
                        <el-avatar :size="36" v-else :src="assistantAvatar" class="ai-avatar">
                            AI
                        </el-avatar>
                    </div>
                    <div class="message-body">
                        <div class="message-role-name">
                            {{ item.role === 'user' ? username : 'AI 助手' }}
                        </div>
                        <div class="message-bubble">
                            <div class="message-content" v-html="renderMarkdown(item.content)"></div>
                        </div>
                    </div>
                </div>

<!--                <div v-if="isLoading" class="message-item assistant">-->
<!--                    <div class="message-avatar">-->
<!--                        <el-avatar :size="36" class="ai-avatar">AI</el-avatar>-->
<!--                    </div>-->
<!--                    <div class="message-body">-->
<!--                        <div class="message-role-name">AI 助手</div>-->
<!--                        <div class="message-bubble typing-bubble">-->
<!--                            <span class="typing-dot"></span>-->
<!--                            <span class="typing-dot"></span>-->
<!--                            <span class="typing-dot"></span>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->

                <!-- 回到底部悬浮按钮：用户上翻历史后出现，点击滚回最新消息 -->
                <transition name="fade">
                    <button
                        v-if="!isAtBottom"
                        class="back-to-bottom"
                        @click="scrollToBottom(true)"
                        title="回到底部"
                    >
                        <el-icon :size="18"><ArrowDown /></el-icon>
                    </button>
                </transition>
            </div>

            <!-- 底部输入区域 -->
            <footer class="input-area">
                <div class="input-wrapper">
                    <div class="input-row">
                        <el-input
                            v-model="question"
                            placeholder="输入你的问题，按 Enter 发送..."
                            class="chat-input"
                            size="large"
                            :disabled="isLoading"
                            @keyup.enter="chat"
                        >
                            <template #suffix>
                                <el-button
                                    type="primary"
                                    :icon="Promotion"
                                    circle
                                    size="small"
                                    :disabled="isLoading || !question.trim()"
                                    @click="chat"
                                    class="send-btn"
                                />
                            </template>
                        </el-input>
                    </div>
                    <p class="input-hint">AI 回答仅供参考，请核实重要信息</p>
                </div>
            </footer>
        </main>
    </div>
</template>

<script setup>
import { ref, watch, nextTick, getCurrentInstance, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import {
    ArrowDown,
    ChatDotRound,
    ChatLineSquare,
    Plus,
    Search,
    MoreFilled,
    Delete,
    Promotion,
    Sunny,
    SwitchButton,
} from '@element-plus/icons-vue'
import {fetchEventSource} from "@microsoft/fetch-event-source";
import { useRouter } from 'vue-router'

// ========== 后端服务地址配置 ==========
// axios 的公共前缀在 src/main.js 中配置，SSE 的 EventSource 需要手动拼接完整地址
const SSE_URL = 'http://localhost:8000/chat/chat'

// 获取当前实例对象
let proxy = getCurrentInstance().proxy

// 路由实例（退出登录后跳转登录页）
const router = useRouter()

// ========== 退出登录 ==========
function handleLogout() {
    // ① 通知后端把当前 token 的 jti 拉入黑名单（axios 拦截器会自动带 Authorization）
    proxy.$axios({
        url: 'auth/logout',
        method: 'post',
    }).catch(() => {
        // token 已失效时后端返回 401，本地退出流程仍需继续
    }).finally(() => {
        // ② 无论接口成败，都清除本地登录态
        sessionStorage.removeItem('token')
        sessionStorage.removeItem('username')
        sessionStorage.removeItem('email')
        sessionStorage.removeItem('role')
        // ③ 回到登录页
        router.push('/login')
    })
}

// 接收用户名称的变量
let username = ref('')
let email = ref('')
// 用户问题
let question = ref('')

// 保存聊天消息的对象
let messages = ref([])
// 侧栏历史记录
let historyList = ref([])
// 控制聊天按钮是否可以点击的变量
let isLoading = ref(false)

// ========== 历史记录栏数据 ==========
const searchKeyword = ref('')
const assistantAvatar = ref('')
const currentChatId = ref(0)

// ========== 自动滚动到底部 ==========
// 滚动容器：对应模板中 ref="messageAreaRef"
const messageAreaRef = ref(null)
// 用户是否停留在"底部附近"（默认 true：初始页面就在最底部）
const isAtBottom = ref(true)
// 距离底部多少像素内，算作"在底部附近"
const SCROLL_THRESHOLD = 50

// 判断滚动容器当前是否靠近底部
// scrollHeight：内容总高度；scrollTop：已滚动的距离；clientHeight：可视区高度
// scrollTop 最大只能滚到 scrollHeight - clientHeight，差值趋近 0 说明在底部
function isNearBottom() {
    const el = messageAreaRef.value
    if (!el) return true
    return el.scrollHeight - el.scrollTop - el.clientHeight < SCROLL_THRESHOLD
}

// 滚动到底部。smooth=true 用平滑动画（点按钮时），false 直接跳（流式输出时更跟手）
function scrollToBottom(smooth = false) {
    const el = messageAreaRef.value
    if (!el) return
    el.scrollTo({ top: el.scrollHeight, behavior: smooth ? 'smooth' : 'auto' })
}

// 滚动事件：用户一上翻，isAtBottom 变 false → 停止自动跟随
function handleScroll() {
    isAtBottom.value = isNearBottom()
}

// 深度监听 messages：
// 为什么 deep？SSE 流式输出改的是 messages[i].content（数组里对象的属性），
// 数组引用本身没变，浅监听不会触发；deep 才能捕捉"每一帧流式数据"的更新。
watch(messages, async () => {
    await nextTick() // 等 Vue 把最新消息渲染进 DOM，再读 scrollHeight 才准确
    if (isAtBottom.value) {
        scrollToBottom(false) // 用户在看底部 → 自动跟随
    }
}, { deep: true })

const quickPrompts = ref([
    { text: "帮我写一段代码" },
    { text: "解释一个技术概念" },
    { text: "帮我优化这段代码" },
    { text: "推荐学习路线" },
])

// ========== Markdown 渲染 ==========
// markdown-it：把 AI 回答渲染成富文本
// html:false → 转义回答里的原始 HTML，防止 XSS
const md = new MarkdownIt({ html: false, linkify: true, breaks: true })

function renderMarkdown(text) {
    return md.render(text || '')
}

// ========== 聊天函数（SSE 流式输出） ==========
function chat() {
  isLoading.value = true // 置为 true，表示正在生成回答

  let myQuestion = question.value.trim() // 取出问题并去掉首尾空格
  question.value = "" // 清空输入框

  // 判断是否输入了内容
  if (myQuestion.length === 0) {
    ElMessage.warning("请输入内容")
    return
  }

  // 用户发送消息时强制回到跟随最新状态
  isAtBottom.value = true

  // 先把用户问题和占位回复插入消息列表
  messages.value.push({role: 'user', content: myQuestion})
  messages.value.push({role: 'assistant', content: 'AI正在努力的生成回复ing~~~'})

  // 拼接流式结果
  let s = ''
  const token = sessionStorage.getItem("token")
  const controller = new AbortController()
  try {
    fetchEventSource(SSE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        question: myQuestion,
        historyId: currentChatId.value
      }),
      signal: controller.signal,
      onopen(response) {

        if (response.status === 401) {
          controller.abort()
          messages.value.splice(messages.value.length - 2, 2)
          isLoading.value = false
          ElMessage.error('登录已失效，请重新登录')
          throw new Error("登录已失效")
        }

        // 游客（role_name=guest）持有合法 token 但无角色权限，后端返回 403
        if (response.status === 403) {
          controller.abort()
          messages.value.splice(messages.value.length - 2, 2)
          isLoading.value = false
          ElMessage.error('无资格使用')
          throw new Error("无资格使用")
        }

        if (!response.ok) {
          controller.abort()
          messages.value.splice(messages.value.length - 2, 2)
          isLoading.value = false
          throw new Error(
              `请求失败：${response.status}`
          )
        }
      },
      onmessage(e) {

        const data = JSON.parse(e.data).content

        if (data === '[DONE]') {

          controller.abort()

          saveConversationResult(
              myQuestion,
              s
          )

          isLoading.value = false

          return
        }

        s += data

        messages.value[
        messages.value.length - 1
            ].content = s
      },

    })
  } catch (error) {

    console.error(error)

    isLoading.value = false
  }
}
// ========== 查询聊天历史记录菜单栏 =============
function query_history_menu(){
    proxy.$axios({
        url: 'history/queryHistoryMenu',
        method:'get',
        params:{
            username:username.value
        }
    }).then(res=>{
        historyList.value = res.data.data
    }).catch(()=>{
        // 游客(403)或未登录(401)时静默，历史栏保持为空
    })
}
// ========== 查询某一条详细对话记录 ==========
function conversationLog(hitstoryId){
    currentChatId.value = hitstoryId
    proxy.$axios({
        url: 'history/conversationLog',
        method : 'get',
        params : {
            historyId : hitstoryId
        }
    }).then(res=>{
        messages.value = res.data.data;
        // 切换历史对话后：强制恢复"跟随最新"，并主动滚到最新一条。
        // 为什么要主动滚？messages 整体替换后，浏览器会保留旧的 scrollTop，
        // 内容变长时 scrollTop 仍停在原值，看起来就是"弹到最上面"。
        isAtBottom.value = true
        nextTick(() => scrollToBottom(false))
    })
}
// ========== 持久化对话记录 ==========
function saveConversationResult(question,answer){
    proxy.$axios({
        url: 'history/saveConversationResult',
        method:'post',
        data: JSON.stringify({
            question: question,
            username: username.value,
            parentId: currentChatId.value,
            answer: answer,
        })
    }).then(res=>{
        if(currentChatId.value===0){
            currentChatId.value = res.data.data
        }
        query_history_menu();
    })
}
function newChat(){
    currentChatId.value = 0;
    messages.value=[]
}
function handleMenuCommand(command, historyId){
    if(command === 'delete'){
        deleteConversationResult(historyId)
    }
}
function deleteConversationResult(historyId){
    proxy.$axios({
        url: 'history/deleteConversationResult',
        method : 'get',
        params : {
            historyId : historyId
        }
    }).then(res=>{
        ElMessage.success('删除成功')
        // 如果删除的是当前正在查看的对话，重置回新对话状态
        if(currentChatId.value === historyId){
            currentChatId.value = 0
            messages.value = []
        }
        query_history_menu()
    }).catch(()=>{
        ElMessage.error('删除失败')
    })
}

// 挂载函数：页面加载后从 sessionStorage 取用户名
// 测试阶段：未登录时给默认值 guest，避免 username.charAt(0) 空指针崩溃
onMounted(() => {
    username.value = sessionStorage.getItem('username') || 'guest'
    email.value = sessionStorage.getItem('email') || ''
    // 游客(role=guest)无问答资格，也不拉历史（后端 /history 接口同样 403）
    if (sessionStorage.getItem('role') !== 'guest') {
        query_history_menu()
    }
    // 页面加载后滚到底部（如刷新后停留在历史对话，直接看到最新内容）
    scrollToBottom(false)
})
</script>

<style scoped>
/* ========== 全局变量 ========== */
:root {
    --sidebar-width: 280px;
    --sidebar-bg: #12140d;
    --sidebar-hover: #1c2015;
    --sidebar-active: #1a200f;
    --primary: #b6ff00;
    --primary-light: #c9ff4d;
    --primary-bg: rgba(182, 255, 0, 0.08);
    --user-bubble: rgba(182, 255, 0, 0.06);
    --ai-bubble: #171a12;
    --text-primary: #f0f3e4;
    --text-secondary: #a6ad97;
    --border-color: #33382a;
    --bg-main: #0d0f0a;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --radius-xl: 12px;
}

/* ========== 整体布局 ========== */
.chat-container {
    display: flex;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
    position: relative;
    background: #0a0b08;
    font-family: var(--font-term);
}

/* ========== 左侧边栏 ========== */
.sidebar {
    width: var(--sidebar-width);
    min-width: var(--sidebar-width);
    height: 100vh;
    background: rgba(15, 17, 12, .92);
    display: flex;
    flex-direction: column;
    border-right: 1px solid rgba(44, 49, 37, .9);
    user-select: none;
    position: relative;
    z-index: 1;
}

.sidebar-header {
    padding: 20px 16px 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    border-bottom: 1px solid #2c3125;
    position: relative;
}

/* 警示条纹分隔线 */
.sidebar-header::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    bottom: -1px;
    height: 4px;
    background: repeating-linear-gradient(45deg, #ffb000 0 10px, #1a1a1a 10px 20px);
    opacity: .7;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--neon-green);
}

.sidebar-title {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--neon-green);
    text-shadow: 0 0 8px rgba(182, 255, 0, .5);
}

.new-chat-btn {
    width: 100%;
    background: transparent !important;
    border: 1px solid var(--neon-green) !important;
    color: var(--neon-green) !important;
    font-weight: 500;
    height: 38px;
    letter-spacing: 2px;
    transition: all 0.3s ease;
}

.new-chat-btn:hover {
    background: rgba(182, 255, 0, 0.12) !important;
    box-shadow: 0 0 16px rgba(182, 255, 0, 0.25) !important;
}

.sidebar-search {
    padding: 12px 16px;
}

.sidebar-search :deep(.el-input__wrapper) {
    background: #10130c;
    border: 1px solid #33382a;
    border-radius: 4px;
    box-shadow: none;
    transition: all 0.2s;
}

.sidebar-search :deep(.el-input__wrapper:hover) {
    border-color: #4a5040;
}

.sidebar-search :deep(.el-input__wrapper.is-focus) {
    border-color: var(--neon-green);
    box-shadow: 0 0 0 1px rgba(182, 255, 0, 0.3), 0 0 10px rgba(182, 255, 0, 0.12);
}

.sidebar-search :deep(.el-input__inner) {
    color: #dde3c8;
}

.sidebar-search :deep(.el-input__inner::placeholder) {
    color: #565d4b;
}

.sidebar-search :deep(.el-input__prefix) {
    color: #565d4b;
}

/* 历史记录列表 */
.history-list {
    flex: 1;
    overflow-y: auto;
    padding: 4px 12px;
    scroll-behavior: smooth;
}

.history-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    margin-bottom: 2px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #a3aa8f;
    position: relative;
    border-left: 2px solid transparent;
}

.history-item:hover {
    background: var(--sidebar-hover);
    color: #dde3c8;
}

.history-item:hover .history-more {
    opacity: 1;
}

.history-item.active {
    background: var(--sidebar-active);
    color: #dde3c8;
    border-left: 2px solid var(--neon-green);
    box-shadow: inset 0 0 20px rgba(182, 255, 0, 0.05);
}

.history-item.active .history-icon {
    color: var(--neon-green);
}

.history-icon {
    flex-shrink: 0;
    color: #8a9279;
    transition: color 0.2s;
}

.history-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.history-title {
    font-size: 13px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-time {
    font-size: 11px;
    color: #7a8371;
}

.history-more {
    flex-shrink: 0;
    opacity: 0;
    transition: opacity 0.2s;
    color: #6f7660;
    cursor: pointer;
}

.history-more:hover {
    color: var(--neon-amber);
}

/* 侧边栏底部用户信息 */
.sidebar-footer {
    padding: 14px 16px;
    border-top: 1px solid #2c3125;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.logout-btn {
    width: 100%;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-avatar {
    background: linear-gradient(135deg, #8fcc00, #39ff14) !important;
    color: #0a0b08 !important;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 0 10px rgba(182, 255, 0, 0.4);
}

.user-name {
    font-size: 14px;
    font-weight: 500;
    color: #dde3c8;
}

/* ========== 右侧主区域 ========== */
.main-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    background: rgba(13, 15, 10, .78);
    position: relative;
    z-index: 1;
}

/* 顶部标题栏 */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: rgba(18, 20, 13, .92);
    border-bottom: 1px solid var(--border-color);
    flex-shrink: 0;
    position: relative;
    z-index: 1;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.header-icon {
    color: var(--neon-green);
    text-shadow: 0 0 8px rgba(182, 255, 0, 0.6);
}

.header-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 1px;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-btn {
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    background: transparent !important;
    transition: all 0.2s;
}

.header-btn:hover {
    color: var(--neon-danger) !important;
    border-color: rgba(255, 51, 85, 0.5) !important;
    background: rgba(255, 51, 85, 0.1) !important;
    box-shadow: 0 0 10px rgba(255, 51, 85, 0.2);
}

/* 消息显示区域 */
.message-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    scroll-behavior: smooth;
    position: relative;
    z-index: 1;
    background: rgba(9, 11, 7, .30);
}

/* 空状态 */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 8px;
    padding: 40px 20px;
}

.empty-icon {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: var(--primary-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
    color: var(--neon-green);
    box-shadow: 0 0 24px rgba(182, 255, 0, 0.2), inset 0 0 20px rgba(182, 255, 0, 0.08);
}

.empty-title {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: 1px;
}

.empty-desc {
    font-size: 15px;
    color: var(--text-secondary);
    margin: 0 0 20px;
}

.quick-prompts {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    max-width: 500px;
}

.prompt-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 4px;
    border: 1px solid #33382a;
    background: #12140d;
    color: var(--text-secondary);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}

.prompt-chip:hover {
    border-color: var(--neon-green);
    color: var(--neon-green);
    transform: translateY(-1px);
    box-shadow: 0 0 12px rgba(182, 255, 0, 0.2);
}

/* 消息项 */
.message-item {
    display: flex;
    gap: 14px;
    margin-bottom: 24px;
    animation: messageIn 0.3s ease;
}

@keyframes messageIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-item.user {
    flex-direction: row-reverse;
}

.message-item.user .message-body {
    align-items: flex-end;
}

.message-item.user .message-role-name {
    text-align: right;
}

.message-avatar {
    flex-shrink: 0;
    margin-top: 4px;
}

.message-avatar :deep(.el-avatar) {
    box-shadow: var(--shadow-sm);
}

.ai-avatar {
    background: linear-gradient(135deg, #00f0ff, #00b8c9) !important;
    color: #001a1c !important;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.35);
}

.message-body {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-width: 70%;
}

.message-role-name {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    padding: 0 4px;
    letter-spacing: 1px;
}

.message-bubble {
    padding: 12px 18px;
    border-radius: var(--radius-lg);
    line-height: 1.6;
    font-size: 14px;
    word-break: break-word;
    position: relative;
}

/* 用户消息：毒绿霓虹框 */
.message-item.user .message-bubble {
    background: rgba(182, 255, 0, 0.06);
    color: var(--neon-green);
    border: 1px solid rgba(182, 255, 0, 0.5);
    border-bottom-right-radius: 4px;
    box-shadow: 0 0 14px rgba(182, 255, 0, 0.12);
}

/* AI 消息：暗色青边面板 */
.message-item.assistant .message-bubble {
    background: #171a12;
    color: var(--text-primary);
    border: 1px solid #33382a;
    border-left: 3px solid var(--neon-cyan);
    border-bottom-left-radius: 4px;
    box-shadow: var(--shadow-sm);
}

.message-content {
    white-space: pre-wrap;
}

/* 回到底部悬浮按钮：仅在用户离开底部（上翻历史）时出现 */
.back-to-bottom {
    position: absolute;
    right: 24px;
    bottom: 24px;
    z-index: 3;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: rgba(18, 20, 13, .95);
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 0 14px rgba(182, 255, 0, .35);
    transition: all .2s ease;
}

.back-to-bottom:hover {
    background: rgba(182, 255, 0, .15);
    box-shadow: 0 0 20px rgba(182, 255, 0, .55);
    transform: translateY(-2px);
}

/* 按钮淡入淡出 */
.fade-enter-active,
.fade-leave-active {
    transition: opacity .2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* 打字动画 */
.typing-bubble {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 18px !important;
}

.typing-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--neon-green);
    animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) {
    animation-delay: 0s;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typingBounce {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    30% {
        transform: translateY(-6px);
        opacity: 1;
    }
}

/* 底部输入区域 */
.input-area {
    padding: 16px 24px 20px;
    background: rgba(18, 20, 13, .92);
    border-top: 1px solid var(--border-color);
    flex-shrink: 0;
    position: relative;
    z-index: 1;
}

.input-area::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-green), transparent);
    opacity: .5;
}

.input-wrapper {
    max-width: 900px;
    margin: 0 auto;
}

.input-row {
    display: flex;
    align-items: center;
}

.chat-input :deep(.el-input__wrapper) {
    border-radius: 6px;
    padding: 6px 16px;
    background: #10130c;
    border: 1px solid #33382a;
    box-shadow: none;
    transition: all 0.3s ease;
}

.chat-input :deep(.el-input__wrapper:hover) {
    border-color: #4a5040;
}

.chat-input :deep(.el-input__wrapper.is-focus) {
    border-color: var(--neon-green);
    box-shadow: 0 0 0 1px rgba(182, 255, 0, 0.3), 0 0 14px rgba(182, 255, 0, 0.12);
}

.chat-input :deep(.el-input__inner) {
    font-size: 14px;
    color: var(--text-primary);
}

.chat-input :deep(.el-input__inner::placeholder) {
    color: #565d4b;
}

.send-btn {
    background: transparent !important;
    border: 1px solid var(--neon-green) !important;
    color: var(--neon-green) !important;
    transition: all 0.3s ease;
}

.send-btn:hover {
    background: rgba(182, 255, 0, 0.15) !important;
    box-shadow: 0 0 14px rgba(182, 255, 0, 0.3) !important;
}

.send-btn.is-disabled {
    border-color: #3a4031 !important;
    color: #565d4b !important;
    background: transparent !important;
    transform: none !important;
    box-shadow: none !important;
}

.input-hint {
    text-align: center;
    font-size: 11px;
    color: #7a8371;
    margin: 8px 0 0;
    letter-spacing: 1px;
}

/* ===== Markdown 渲染内容 ===== */
.message-content {
    line-height: 1.7;
}

.message-content :deep(h1),
.message-content :deep(h2),
.message-content :deep(h3),
.message-content :deep(h4) {
    color: var(--neon-green);
    text-shadow: 0 0 10px rgba(182, 255, 0, .4);
    margin: 1.2em 0 .5em;
    line-height: 1.3;
}

.message-content :deep(h1) {
    font-size: 1.4em;
    border-bottom: 1px solid rgba(182, 255, 0, .25);
    padding-bottom: .3em;
}

.message-content :deep(h2) { font-size: 1.25em; }
.message-content :deep(h3) { font-size: 1.1em; }
.message-content :deep(h4) { font-size: 1em; }

.message-content :deep(p) { margin: .6em 0; }

.message-content :deep(strong) {
    color: var(--neon-green);
    font-weight: 700;
}

.message-content :deep(a) {
    color: var(--neon-cyan);
    text-decoration: underline;
    text-shadow: 0 0 6px rgba(0, 240, 255, .4);
}

.message-content :deep(a:hover) { color: #fff; }

.message-content :deep(code) {
    background: rgba(182, 255, 0, .08);
    border: 1px solid rgba(182, 255, 0, .2);
    color: var(--neon-green);
    padding: 1px 5px;
    border-radius: 3px;
    font-family: var(--font-term);
    font-size: .92em;
}

.message-content :deep(pre) {
    background: #0d100a;
    border: 1px solid #33382a;
    border-left: 3px solid var(--neon-cyan);
    border-radius: 4px;
    padding: 12px 14px;
    overflow-x: auto;
    margin: .8em 0;
    box-shadow: 0 0 10px rgba(0, 240, 255, .08);
}

.message-content :deep(pre code) {
    background: transparent;
    border: none;
    color: #dde3c8;
    padding: 0;
    font-size: .92em;
}

.message-content :deep(ul),
.message-content :deep(ol) {
    padding-left: 1.5em;
    margin: .6em 0;
}

.message-content :deep(li) { margin: .2em 0; }
.message-content :deep(li::marker) { color: var(--neon-green); }

.message-content :deep(blockquote) {
    border-left: 3px solid var(--neon-amber);
    margin: .8em 0;
    padding: 2px 14px;
    color: var(--text-mid);
    background: rgba(255, 176, 0, .05);
}

.message-content :deep(table) {
    border-collapse: collapse;
    margin: .8em 0;
    width: 100%;
    font-size: .92em;
}

.message-content :deep(th),
.message-content :deep(td) {
    border: 1px solid #33382a;
    padding: 6px 10px;
    text-align: left;
}

.message-content :deep(th) {
    background: rgba(182, 255, 0, .08);
    color: var(--neon-green);
}

.message-content :deep(hr) {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(182, 255, 0, .4), transparent);
    margin: 1em 0;
}

.message-content :deep(img) {
    max-width: 100%;
    border: 1px solid #33382a;
    border-radius: 4px;
}

/* ===== 荧光辉光增强 ===== */
@keyframes neonPulse {
    0%, 100% {
        box-shadow: 0 0 8px rgba(182, 255, 0, .4), 0 0 20px rgba(182, 255, 0, .15);
    }
    50% {
        box-shadow: 0 0 16px rgba(182, 255, 0, .8), 0 0 36px rgba(182, 255, 0, .35);
    }
}

@keyframes neonPulseCyan {
    0%, 100% {
        box-shadow: 0 0 8px rgba(0, 240, 255, .4), 0 0 20px rgba(0, 240, 255, .15);
    }
    50% {
        box-shadow: 0 0 16px rgba(0, 240, 255, .8), 0 0 36px rgba(0, 240, 255, .35);
    }
}

/* 发送按钮：呼吸荧光 */
.send-btn:not(.is-disabled) {
    animation: neonPulse 2s ease-in-out infinite;
}

/* 新对话按钮：呼吸荧光 */
.new-chat-btn {
    animation: neonPulse 3s ease-in-out infinite;
}

/* 用户消息气泡：更强绿光 */
.message-item.user .message-bubble {
    box-shadow:
        0 0 12px rgba(182, 255, 0, .25),
        0 0 30px rgba(182, 255, 0, .1),
        inset 0 0 12px rgba(182, 255, 0, .05);
}

/* AI 消息气泡：青色荧光边 */
.message-item.assistant .message-bubble {
    box-shadow:
        0 0 10px rgba(0, 240, 255, .1),
        0 2px 8px rgba(0, 0, 0, .4);
}

/* 历史选中项：绿条发光 */
.history-item.active {
    box-shadow:
        inset 0 0 20px rgba(182, 255, 0, .06),
        0 0 12px rgba(182, 255, 0, .15);
}

/* 头部图标：青色呼吸 */
.header-icon {
    animation: neonPulseCyan 2.5s ease-in-out infinite;
}

/* 空状态图标：绿色呼吸 */
.empty-icon {
    animation: neonPulse 3.5s ease-in-out infinite;
}

/* ===== 赛博朋克城市背景（初音未来配色 #39C5BB） ===== */
.cp-bg {
    position: absolute;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
    background: linear-gradient(180deg, #0a0c08 0%, #0c0f09 55%, #0a0c08 100%);
}

.cp-rings {
    position: absolute;
    left: 50%;
    top: 40%;
    width: 0;
    height: 0;
}

.cp-ring {
    position: absolute;
    left: 0;
    top: 0;
    border-radius: 50%;
}

/* 外圈：初音青绿，带刻度环 */
.cp-ring-a {
    width: 430px;
    height: 430px;
    transform: translate(-50%, -50%);
    border: 2px solid rgba(57, 197, 187, .3);
    box-shadow: 0 0 40px rgba(57, 197, 187, .2), inset 0 0 40px rgba(57, 197, 187, .08);
    animation: ringPulseMiku 6s ease-in-out infinite;
}

.cp-ring-a::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 50%;
    border: 1px dashed rgba(57, 197, 187, .25);
    animation: ringSpin 24s linear infinite;
}

/* 中圈：品红 */
.cp-ring-b {
    width: 310px;
    height: 310px;
    transform: translate(-50%, -50%);
    border: 1px solid rgba(255, 43, 214, .22);
    box-shadow: 0 0 30px rgba(255, 43, 214, .15), inset 0 0 30px rgba(255, 43, 214, .05);
    animation: ringPulsePink 6s ease-in-out infinite 1.5s;
}

.cp-ring-b::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 50%;
    border: 2px solid transparent;
    border-top-color: rgba(255, 43, 214, .8);
    animation: ringSpin 8s linear infinite;
}

/* 内圈：毒绿 */
.cp-ring-c {
    width: 190px;
    height: 190px;
    transform: translate(-50%, -50%);
    border: 1px solid rgba(182, 255, 0, .45);
    box-shadow: 0 0 30px rgba(182, 255, 0, .35), inset 0 0 20px rgba(182, 255, 0, .12);
    animation: ringPulseGreen 4s ease-in-out infinite;
}

.cp-ring-c::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 50%;
    border: 2px solid transparent;
    border-bottom-color: rgba(182, 255, 0, .9);
    animation: ringSpin 5s linear infinite reverse;
}

/* 核心光点 */
.cp-core {
    width: 56px;
    height: 56px;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle, #fff 0%, rgba(57, 197, 187, .9) 30%, rgba(57, 197, 187, 0) 70%);
    box-shadow: 0 0 40px rgba(57, 197, 187, .7), 0 0 90px rgba(57, 197, 187, .3);
    animation: corePulse 3s ease-in-out infinite;
}

/* 城市天际线：初音青绿线条 */
.cp-city {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 38%;
    z-index: 1;
}

.bldg {
    position: absolute;
    bottom: 0;
    /* 每栋楼的霓虹主色，由下方 .b1~.b11 各自覆盖，形成青绿系多元色调 */
    --glow: #39c5bb;
    background: linear-gradient(180deg, #12160e, #090b07);
    border-top: 1px solid color-mix(in srgb, var(--glow) 55%, transparent);
    box-shadow: 0 0 12px color-mix(in srgb, var(--glow) 12%, transparent); /* 光晕范围较原来略大 */
}

.bldg::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(90deg, transparent 0 8px, color-mix(in srgb, var(--glow) 8%, transparent) 8px 10px),
        repeating-linear-gradient(0deg, transparent 0 12px, color-mix(in srgb, var(--glow) 6%, transparent) 12px 14px);
}

/* 大楼楼角：青绿系霓虹角，被照亮时亮起，跟随每栋楼的 --glow 变色 */
.bldg::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 20px;
    background: linear-gradient(180deg, var(--glow), transparent);
    box-shadow: 0 0 16px color-mix(in srgb, var(--glow) 80%, transparent);
    opacity: 0;
    animation: cornerGlow 7s ease-in-out infinite;
}

.bldg:nth-child(2n)::after { animation-delay: 1s; }
.bldg:nth-child(3n)::after { animation-delay: 2.5s; }

/* 光束扫过城市 */
.cp-sweep {
    position: absolute;
    left: 0;
    right: 0;
    top: -10%;
    bottom: 0;
    z-index: 2;
    background: linear-gradient(180deg,
        rgba(57, 197, 187, 0) 0%,
        rgba(57, 197, 187, .08) 32%,
        rgba(182, 255, 0, .10) 45%,
        rgba(255, 43, 214, .05) 55%,
        rgba(0, 0, 0, 0) 75%);
    opacity: 0;
    animation: citySweep 7s ease-in-out infinite;
    pointer-events: none;
}

/* 大楼配色：同一青绿系内，每栋楼不同色调，呈现多元霓虹 */
.b1  { --glow: #39c5bb; }
.b2  { --glow: #4fd8c4; }
.b3  { --glow: #2ea8a0; }
.b4  { --glow: #5be0ce; }
.b5  { --glow: #3ab8c9; }
.b6  { --glow: #46d0a8; }
.b7  { --glow: #6ae3d0; }
.b8  { --glow: #2cbf9b; }
.b9  { --glow: #35c7c2; }
.b10 { --glow: #7adbc4; }
.b11 { --glow: #25978f; }

/* 大楼布局 */
.b1  { left: 3%;  width: 9%;  height: 52%; }
.b2  { left: 12%; width: 7%;  height: 78%; }
.b3  { left: 19%; width: 10%; height: 44%; }
.b4  { left: 29%; width: 6%;  height: 68%; }
.b5  { left: 35%; width: 11%; height: 90%; }
.b6  { left: 46%; width: 8%;  height: 58%; }
.b7  { left: 54%; width: 12%; height: 74%; }
.b8  { left: 66%; width: 7%;  height: 48%; }
.b9  { left: 73%; width: 10%; height: 84%; }
.b10 { left: 83%; width: 8%;  height: 55%; }
.b11 { left: 91%; width: 9%;  height: 66%; }

/* ===== 城市背景动画 ===== */
@keyframes ringSpin {
    to { transform: rotate(360deg); }
}

@keyframes ringPulseMiku {
    0%, 100% { box-shadow: 0 0 20px rgba(57, 197, 187, .12), inset 0 0 20px rgba(57, 197, 187, .04); }
    50% { box-shadow: 0 0 60px rgba(57, 197, 187, .45), inset 0 0 60px rgba(57, 197, 187, .16); }
}

@keyframes ringPulsePink {
    0%, 100% { box-shadow: 0 0 15px rgba(255, 43, 214, .1), inset 0 0 15px rgba(255, 43, 214, .03); }
    50% { box-shadow: 0 0 45px rgba(255, 43, 214, .35), inset 0 0 45px rgba(255, 43, 214, .12); }
}

@keyframes ringPulseGreen {
    0%, 100% { box-shadow: 0 0 15px rgba(182, 255, 0, .18), inset 0 0 15px rgba(182, 255, 0, .06); }
    50% { box-shadow: 0 0 50px rgba(182, 255, 0, .5), inset 0 0 30px rgba(182, 255, 0, .18); }
}

@keyframes corePulse {
    0%, 100% { opacity: .7; transform: translate(-50%, -50%) scale(1); }
    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.15); }
}

@keyframes cornerGlow {
    0%, 100% { opacity: 0; }
    40% { opacity: 1; }
    65% { opacity: 0; }
}

@keyframes citySweep {
    0% { opacity: 0; transform: translateY(-30px); }
    30% { opacity: 1; }
    55% { opacity: .2; }
    70% { opacity: 0; transform: translateY(40px); }
    100% { opacity: 0; transform: translateY(40px); }
}
</style>
