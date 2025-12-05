import { create } from 'zustand';

export interface PageExplanation {
  page_number: number;
  page_type: string;
  content: {
    summary: string;
    key_points: Array<{
      concept: string;
      explanation: string;
      is_important: boolean;
    }>;
    analogy: string;
    example: string;
  };
  original_language: string;
}

interface PdfState {
  // PDF 信息
  pdfId: string | null;
  pdfFile: File | null;
  totalPages: number;
  filename: string;

  // 当前页面
  currentPage: number;

  // 解释缓存
  explanations: Map<number, PageExplanation>;

  // 加载状态（按页面跟踪）
  isUploading: boolean;
  loadingPages: Set<number>;

  // 错误状态（按页面跟踪）
  pageErrors: Map<number, string>;
  error: string | null;

  // Actions
  setPdfFile: (file: File) => void;
  setPdfInfo: (pdfId: string, totalPages: number, filename: string) => void;
  setCurrentPage: (page: number) => void;
  setExplanation: (page: number, explanation: PageExplanation) => void;
  setIsUploading: (isUploading: boolean) => void;
  setPageLoading: (page: number, isLoading: boolean) => void;
  setPageError: (page: number, error: string | null) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const usePdfStore = create<PdfState>((set) => ({
  // 初始状态
  pdfId: null,
  pdfFile: null,
  totalPages: 0,
  filename: '',
  currentPage: 1,
  explanations: new Map(),
  isUploading: false,
  loadingPages: new Set(),
  pageErrors: new Map(),
  error: null,

  // Actions
  setPdfFile: (file) => set({ pdfFile: file }),

  setPdfInfo: (pdfId, totalPages, filename) =>
    set({ pdfId, totalPages, filename, currentPage: 1 }),

  setCurrentPage: (page) => set({ currentPage: page }),

  setExplanation: (page, explanation) =>
    set((state) => {
      const newExplanations = new Map(state.explanations);
      newExplanations.set(page, explanation);
      return { explanations: newExplanations };
    }),

  setIsUploading: (isUploading) => set({ isUploading }),

  setPageLoading: (page, isLoading) =>
    set((state) => {
      const newLoadingPages = new Set(state.loadingPages);
      if (isLoading) {
        newLoadingPages.add(page);
      } else {
        newLoadingPages.delete(page);
      }
      return { loadingPages: newLoadingPages };
    }),

  setPageError: (page, error) =>
    set((state) => {
      const newPageErrors = new Map(state.pageErrors);
      if (error) {
        newPageErrors.set(page, error);
      } else {
        newPageErrors.delete(page);
      }
      return { pageErrors: newPageErrors };
    }),

  setError: (error) => set({ error }),

  reset: () =>
    set({
      pdfId: null,
      pdfFile: null,
      totalPages: 0,
      filename: '',
      currentPage: 1,
      explanations: new Map(),
      isUploading: false,
      loadingPages: new Set(),
      pageErrors: new Map(),
      error: null,
    }),
}));
