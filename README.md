# UniTutor AI - 智能课件讲解助手

一个基于多智能体的课件解析系统,将复杂的大学讲义转化为通俗易懂的中文解释。

## 🎯 项目简介

**问题**: 学生在理解复杂的学术幻灯片时遇到困难(特别是外语授课的内容)

**解决方案**: 上传 PDF 课件 → AI 智能体提取概念 → 生成中文解释和类比

**用户体验**: 左右分屏界面 - 左侧显示原始 PDF,右侧显示 AI 解释

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│              前端 (Next.js 14)                  │
│  ┌─────────────────┐  ┌────────────────────┐   │
│  │  PDF 查看器     │  │   解释面板         │   │
│  │  (react-pdf)    │  │  (Shadcn/UI)       │   │
│  └─────────────────┘  └────────────────────┘   │
└──────────────┬──────────────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────────────┐
│        后端 (FastAPI + LangGraph)               │
│  ┌──────────────────────────────────────────┐   │
│  │  LangGraph 智能体工作流                   │   │
│  │  导航员 → 教授 → 导师 → 格式化            │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐    │
│  │ LlamaParse│  │Claude/Gemini│ SQLite    │    │
│  │ (PDF解析)│  │  (LLM)    │  │ (缓存)    │    │
│  └──────────┘  └──────────┘  └────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 📦 技术栈

