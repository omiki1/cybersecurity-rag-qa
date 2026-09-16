<template>
    <div class="login-container">
        <div class="login-card">
            <!-- 终端标题栏 -->
            <div class="login-term-bar">
                <div class="term-dots">
                    <span class="term-dot term-dot-r"></span>
                    <span class="term-dot term-dot-y"></span>
                    <span class="term-dot term-dot-g"></span>
                </div>
                <span class="term-label">WASTELAND.AI :: 安全接入节点</span>
            </div>

            <!-- 卡片主体 -->
            <div class="login-body">
                <div class="login-head">
                    <h1 class="login-glitch" data-text="网络安全问答系统">网络安全问答系统</h1>
                    <p class="login-sub">// 知识库接入协议</p>
                </div>

                <!-- 登录方式切换 -->
                <div class="login-tabs">
                    <button
                        type="button"
                        class="login-tab"
                        :class="{ active: loginMode === 'password' }"
                        @click="switchMode('password')"
                    >密码登录</button>
                    <button
                        type="button"
                        class="login-tab"
                        :class="{ active: loginMode === 'code' }"
                        @click="switchMode('code')"
                    >验证码登录</button>
                    <button
                        type="button"
                        class="login-tab"
                        :class="{ active: loginMode === 'register' }"
                        @click="switchMode('register')"
                    >注 册</button>
                </div>

                <!-- ===== 密码登录 ===== -->
                <el-form v-if="loginMode === 'password'" label-position="top" class="login-form">
                    <el-form-item label="邮箱">
                        <el-input
                                v-model="email"
                                placeholder="请输入邮箱地址"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Message/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="密码">
                        <el-input
                                v-model="password"
                                type="password"
                                show-password
                                placeholder="请输入密码"
                                @keyup.enter="passwordLogin"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Lock/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item class="login-actions">
                        <el-button
                                class="login-btn"
                                @click="passwordLogin"
                        >
                            登 录
                        </el-button>
                    </el-form-item>
                </el-form>

                <!-- ===== 验证码登录 ===== -->
                <el-form v-else-if="loginMode === 'code'" label-position="top" class="login-form">
                    <el-form-item label="邮箱">
                        <el-input
                                id="email"
                                v-model="email"
                                :disabled="!isCode"
                                placeholder="请输入邮箱地址"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Message/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="验证码">
                        <el-input
                                v-model="code"
                                :disabled="isCode"
                                placeholder="请输入验证码"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Key/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item class="login-actions">
                        <el-button
                                v-show="isCode"
                                class="login-btn"
                                @click="sendEmail"
                        >
                            发送验证码
                        </el-button>

                        <el-button
                                v-show="!isCode"
                                class="login-btn login-btn-verify"
                                @click="checkCode"
                        >
                            验证并接入
                        </el-button>
                    </el-form-item>
                </el-form>

                <!-- ===== 注册 ===== -->
                <el-form v-else-if="loginMode === 'register'" label-position="top" class="login-form">
                    <el-form-item label="用户名">
                        <el-input
                                v-model="regUsername"
                                placeholder="请输入用户名"
                        >
                            <template #prefix>
                                <el-icon>
                                    <User/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="邮箱">
                        <el-input
                                v-model="regEmail"
                                placeholder="请输入邮箱地址"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Message/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="密码">
                        <el-input
                                v-model="regPassword"
                                type="password"
                                show-password
                                placeholder="请输入密码（至少6位）"
                                @keyup.enter="register"
                        >
                            <template #prefix>
                                <el-icon>
                                    <Lock/>
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-form-item class="login-actions">
                        <el-button
                                class="login-btn login-btn-register"
                                @click="register"
                        >
                            注 册
                        </el-button>
                    </el-form-item>
                </el-form>

                <!-- 游客登录：无需密码，签发 guest 角色 JWT，用于测试权限拦截 -->
                <div class="guest-login">
                    <button type="button" class="login-btn login-btn-guest" @click="guestLogin">
                        游客登录
                    </button>
                </div>

                <div class="login-foot">
                    <span class="boot-line">[ WASTELAND OS v4.2.0 ] [ 信号 ▂▃▅ ]</span>
                    <span class="boot-cursor">▌</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Key, Lock, User } from '@element-plus/icons-vue'

const router = useRouter()

// 登录方式：password / code
const loginMode = ref('password')

// 控制验证码输入框是否可输入 --- true 表示当前要输入邮箱号（发送验证码阶段）
const isCode = ref(true)

// 保存邮箱号、密码、验证码
const email = ref('')
const password = ref('')
const code = ref('')

// 注册表单数据
const regUsername = ref('')
const regEmail = ref('')
const regPassword = ref('')

// 获取当前实例对象 --- 通过它可以访问到 main.js 中挂载的 $axios
const proxy = getCurrentInstance().proxy

