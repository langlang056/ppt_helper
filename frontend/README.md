# UniTutor AI - 前端

简洁的黑白风格前端,用于测试 PDF 解析和 AI 解释功能。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
# 或
yarn install
# 或
pnpm install
```

### 2. 配置环境变量

确保 `.env.local` 文件存在:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 `http://localhost:3000`

## 📋 使用说明

1. **启动后端**: 确保后端服务运行在 `http://localhost:8000`
2. **上传 PDF**: 点击"选择 PDF 文件"按钮
3. **查看解释**: PDF 加载后,自动显示第一页的 AI 解释
4. **翻页**: 使用"上一页"/"下一页"按钮浏览

## 🎨 界面特点

- **黑白简洁**: 纯黑白配色,专注功能
- **左右分屏**: 左侧 PDF,右侧解释
- **响应式**: 自适应窗口大小
- **无干扰**: 最小化设计,突出内容

## 📂 项目结构

```
frontend/
├── app/
│   ├── layout.tsx          # 根布局
│   ├── page.tsx            # 主页面
│   └── globals.css         # 全局样式
├── components/
│   ├── PdfUploader.tsx     # PDF 上传组件
│   ├── PdfViewer.tsx       # PDF 查看器
│   └── ExplanationPanel.tsx # 解释面板
├── lib/
│   └── api.ts              # API 调用
├── store/
│   └── pdfStore.ts         # Zustand 状态管理
└── package.json
```

## 🔧 技术栈

- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **PDF 渲染**: react-pdf
- **状态管理**: Zustand
- **HTTP 客户端**: Axios

## 🐛 故障排除

**PDF 无法显示**: 检查 PDF.js worker 是否加载成功

**无法连接后端**: 确认后端服务运行且地址正确

**上传失败**: 检查文件是否为 PDF 格式且小于 50MB

更多信息请查看 [项目主 README](../README.md)
