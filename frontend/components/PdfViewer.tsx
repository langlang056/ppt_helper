'use client';

// Polyfill must be imported first
import '@/lib/polyfills';

import { useState, useEffect, useRef } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import { usePdfStore } from '@/store/pdfStore';

// 配置 PDF.js worker
if (typeof window !== 'undefined') {
  pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
}

export default function PdfViewer() {
  const { pdfFile, currentPage, totalPages, setCurrentPage } = usePdfStore();
  const [numPages, setNumPages] = useState<number>(0);
  const [pageWidth, setPageWidth] = useState<number | undefined>(undefined);
  const [pageHeight, setPageHeight] = useState<number | undefined>(undefined);
  const [inputPage, setInputPage] = useState<string>(String(currentPage));
  const inputRef = useRef<HTMLInputElement>(null);

  // 同步 inputPage 与 currentPage
  useEffect(() => {
    setInputPage(String(currentPage));
  }, [currentPage]);

  useEffect(() => {
    const updateSize = () => {
      const container = document.getElementById('pdf-container');
      if (container) {
        const containerWidth = container.clientWidth;
        const containerHeight = container.clientHeight;

        // PPT 通常是 16:9 或 4:3 的宽高比，我们按容器大小自适应
        // 计算基于宽度和高度的缩放，选择能完整显示的那个
        const pptAspectRatio = 16 / 9; // 假设 PPT 是 16:9

        const widthBasedHeight = containerWidth / pptAspectRatio;
        const heightBasedWidth = containerHeight * pptAspectRatio;

        // 留一些边距 (padding)
        const padding = 16;
        const availableWidth = containerWidth - padding * 2;
        const availableHeight = containerHeight - padding * 2;

        if (widthBasedHeight <= availableHeight) {
          // 宽度受限，使用宽度来缩放
          setPageWidth(availableWidth);
          setPageHeight(undefined);
        } else {
          // 高度受限，使用高度来缩放
          setPageHeight(availableHeight);
          setPageWidth(undefined);
        }
      }
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  const goToPrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  // 页码跳转
  const handlePageInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputPage(e.target.value);
  };

  const handlePageInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      goToPage();
    }
  };

  const goToPage = () => {
    const pageNum = parseInt(inputPage, 10);
    if (!isNaN(pageNum) && pageNum >= 1 && pageNum <= totalPages) {
      setCurrentPage(pageNum);
      inputRef.current?.blur();
    } else {
      // 恢复为当前页码
      setInputPage(String(currentPage));
    }
  };

  if (!pdfFile) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-400">请先上传 PDF 文件</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full w-full">
      {/* 工具栏 - 紧凑版 */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white flex-shrink-0">
        <div className="flex items-center gap-2">
          <button
            onClick={goToPrevPage}
            disabled={currentPage <= 1}
            className="px-3 py-1.5 text-sm border border-gray-300 disabled:border-gray-200 disabled:text-gray-400 hover:bg-gray-50 hover:border-gray-400 transition-all shadow-sm disabled:shadow-none font-medium rounded"
          >
            上一页
          </button>
          <div className="flex items-center gap-1">
            <input
              ref={inputRef}
              type="text"
              value={inputPage}
              onChange={handlePageInputChange}
              onKeyDown={handlePageInputKeyDown}
              onBlur={goToPage}
              className="w-12 px-2 py-1 text-sm text-center border border-gray-300 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-500">/ {totalPages}</span>
          </div>
          <button
            onClick={goToNextPage}
            disabled={currentPage >= totalPages}
            className="px-3 py-1.5 text-sm border border-gray-300 disabled:border-gray-200 disabled:text-gray-400 hover:bg-gray-50 hover:border-gray-400 transition-all shadow-sm disabled:shadow-none font-medium rounded"
          >
            下一页
          </button>
        </div>
      </div>

      {/* PDF 显示区域 - 最大化显示，垂直居中 */}
      <div
        id="pdf-container"
        className="flex-1 overflow-auto p-2 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center min-h-0"
      >
        <Document
          file={pdfFile}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={
            <div className="flex items-center justify-center p-8">
              <div className="animate-spin h-8 w-8 border-2 border-black border-t-transparent rounded-full"></div>
            </div>
          }
          error={
            <div className="p-8 text-center">
              <p className="text-red-600">PDF 加载失败</p>
            </div>
          }
        >
          <Page
            pageNumber={currentPage}
            width={pageWidth}
            height={pageHeight}
            renderTextLayer={false}
            renderAnnotationLayer={false}
          />
        </Document>
      </div>
    </div>
  );
}
