# UniTutor AI - 后端服务

FastAPI 后端服务,支持 PDF 解析和多 LLM 提供商。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env`:

```bash
cp .env.example .env
```

编辑 `.env`:

```env
# 必需
LLAMA_CLOUD_API_KEY=llx-你的-Key

# LLM 提供商 (选一个)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy-你的-Gemini-Key

# 或使用 Claude
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-你的-Claude-Key
```

### 3. 启动服务

```bash
python -m uvicorn app.main:app --reload
```

访问:
- API: `http://localhost:8000`
- 文档: `http://localhost:8000/docs`

## 📖 API 端点

### 上传 PDF
```http
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "pdf_id": "a3f2d9c8",
  "total_pages": 42,
  "filename": "lecture.pdf"
}
```

### 获取页面解释
```http
GET /api/explain/{pdf_id}/{page_number}

Response:
{
  "page_number": 1,
  "page_type": "CONTENT",
  "content": {
    "summary": "页面摘要",
    "key_points": [...],
    "analogy": "类比",
    "example": "示例"
  }
}
```

### 获取 PDF 信息
```http
GET /api/pdf/{pdf_id}/info
```

## 🔧 LLM 配置

支持两种 LLM 提供商,通过环境变量切换:

### Gemini (推荐,免费)
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=你的-Key
```

### Claude (功能强大)
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=你的-Key
```

修改 `.env` 后重启服务即可切换。

## 📂 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 应用
│   ├── config.py            # 配置管理
│   ├── models/
│   │   ├── database.py      # 数据库模型
│   │   └── schemas.py       # API 模式
│   └── services/
│       ├── pdf_parser.py    # PDF 解析
│       ├── cache_service.py # 缓存服务
│       └── llm_service.py   # LLM 统一接口
├── uploads/                 # PDF 文件存储
├── requirements.txt
└── .env
```

## 🔍 故障排除

**API Key 错误**: 检查 `.env` 文件配置

**PDF 解析失败**: 确保文件 < 50MB 且无密码

**数据库错误**: 删除 `unitutor.db` 并重启

更多信息请查看 [项目主 README](../README.md)
