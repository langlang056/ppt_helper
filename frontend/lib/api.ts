import axios from 'axios';
import { PageExplanation } from '@/store/pdfStore';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface UploadResponse {
  pdf_id: string;
  total_pages: number;
  filename: string;
  message?: string;
}

export interface PdfInfo {
  pdf_id: string;
  filename: string;
  total_pages: number;
  uploaded_at: string;
}

/**
 * 上传 PDF 文件
 */
export async function uploadPdf(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

/**
 * 获取页面解释
 */
export async function getExplanation(
  pdfId: string,
  pageNumber: number
): Promise<PageExplanation> {
  const response = await api.get<PageExplanation>(
    `/api/explain/${pdfId}/${pageNumber}`
  );

  return response.data;
}

/**
 * 获取 PDF 信息
 */
export async function getPdfInfo(pdfId: string): Promise<PdfInfo> {
  const response = await api.get<PdfInfo>(`/api/pdf/${pdfId}/info`);
  return response.data;
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await api.get('/');
    return response.status === 200;
  } catch {
    return false;
  }
}
