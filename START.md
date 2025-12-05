# 🚀 快速启动指南

## 一键启动完整应用

### 1️⃣ 启动后端 (终端 1)

```bash
cd backend
python -m uvicorn app.main:app --reload
```

等待看到:
```
✅ Database initialized
✅ Upload directory: uploads
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2️⃣ 启动前端 (终端 2)

```bash
cd frontend
npm run dev
```

等待看到:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
```

### 3️⃣ 打开浏览器

访问: `http://localhost:3000`

---

## 🎯 使用流程

1. **上传 PDF**: 点击"选择 PDF 文件"
2. **等待解析**: 后端会解析 PDF 并提取文本
3. **查看解释**: 自动显示第一页的 AI 解释
4. **翻页浏览**: 使用"上一页"/"下一页"按钮

---

## ⚙️ 环境检查

### 后端检查

```bash
# 检查 Python 版本 (需要 3.11+)
python --version

# 检查虚拟环境
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 检查依赖
pip list | grep fastapi
```

### 前端检查

```bash
# 检查 Node.js 版本 (需要 18+)
node --version

# 检查依赖
cd frontend
npm list react next
```

### API Keys 检查

确保 `backend/.env` 包含:
```env
LLAMA_CLOUD_API_KEY=llx-...
GEMINI_API_KEY=AIzaSy-...  # 或 ANTHROPIC_API_KEY
LLM_PROVIDER=gemini
```

---

## 🐛 常见问题

### 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'fastapi'`

**解决**:
```bash
cd backend
pip install -r requirements.txt
```

---

**问题**: `ValidationError: LLAMA_CLOUD_API_KEY`

**解决**: 检查 `.env` 文件是否存在且包含有效 API Key

---

### 前端启动失败

**问题**: `Module not found: Can't resolve 'react'`

**解决**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

**问题**: PDF 无法显示

**解决**: 清除浏览器缓存或使用无痕模式

---

### API 连接失败

**问题**: 前端显示"上传失败,请检查网络连接和后端服务"

**解决**:
1. 确认后端运行在 `http://localhost:8000`
2. 访问 `http://localhost:8000/docs` 检查 API 文档
3. 检查 `frontend/.env.local` 中的 API 地址

---

## 📊 测试流程

### 1. 测试后端 API

```bash
# 方法 1: 访问 API 文档
浏览器打开: http://localhost:8000/docs

# 方法 2: 使用 curl
curl http://localhost:8000/

# 应该返回:
{
  "message": "UniTutor AI Backend is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 2. 测试前端页面

```bash
# 访问前端
浏览器打开: http://localhost:3000

# 检查控制台是否有错误
按 F12 打开开发者工具
```

### 3. 端到端测试

1. 准备一个测试 PDF (< 50MB)
2. 在前端上传 PDF
3. 查看浏览器控制台输出
4. 确认解释面板显示内容

---

## 🎉 成功标志

**后端**:
- ✅ 终端显示 `Uvicorn running on http://0.0.0.0:8000`
- ✅ 访问 `http://localhost:8000` 返回 JSON
- ✅ 访问 `http://localhost:8000/docs` 显示 API 文档

**前端**:
- ✅ 终端显示 `Local: http://localhost:3000`
- ✅ 浏览器显示 "UniTutor AI" 页面
- ✅ 能够点击上传按钮

**整体**:
- ✅ 上传 PDF 成功
- ✅ PDF 显示在左侧
- ✅ 解释显示在右侧
- ✅ 翻页功能正常

---

需要帮助? 查看完整文档: [README.md](README.md)