// 切换登录方式
function switchMode(mode) {
    loginMode.value = mode
    if (mode === 'code') {
        isCode.value = true // 切到验证码模式时，先进入"发送验证码"阶段
    }
}

// 解析 JWT 的 payload
function parseJwt(token) {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const pad = base64 + '='.repeat((4 - base64.length % 4) % 4)
    const bytes = Uint8Array.from(atob(pad), c => c.charCodeAt(0))
    return JSON.parse(new TextDecoder().decode(bytes))
}

// ========== 密码登录 ==========
function passwordLogin() {
    if (!email.value || !password.value) {
        ElMessage.warning('请输入邮箱和密码')
        return
    }
    proxy.$axios({
        url: '/auth/login',
        method: 'post',
        data: JSON.stringify({
            email: email.value,
            password: password.value,
        }),
    }).then(res => {
        if (res.data.code === 200) {
            // data 是 JWT token
            const token = res.data.data
            sessionStorage.setItem('token', token)
            const payload = parseJwt(token)
            sessionStorage.setItem('username', payload.username)
            sessionStorage.setItem('email', email.value)
            sessionStorage.setItem('role', payload.role_name)
            ElMessage.success('登录成功')
            // 延迟 1 秒跳转到聊天页
            setTimeout(() => {
                router.push('/chat')
            }, 1000)
        } else {
            ElMessage.error(res.data.msg)
        }
    })
}

// ========== 游客登录（无需密码，测试 JWT 权限拦截） ==========
function guestLogin() {
    proxy.$axios({
        url: '/auth/guestLogin',
        method: 'post',
    }).then(res => {
        if (res.data.code === 200) {
            const token = res.data.data
            sessionStorage.setItem('token', token)
            const payload = parseJwt(token)
            sessionStorage.setItem('username', payload.username)   // 'guest'
            sessionStorage.setItem('email', '')
            sessionStorage.setItem('role', payload.role_name)      // 'guest'
            ElMessage.success('已进入游客模式（无问答资格）')
            setTimeout(() => {
                router.push('/chat')
            }, 600)
        } else {
            ElMessage.error(res.data.msg)
        }
    })
}

// ========== 注册 ==========
function register() {
    if (!regUsername.value || !regEmail.value || !regPassword.value) {
        ElMessage.warning('请填写完整的注册信息')
        return
    }
    if (regPassword.value.length < 6) {
        ElMessage.warning('密码至少 6 位')
        return
    }
    proxy.$axios({
        url: '/users/register',
        method: 'post',
        data: JSON.stringify({
            username: regUsername.value,
            email: regEmail.value,
            password: regPassword.value,
        }),
    }).then(res => {
        if (res.data.code === 200) {
            ElMessage.success('注册成功，请登录')
            loginMode.value = 'password'
            email.value = regEmail.value
            password.value = ''
        } else {
            ElMessage.error(res.data.msg)
        }
    })
}

// ========== 验证码登录 ==========
// 发送验证码
function sendEmail() {
    let sendEmail = email.value // 获取用户输入的邮箱号
    proxy.$axios({
        url: 'users/sendEmail', // 请求地址，自动拼接前缀 http://localhost:8000/
        method: 'get', // 请求方式
        params: { // 请求参数，key 必须和后端接口形参一致
            email: sendEmail,
        },
    }).then(res => {
        let code = res.data.code
        let msg = res.data.msg
        let data = res.data.data
        if (code === 200) {
            isCode.value = !isCode.value // 切换到输入验证码阶段
            sessionStorage.setItem('username', data.username) // 保存用户名（data 为后端返回的用户名）
            sessionStorage.setItem('email', data.email)
            ElMessage.info('成功发送验证码')
        } else {
            ElMessage.error(msg)
        }
    })
}

// 验证码登录
function checkCode() {
    let payload = {
        email: email.value,
        code: code.value,
    }
    proxy.$axios({
        url: 'auth/loginByCode',
        method: 'post',
        data: JSON.stringify(payload),
    }).then(res => {
        if (res.data.code === 200) {
            // data 是 JWT token：与密码登录同一套存储
            const token = res.data.data
            sessionStorage.setItem('token', token)
            const info = parseJwt(token)
            sessionStorage.setItem('username', info.username)
            sessionStorage.setItem('email', email.value)
            sessionStorage.setItem('role', info.role_name)
            ElMessage.success('登录成功')
            // 延迟 1 秒跳转到聊天页
            setTimeout(() => {
                router.push('/chat')
            }, 1000)
        } else {
            ElMessage.error(res.data.msg)
        }
    })
}
</script>

