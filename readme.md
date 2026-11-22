#  AI 智能邮件任务助手 (AI Smart Email Task Assistant)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Vue3](https://img.shields.io/badge/Vue-3.0-4FC08D)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-purple)

本项目是一个基于大语言模型（DeepSeek）的**智能邮件待办提取与任务管理系统**。系统通过标准 IMAP 协议安全接入用户邮箱，自动增量拉取未读邮件，并利用大模型的强大语义理解能力，从长篇大论中精准提取出“待办任务”、“截止时间”等关键信息，无缝转化为用户的备忘录任务。

##  核心特性

-  **真实邮件接入**：基于 IMAP 协议安全拉取 QQ 邮箱，支持基于时间戳的增量同步，不漏邮件且不重复抓取。
-  **AI 特化提取引擎**：深度集成 DeepSeek 大模型，智能过滤广告与寒暄，精准提取任务实体并输出标准 JSON。
-  **人在回路 (Human-in-the-loop)**：AI 提取的任务以“候选”状态进入收件箱，用户可一键确认、人工改写或直接忽略，保证数据准确性。
-  **完整的任务生命周期**：支持任务从“候选” -> “进行中” -> “已完成”的全流程状态机流转。
-  **极简高颜值的现代化前端**：基于 Vue3 + Tailwind CSS 构建，开箱即用，实时与后端接口交互。
-  **一键启动体验**：提供 `start.bat` 脚本，无需复杂配置，双击即可同时启动前后端。

##  技术栈

- **后端**：Python 3.10+, FastAPI, SQLAlchemy, SQLite, APScheduler (定时任务)
- **AI 引擎**：DeepSeek API (兼容 OpenAI SDK)
- **前端**：Vue 3 (CDN), Tailwind CSS, 原生 Fetch API
- **协议**：IMAP (邮件拉取), RESTful API (前后端通信)

##  项目结构

```text
ai-task-memory/
├── backend/                # 后端代码
│   ├── app/
│   │   ├── ai_engine/      # AI 引擎模块 (Prompt构建, DeepSeek调用, JSON解析)
│   │   ├── api/            # API 路由 (任务管理, 配置管理)
│   │   ├── core/           # 核心配置 (数据库连接, 环境变量)
│   │   ├── jobs/           # 定时任务 (IMAP 邮件拉取)
│   │   ├── models/         # SQLAlchemy 数据库模型
│   │   ├── schemas/        # Pydantic 数据校验模型
│   │   ├── services/       # 核心业务逻辑
│   │   └── main.py         # FastAPI 启动入口
│   ├── init_db.py          # 数据库初始化脚本
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── css/                # 样式文件
│   ├── js/                 # Vue 逻辑与 API 请求封装
│   └── index.html          # 前端主页面
├── .gitignore              # Git 忽略配置
├── start.bat               # Windows 一键启动脚本
└── README.md               # 项目说明文档
```

## 🚀 快速开始 (Quick Start)

### 1. 环境准备

确保你的电脑上安装了 Python 3.10 或更高版本。

### 2. 安装依赖

进入 `backend` 目录，安装所需的 Python 包：

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

在 backend 目录下新建一个 .env 文件，填入你的配置信息：

env
#### DeepSeek API 密钥 (必填)
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥

#### QQ 邮箱账号与 IMAP 授权码 (必填)
#### 注意：请前往 QQ 邮箱网页端 -> 设置 -> 账号 -> 开启 IMAP 服务，并生成 16 位授权码
QQ_EMAIL_ACCOUNT=你的QQ号@qq.com
QQ_EMAIL_AUTH_CODE=你的16位授权码

### 4. 初始化数据库
在 backend 目录下运行初始化脚本（这会在本地生成 ai_memo.db SQLite 数据库）：
```
bash
python init_db.py
```

### 5. 一键启动
回到项目根目录，双击运行 start.bat。

脚本会自动打开一个终端启动 FastAPI 后端服务。

脚本会自动在你的默认浏览器中打开 frontend/index.html 前端页面。

### 6. 开始使用
给自己的 QQ 邮箱发一封带有任务描述的测试邮件（如：“明天下午3点交报告”）。

等待最多 60 秒（后端定时任务扫描）。

在前端页面点击“刷新”，即可看到 AI 自动提取出的任务卡片。

### 开发踩坑记录与安全设计
敏感信息隔离：系统严格使用 .env 文件和 .gitignore 保护 API Key 和邮箱授权码，避免泄露。在开发过程中，成功通过 GitHub 的 Push Protection 拦截机制，避免了密钥被误提交至公开仓库。

中文编码问题：在 IMAP 拉取邮件时，原生的 imaplib 处理中文经常报错。系统最终改用 imapclient + mail-parser 库，完美解决了 MIME 解码和中文乱码问题。

异步定时任务：使用 APScheduler 与 FastAPI 的 lifespan 生命周期管理结合，确保后台邮件拉取任务随服务启停，避免资源泄露。

增量同步机制：摒弃了单纯依赖“未读状态”的方式，采用“读取本地最新邮件时间戳 -> 向服务器请求该时间后的所有邮件”的增量方案，保证了数据绝对不丢失。

### 隐私声明
本项目为个人期末大作业演示。所有邮件解析、大模型调用均在本地发起的请求，邮件内容仅短暂经过内存与大模型 API 进行分析，并仅保存在用户本地的 SQLite 数据库中，绝不上传至任何第三方服务器。