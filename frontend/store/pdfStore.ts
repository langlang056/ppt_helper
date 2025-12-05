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

  // 加载状态
  isUploading: boolean;
  isLoadingExplanation: boolean;

  // 错误状态
  error: string | null;

  // Actions
  setPdfFile: (file: File) => void;
  setPdfInfo: (pdfId: string, totalPages: number, filename: string) => void;
  setCurrentPage: (page: number) => void;
  setExplanation: (page: number, explanation: PageExplanation) => void;
  setIsUploading: (isUploading: boolean) => void;
  setIsLoadingExplanation: (isLoading: boolean) => void;
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
  isLoadingExplanation: false,
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

  setIsLoadingExplanation: (isLoading) =>
    set({ isLoadingExplanation: isLoading }),

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
      isLoadingExplanation: false,
      error: null,
    }),
}));