<style scoped>
.login-container {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.login-card {
    width: 460px;
    background: linear-gradient(180deg, #1a1d14, #13150e);
    border: 1px solid #3a4031;
    border-radius: 6px;
    position: relative;
    box-shadow:
        0 0 0 1px rgba(0, 0, 0, .6),
        0 0 24px rgba(182, 255, 0, .08),
        inset 0 0 40px rgba(0, 0, 0, .4);
}

/* 终端标题栏 */
.login-term-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: #0e100b;
    border-bottom: 1px solid #3a4031;
}

.term-dots {
    display: flex;
    gap: 6px;
}

.term-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.term-dot-r { background: #ff3355; }
.term-dot-y { background: #ffb000; }
.term-dot-g { background: #39ff14; }

.term-label {
    font-size: 12px;
    color: #8a9279;
    letter-spacing: 1px;
}

.login-body {
    padding: 30px 34px 24px;
}

.login-head {
    text-align: center;
    margin-bottom: 22px;
}

.login-glitch {
    font-size: 27px;
    color: var(--neon-green);
    text-shadow: 0 0 12px rgba(182, 255, 0, .6);
    margin: 0;
    letter-spacing: 3px;
    position: relative;
}

/* 故障文字（glitch）伪影 */
.login-glitch::before,
.login-glitch::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    opacity: .75;
}
.login-glitch::before {
    color: var(--neon-pink);
    z-index: -1;
    animation: glitch-a 3.2s infinite steps(1);
}
.login-glitch::after {
    color: var(--neon-cyan);
    z-index: -2;
    animation: glitch-b 3.2s infinite steps(1);
}

@keyframes glitch-a {
    0%, 90% { transform: translate(0); opacity: .75; }
    91% { transform: translate(-3px, 1px); }
    93% { transform: translate(2px, -1px); }
    96% { transform: translate(-1px, 0); }
    100% { transform: translate(0); }
}

@keyframes glitch-b {
    0%, 88% { transform: translate(0); opacity: .75; }
    89% { transform: translate(3px, -1px); }
    92% { transform: translate(-2px, 1px); }
    97% { transform: translate(1px, 0); }
    100% { transform: translate(0); }
}

.login-sub {
    color: #8a9279;
    font-size: 13px;
    margin-top: 8px;
    letter-spacing: 1px;
}

/* 登录方式切换 tab */
.login-tabs {
    display: flex;
    margin-bottom: 22px;
    border-bottom: 1px solid #33382a;
}

.login-tab {
    flex: 1;
    padding: 10px 0;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: #6f7660;
    font-family: var(--font-term);
    font-size: 14px;
    letter-spacing: 2px;
    cursor: pointer;
    transition: all .2s;
}

.login-tab:hover {
    color: #a3aa8f;
}

.login-tab.active {
    color: var(--neon-green);
    border-bottom-color: var(--neon-green);
    text-shadow: 0 0 8px rgba(182, 255, 0, .5);
}

.login-form :deep(.el-form-item__label) {
    color: #8a8f7d;
    font-size: 13px;
    letter-spacing: 1px;
}

.login-form :deep(.el-input__wrapper) {
    background: #10130c;
    border: 1px solid #33382a;
    border-radius: 4px;
    padding: 6px 12px;
}

.login-actions {
    margin-bottom: 0;
}

.login-btn {
    width: 100%;
    height: 42px;
    background: transparent;
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    border-radius: 4px;
    letter-spacing: 2px;
    font-size: 15px;
    transition: all .2s;
}

.login-btn:hover {
    background: rgba(182, 255, 0, .12);
    box-shadow: 0 0 16px rgba(182, 255, 0, .25);
}

.login-btn-verify {
    border-color: var(--neon-amber);
    color: var(--neon-amber);
}

/* 注册按钮：数据青变体 */
.login-btn-register {
    border-color: var(--neon-cyan);
    color: var(--neon-cyan);
}

.login-btn-register:hover {
    background: rgba(0, 240, 255, .12);
    box-shadow: 0 0 16px rgba(0, 240, 255, .25);
}

.login-btn-verify:hover {
    background: rgba(255, 176, 0, .12);
    box-shadow: 0 0 16px rgba(255, 176, 0, .25);
}

/* 游客登录按钮：中性灰 */
.guest-login {
    margin-top: 14px;
}
.login-btn-guest {
    border-color: #5a6150;
    color: #a6ad97;
    letter-spacing: 2px;
}
.login-btn-guest:hover {
    background: rgba(166, 173, 151, .12);
    box-shadow: 0 0 16px rgba(166, 173, 151, .2);
}

.login-foot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 24px;
    padding-top: 14px;
    border-top: 1px dashed #33382a;
}

.boot-line {
    font-size: 11px;
    color: #7a8371;
    letter-spacing: 1px;
}

.boot-cursor {
    color: var(--neon-green);
    animation: blink 1s steps(1) infinite;
}

@keyframes blink {
    50% { opacity: 0; }
}
</style>
