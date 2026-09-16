# 网络安全知识问答 RAG 系统（Cybersecurity RAG QA）

> 面向**网络安全法规与漏洞知识**的检索增强生成（RAG）问答系统。
> 知识库约 **22,125 条**（CVE 漏洞通告 + 安全问答对），通过「多路检索 → 融合 → 精排 → 生成」输出**有知识库依据**的回答，显著降低大模型幻觉，支持多轮对话与流式输出。

---

## 📌 项目简介

用户提出网络安全相关问题（漏洞查询、攻击防护、安全法规、合规测评、应急响应等），系统先判断问题是否属于安全领域，再通过**向量检索 + 关键词检索 + 假设文档检索**三路召回知识库内容，经 **RRF 融合**与 **Cross-Encoder 重排**精选证据，最后交由大模型生成带依据的流式回答；非安全领域的闲聊问题则直接由大模型应答。

---

## ✨ 功能特性

### 用户与认证
- 注册 / 登录（邮箱 + 密码，bcrypt 哈希存储）
- 验证码登录（邮箱验证码，Redis 60 秒有效，一次性）
- 游客登录（用于体验与权限演示）
- **JWT 认证**（python-jose，HS256，含过期时间与唯一 jti）
- **黑名单登出**：登出后将 token 的 jti 写入 Redis 黑名单，立即失效
- **角色权限**：`user / admin / guest` 三级，聊天与历史接口要求 user/admin

### 对话与历史
- 多轮对话：结合对话历史理解指代与上下文
- **滚动历史摘要**：超过 3 轮后按桶（3 条记录/桶）压缩为摘要入库，长对话不丢失早期关键信息，且**每桶只压缩一次**
- SSE 流式输出：逐字渲染，中断可感知
- 历史管理：会话列表（第一问为标题）、查看完整对话、删除会话（联动清理摘要表）、自动保存

### 检索与生成（RAG 核心）
- **三路混合检索**：
  - Dense 向量检索（Sentence-Transformer MiniLM，Chroma HNSW 索引）
  - BM25 关键词检索（jieba 中文分词 + 停用词表）
  - HyDE 假设文档检索（大模型生成"假设文档"后二次向量检索）
- **Weighted RRF 融合**：k=60，权重 Dense 1.0 / HyDE 0.7 / BM25 1.0
- **Cross-Encoder 重排**：bge-reranker 对 (问题, 文档) 逐对打分精排
- **意图识别路由**：本地小模型判断是否网络安全领域；低置信度兜底策略
- **生成约束**：提示词强约束"不使用来源字眼、不编造事实、以检索内容为准"

---

## 🏗️ 系统架构

### 分层结构

```text
前端 (Vue3)
  │  HTTP / SSE（带 JWT）
  ▼
后端 (FastAPI)
  ├─ Controller 路由层（收参数、调 Service、返回）
  ├─ Service 业务层（业务逻辑、组装 {code, msg, data}）
  ├─ DAO 数据访问层（裸 SQL，pymysql 参数化查询）
  ▼
MySQL（业务数据）   Redis（验证码/黑名单）   Chroma（知识向量）
```

### RAG 主链路

```text
用户问题
  → 意图识别（本地 qwen3：是否网络安全领域？）
  ├─ 否 → 直接大模型闲聊（带历史）→ SSE
  └─ 是 → 三路召回（向量 + BM25 + HyDE，各 Top-20）
        → Weighted RRF 融合（Top-30）
        → bge-reranker 重排精排
        → 组装 Prompt（历史摘要 + 检索证据 + 问题）
        → DeepSeek 流式生成 → SSE
```

---

## 🧰 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 · Vite · Element Plus · Axios · @microsoft/fetch-event-source · markdown-it · Pinia |
| 后端 | Python · FastAPI · Uvicorn · LangChain（LCEL 管道） · PyMySQL（裸 SQL） |
| 检索 | Chroma（HNSW） · Sentence-Transformer · rank_bm25 + jieba · HyDE · RRF · bge-reranker |
| 模型 | 本地 qwen3（意图路由） · GLM（HyDE / 历史摘要） · DeepSeek（最终生成） · MiniLM（向量化） |
| 存储 | MySQL（用户/会话/摘要） · Redis（验证码 / token 黑名单） · Chroma（22,125 条知识向量） |
| 认证 | python-jose（JWT） · passlib/bcrypt · RBAC 角色权限 |

> 模型权重与 API 密钥均通过环境变量注入，仓库不含任何模型文件与密钥。

---

## 🚀 快速开始

### 环境要求

- Python 3.10+（推荐 3.12）
- Node.js 16+（前端构建）
- MySQL 8+、Redis
- Ollama（本地意图识别模型）

### 1. 配置后端环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env，填写：
#   SECRET_KEY / MYSQL_* / REDIS_* / SMTP 邮箱授权码
#   CHAT_OPENAI_API_KEY（DeepSeek）/ GLM_API_KEY
#   EMBEDDING_MODEL_PATH / RERANKER_MODEL_PATH / DATA_ROOT
# 键名与说明以 backend/.env.example 为准
```

### 2. 初始化数据库

创建数据库后执行以下建表语句：

```sql
CREATE DATABASE IF NOT EXISTS cyber_rag DEFAULT CHARSET utf8mb4;

