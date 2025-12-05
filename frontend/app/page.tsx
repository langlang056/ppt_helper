'use client';

import { usePdfStore } from '@/store/pdfStore';
import PdfUploader from '@/components/PdfUploader';
import PdfViewer from '@/components/PdfViewer';
import ExplanationPanel from '@/components/ExplanationPanel';

export default function Home() {
  const { error, filename } = usePdfStore();

  return (
    <div className="flex flex-col h-screen">
      {/* 顶部导航栏 */}
      <header className="border-b border-border bg-white">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold">UniTutor AI</h1>
            {filename && (
              <span className="text-sm text-gray-500">· {filename}</span>
            )}
          </div>
          <PdfUploader />
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="px-6 py-3 bg-red-50 border-t border-red-200">
            <p className="text-sm text-red-600">❌ {error}</p>
          </div>
        )}
      </header>

      {/* 主内容区 - 左右分屏 */}
      <main className="flex-1 flex overflow-hidden">
        {/* 左侧: PDF 查看器 */}
        <div className="flex-1 border-r border-border bg-white">
          <PdfViewer />
        </div>

        {/* 右侧: 解释面板 */}
        <div className="w-[500px] bg-white">
          <ExplanationPanel />
        </div>
      </main>

      {/* 底部状态栏 */}
      <footer className="border-t border-border bg-white px-6 py-2">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>智能课件讲解助手</span>
          <span>后端: http://localhost:8000</span>
        </div>
      </footer>
    </div>
  );
}
