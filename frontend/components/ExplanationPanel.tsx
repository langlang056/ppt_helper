'use client';

import { useEffect } from 'react';
import { usePdfStore } from '@/store/pdfStore';
import { getExplanation } from '@/lib/api';

export default function ExplanationPanel() {
  const {
    pdfId,
    currentPage,
    explanations,
    isLoadingExplanation,
    setExplanation,
    setIsLoadingExplanation,
    setError,
  } = usePdfStore();

  // 当页面切换时,加载解释
  useEffect(() => {
    if (!pdfId) return;

    // 检查缓存
    if (explanations.has(currentPage)) {
      return;
    }

    // 加载解释
    const loadExplanation = async () => {
      setIsLoadingExplanation(true);
      setError(null);

      try {
        const explanation = await getExplanation(pdfId, currentPage);
        setExplanation(currentPage, explanation);
      } catch (error: any) {
        console.error('加载解释失败:', error);
        setError(error.response?.data?.detail || '加载解释失败');
      } finally {
        setIsLoadingExplanation(false);
      }
    };

    loadExplanation();
  }, [pdfId, currentPage]);

  const currentExplanation = explanations.get(currentPage);

  if (!pdfId) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-400 text-center px-4">
          上传 PDF 后,这里将显示 AI 生成的解释
        </p>
      </div>
    );
  }

  if (isLoadingExplanation) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-black border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-500">正在生成解释...</p>
        </div>
      </div>
    );
  }

  if (!currentExplanation) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-400">暂无解释</p>
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto p-6">
      {/* 页面类型 */}
      <div className="mb-4">
        <span className="px-2 py-1 text-xs border border-black">
          {currentExplanation.page_type}
        </span>
      </div>

      {/* 摘要 */}
      <div className="mb-6">
        <h3 className="text-lg font-bold mb-2">📝 摘要</h3>
        <p className="text-gray-700 leading-relaxed">
          {currentExplanation.content.summary}
        </p>
      </div>

      {/* 关键点 */}
      {currentExplanation.content.key_points.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-bold mb-3">🔑 关键概念</h3>
          <div className="space-y-3">
            {currentExplanation.content.key_points.map((point, index) => (
              <div
                key={index}
                className={`p-3 border ${
                  point.is_important ? 'border-black bg-gray-50' : 'border-gray-300'
                }`}
              >
                <h4 className="font-semibold mb-1">{point.concept}</h4>
                <p className="text-sm text-gray-700">{point.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 类比 */}
      {currentExplanation.content.analogy && (
        <div className="mb-6">
          <h3 className="text-lg font-bold mb-2">💡 类比说明</h3>
          <div className="p-3 bg-gray-50 border border-gray-300">
            <p className="text-gray-700 italic">
              {currentExplanation.content.analogy}
            </p>
          </div>
        </div>
      )}

      {/* 示例 */}
      {currentExplanation.content.example && (
        <div className="mb-6">
          <h3 className="text-lg font-bold mb-2">📚 示例</h3>
          <div className="p-3 border border-gray-300">
            <p className="text-gray-700">{currentExplanation.content.example}</p>
          </div>
        </div>
      )}

      {/* 元信息 */}
      <div className="mt-8 pt-4 border-t border-border text-xs text-gray-400">
        <p>页面 {currentExplanation.page_number}</p>
        <p>原始语言: {currentExplanation.original_language}</p>
      </div>
    </div>
  );
}