USE cyber_rag;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  users_id      INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
  username      VARCHAR(255) COMMENT '用户名',
  email         VARCHAR(255) COMMENT '邮箱',
  password_hash VARCHAR(255) COMMENT '密码哈希(bcrypt)',
  role_name     VARCHAR(20) DEFAULT 'user' COMMENT '角色: user/admin/guest',
  avatar        VARCHAR(500) COMMENT '头像URL',
  create_time   DATETIME COMMENT '注册时间',
  UNIQUE KEY uk_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 会话历史表（parent_id=0 为会话首问，其余挂接其下）
CREATE TABLE IF NOT EXISTS history (
  history_id  INT AUTO_INCREMENT PRIMARY KEY,
  question    TEXT COMMENT '用户问题',
  username    VARCHAR(255) COMMENT '用户名',
  parent_id   INT COMMENT '父会话id，0=会话首问',
  answer      TEXT COMMENT '回答',
  create_time DATETIME COMMENT '创建时间',
  summary     TEXT COMMENT '滚动摘要（按桶压缩）',
  KEY idx_username_parent (username, parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会话历史表';

-- 历史摘要表（滚动摘要独立存储，删除会话时联动清理）
CREATE TABLE IF NOT EXISTS history_summary (
  summary_id  INT AUTO_INCREMENT PRIMARY KEY,
  username    VARCHAR(255),
  history_id  INT COMMENT '会话锚点id',
  summary     TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='历史摘要表';
```

### 3. 准备知识库并灌库

```bash
# DATA_ROOT 指向数据目录（含 cve_all.jsonl 等语料）
cd backend
python create_data/LawDataBuild.py     # 向量化并写入 Chroma（cyber_law 集合）
```

### 4. 启动后端

```bash
cd backend
pip install -r requirements.txt        # 或使用独立 conda 环境
python main.py                          # http://localhost:8000（Swagger: /docs）
```

### 5. 启动前端

```bash
cd frontend
npm install
npm run dev                             # http://localhost:8080
```

---

## 🔌 API 概览

| 模块 | 方法与路径 | 说明 |
|---|---|---|
| 认证 | `POST /auth/login` | 密码登录，返回 JWT |
| 认证 | `POST /auth/loginByCode` | 验证码登录 |
| 认证 | `POST /auth/guestLogin` | 游客登录 |
| 认证 | `POST /auth/logout` | 登出（jti 入黑名单，需 token） |
| 用户 | `POST /users/register` | 注册 |
| 用户 | `GET /users/sendEmail` | 发送邮箱验证码 |
| 用户 | `GET /users/profile` | 查询资料 |
| 聊天 | `POST /chat/chat` | **SSE 流式对话**（带历史摘要与 RAG） |
| 历史 | `GET /history/queryHistoryMenu` | 会话列表 |
| 历史 | `GET /history/conversationLog` | 会话完整内容 |
| 历史 | `POST /history/saveConversationResult` | 保存一轮对话 |
| 历史 | `GET /history/deleteConversationResult` | 删除会话 |

> 除登录/注册/发验证码外，其余接口均需 `Authorization: Bearer <token>`；聊天与历史接口要求角色为 user/admin。

---

## 📁 目录结构

```text
backend/
  ├─ main.py                 # 入口：路由注册、CORS、启动预热（BM25 索引）
  ├─ common/                 # 公共层：MySQL/Redis 连接、JWT、密码哈希、角色权限
  ├─ auth/                   # 认证模块（登录 / 验证码登录 / 游客 / 登出）
  ├─ user/                   # 用户模块（注册 / 资料 / 发验证码）
  ├─ chat/                   # 聊天模块（SSE 对话 / 历史 / 滚动摘要）
  ├─ rag/                    # 检索：向量、BM25、HyDE、RRF、重排
  ├─ ai/                     # 模型加载（DeepSeek / GLM / Ollama / Embedding）
  ├─ create_data/            # 灌库脚本与知识库语料
  └─ .env.example            # 环境变量模板（占位符）
frontend/
  └─ src/
     ├─ main.js              # 入口：axios 拦截器（自动带 token）
     ├─ router/              # 路由（/login、/chat）
     └─ views/               # Login.vue、Chat.vue
```

---

## 🔒 安全与隐私

- **密钥零入库**：所有密钥/API Key/数据库密码均通过 `.env` 注入，仓库仅保留 `.env.example` 占位符模板；
- **本地路径零入库**：模型路径、数据目录等通过环境变量配置，仓库不包含任何本地绝对路径；
- **JWT 安全**：HS256 签名、过期时间、唯一 jti；登出即黑名单失效；
- **密码安全**：bcrypt 哈希存储，不存明文；
- **统一响应**：所有接口返回 `{code, msg, data}`，校验失败由 FastAPI 422 处理；
- **数据隔离**：向量库（Chroma）、上传文件、前端依赖均不入库，可按需重新生成/安装。

---

## 📝 说明

- 知识库语料 `cve_all.jsonl` 为公开漏洞通告整理（约 2.2 万条），`DATA_ROOT` 指向本地数据目录；
- 模型权重需自行准备（Embedding / Reranker 本地模型、Ollama 模型、API Key）；
- 本项目为学习与演示用途，生产部署请补充鉴权加固、限流、日志与合规评估。