| 层级          | 技术                                  |
| ------------- | ------------------------------------- |
| **前端**      | Next.js 14, TypeScript, Tailwind CSS  |
| **PDF 查看**  | react-pdf                             |
| **后端**      | FastAPI, Python 3.11+                 |
| **智能体**    | LangChain + LangGraph                 |
| **LLM**       | Claude/Gemini (可切换)                |
| **PDF 解析**  | LlamaParse (by LlamaIndex)            |
| **数据库**    | SQLite (开发), PostgreSQL (生产)      |
| **状态管理**  | Zustand                               |

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.11+
- Node.js 18+ (前端,Phase 3)
- API Keys:
  - [LlamaCloud API Key](https://cloud.llamaindex.ai/api-key) (必需)
  - [Anthropic API Key](https://console.anthropic.com/) 或 [Gemini API Key](https://aistudio.google.com/apikey) (二选一)

### 2. 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活环境 (Windows)
venv\Scripts\activate

# 激活环境 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 到 `.env`:

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件:

```env
# 必需: LlamaCloud API Key
LLAMA_CLOUD_API_KEY=llx-你的-API-Key

# 选择一个 LLM 提供商 (推荐 Gemini,免费且快速)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy-你的-Gemini-Key

# 或使用 Anthropic Claude
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-你的-Claude-Key
```

### 4. 启动服务器

```bash
# 在 backend 目录下
python -m uvicorn app.main:app --reload
```

服务器地址: `http://localhost:8000`

API 文档: `http://localhost:8000/docs`

---

## 📖 API 使用

### 1. 上传 PDF

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@你的课件.pdf"
```

**响应**:
```json
{
  "pdf_id": "a3f2d9c8b1e4f5a6",
  "total_pages": 42,
  "filename": "你的课件.pdf",
  "message": "PDF uploaded and parsed successfully"
}
```

### 2. 获取页面解释

```bash
curl "http://localhost:8000/api/explain/{pdf_id}/1"
```

**响应** (Phase 1 - 基础版本):
```json
{
  "page_number": 1,
  "page_type": "CONTENT",
  "content": {
    "summary": "第 1 页内容摘要",
    "key_points": [
      {
        "concept": "核心概念",
        "explanation": "概念解释",
        "is_important": true
      }
    ],
    "analogy": "类比说明",
    "example": "实例"
  },
  "original_language": "mixed"
}
```

### 3. 获取 PDF 信息

```bash
curl "http://localhost:8000/api/pdf/{pdf_id}/info"
```

---

## 🔧 LLM 配置

### 使用 Google Gemini (推荐)

**优点**:
- 免费配额充足 (gemini-2.0-flash-exp 测试期免费)
- 响应速度快
- 适合高频调用

**配置**:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=你的-Gemini-Key
```

**获取 API Key**: [Google AI Studio](https://aistudio.google.com/apikey)

### 使用 Anthropic Claude

**优点**:
- 更强的推理能力
- 更好的指令遵循
- 适合复杂任务

**配置**:
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=你的-Claude-Key
```

**获取 API Key**: [Anthropic Console](https://console.anthropic.com/)

### 切换 LLM 提供商

只需修改 `.env` 文件中的 `LLM_PROVIDER`,无需修改代码:

```env
# 切换到 Gemini
LLM_PROVIDER=gemini

# 切换到 Claude
LLM_PROVIDER=anthropic
```

重启服务器后生效。

---

## 💰 成本估算

**使用场景**: 2 用户/天 × 2.5 份 PDF × 50 页 = 250 页/天

### 方案 1: Gemini (推荐)

| 服务          | 单价/页    | 每日成本 | 每月成本   |
| ------------- | ---------- | -------- | ---------- |
| LlamaParse    | $0.003     | $0.75    | $22.50     |
| Gemini Flash  | 免费(测试期) | $0      | $0         |
| **总计**      |            | **$0.75**| **$22.50** |

### 方案 2: Claude

| 服务          | 单价/页 | 每日成本 | 每月成本    |
| ------------- | ------- | -------- | ----------- |
| LlamaParse    | $0.003  | $0.75    | $22.50      |
| Claude 3.5    | ~$0.02  | $5.00    | $150.00     |
| **总计**      |         | **$5.75**| **$172.50** |

**缓存优化**: 第二次访问相同 PDF = $0 (从 SQLite 缓存读取)

---

## 📂 项目结构

```
ppt_helper/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 路由
│   │   ├── config.py            # 配置管理
│   │   ├── agents/              # (Phase 2) LangGraph 智能体
│   │   ├── models/
│   │   │   ├── database.py      # SQLAlchemy 模型
│   │   │   └── schemas.py       # API 数据模式
│   │   └── services/
│   │       ├── pdf_parser.py    # LlamaParse 封装
│   │       ├── cache_service.py # 数据库缓存
│   │       └── llm_service.py   # LLM 统一接口
│   ├── uploads/                 # PDF 存储目录
│   ├── requirements.txt         # Python 依赖
│   └── .env                     # 环境变量
│
└── frontend/                    # (Phase 3) Next.js 前端
    ├── app/
    ├── components/
    └── package.json
```

---

## 🎓 开发阶段

### ✅ Phase 1: 后端解析与基础 API (已完成)

**完成内容**:
- ✅ FastAPI 服务器与 CORS 支持
- ✅ PDF 上传与去重 (SHA256 哈希)
- ✅ LlamaParse 集成进行文本提取
- ✅ SQLite 缓存节省成本
- ✅ 基础 REST API (`/upload`, `/explain`)
- ✅ 多 LLM 支持 (Claude/Gemini 可切换)

### 🔄 Phase 2: LangGraph 多智能体工作流 (下一步)

**目标**:
1. 构建 **导航员智能体** - 分类页面类型 (标题/内容/结尾)
2. 构建 **教授智能体** - 提取学术概念(原语言)
3. 构建 **导师智能体** - 简化为中文 + 创建类比
4. 构建 **格式化智能体** - 结构化 JSON 输出

**智能体流程**:
```
输入: 页面文本 (英文/法文)
  ↓
导航员 → 这是标题页还是内容页?
  ↓
教授 → 提取: "梯度下降: ∇f(x) = ..."
  ↓
导师 → "梯度下降就像蒙眼下山,每次往最陡的方向走一小步"
  ↓
格式化 → JSON 输出
```

### ✅ Phase 3: 前端设置与 PDF 查看器 (已完成)

**完成内容**:
- ✅ Next.js 14 App Router 项目
- ✅ 简洁黑白风格设计
- ✅ 左右分屏布局 (PDF + 解释)
- ✅ react-pdf 集成
- ✅ 页面导航功能
- ✅ Zustand 状态管理
- ✅ 后端 API 连接
- ✅ 响应式设计

**使用方法**:
```bash
# 1. 启动后端
cd backend
python -m uvicorn app.main:app --reload

# 2. 启动前端 (新终端)
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000`

### 🔄 Phase 4: LangGraph 多智能体工作流 (下一步)

**目标**:
1. 构建 **导航员智能体** - 分类页面类型
2. 构建 **教授智能体** - 提取学术概念
3. 构建 **导师智能体** - 简化为中文 + 创建类比
4. 构建 **格式化智能体** - 结构化 JSON 输出

**智能体流程**:
```
输入: 页面文本 (英文/法文)
  ↓
导航员 → 这是标题页还是内容页?
  ↓
教授 → 提取: "梯度下降: ∇f(x) = ..."
  ↓
导师 → "梯度下降就像蒙眼下山,每次往最陡的方向走一小步"
  ↓
格式化 → JSON 输出
```

---

## 🔍 故障排除

### 错误: "LLAMA_CLOUD_API_KEY not found"

**解决**: 确保 `.env` 文件存在且包含有效的 API Key

### 错误: "API key not valid"

**解决**:
- 检查 API Key 是否正确复制
- 确认 API Key 未过期
- Anthropic: 确保账户有余额
- Gemini: 确认在 [AI Studio](https://aistudio.google.com/) 创建了 API Key

### 错误: "Unable to parse PDF"

**解决**:
- 检查 PDF 是否有密码保护
- 确保文件大小 < 50MB
- 验证 LlamaParse API Key 是否有效

### 数据库错误

**解决**: 删除 `unitutor.db` 并重启服务器以重新创建表

```bash
rm backend/unitutor.db
python -m uvicorn app.main:app --reload
```

### 切换 LLM 后出错

**解决**:
1. 确认新 LLM 的 API Key 已正确配置
2. 重启服务器
3. 检查 `app/config.py` 中的 `llm_provider` 设置

---

## 🎯 设计亮点

### 为什么选择 LlamaParse?
- 处理复杂的幻灯片布局 (多栏、表格、图表)
- 比 PyPDF2/pdfplumber 更适合学术材料
- 输出结构化的 Markdown

### 为什么选择 LangGraph?
- 清晰的状态机用于智能体工作流
- 比基础 LangChain 链更适合多智能体系统
- 内置检查点和调试功能

### 为什么需要缓存?
- 同一 PDF 第二次上传 = 即时响应
- 每页节省约 $0.02 的重复访问成本
- 对于 2 用户场景至关重要(可能复习相同材料)

### 为什么支持多 LLM?
- **灵活性**: 根据需求和预算选择
- **成本优化**: 开发用 Gemini,生产用 Claude
- **无缝切换**: 修改配置即可,无需改代码

---

## 📝 开发日志

### 2024-12 更新

**后端**:
- ✅ 添加 Google Gemini API 支持
- ✅ 创建统一的 LLM 服务层
- ✅ 支持 Anthropic Claude 和 Google Gemini 无缝切换
- ✅ 修复 LlamaParse 语言参数问题
- ✅ 完善中文文档

**前端**:
- ✅ Next.js 14 App Router 项目搭建
- ✅ 简洁黑白风格界面设计
- ✅ PDF 上传和查看功能
- ✅ 左右分屏布局
- ✅ AI 解释面板
- ✅ Zustand 状态管理集成
- ✅ 完整的前后端对接

---

## 🤝 贡献

这是一个个人项目,欢迎反馈!

## 📄 许可

仅供个人使用。

---

**使用 Claude Code 构建** 🤖
