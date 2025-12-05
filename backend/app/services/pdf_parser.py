"""PDF解析服务 - 仅使用 PyPDF2 本地解析"""
import hashlib
from pathlib import Path
from typing import Dict
from PyPDF2 import PdfReader


class PDFParserService:
    """PDF解析服务 - 使用 PyPDF2 进行本地解析"""

    def __init__(self):
        """初始化 PDF 解析器"""
        print("✅ PDF解析器已初始化 (使用 PyPDF2)")

    def _parse_with_pypdf2(self, file_path: str) -> Dict[str, any]:
        """使用 PyPDF2 进行本地 PDF 解析"""
        pdf_id = self._generate_pdf_id(file_path)
        reader = PdfReader(file_path)

        pages = []
        for idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            page_data = {
                "page_number": idx,
                "text": text,
                "metadata": {"source": f"page_{idx}"},
            }
            pages.append(page_data)

        return {
            "pdf_id": pdf_id,
            "total_pages": len(pages),
            "pages": pages,
        }

    async def parse_pdf(self, file_path: str) -> Dict[str, any]:
        """
        解析 PDF 并返回逐页内容

        Args:
            file_path: PDF 文件的绝对路径

        Returns:
            {
                "pdf_id": "sha256_hash",
                "total_pages": 42,
                "pages": [
                    {
                        "page_number": 1,
                        "text": "提取的文本...",
                        "metadata": {"source": "page_1"}
                    },
                    ...
                ]
            }
        """
        return self._parse_with_pypdf2(file_path)

    async def parse_single_page(self, file_path: str, page_number: int) -> str:
        """
        提取特定页面的文本

        Args:
            file_path: PDF 路径
            page_number: 页码 (1-indexed)

        Returns:
            提取的文本
        """
        result = await self.parse_pdf(file_path)
        pages = result["pages"]

        if page_number < 1 or page_number > len(pages):
            raise ValueError(f"页码 {page_number} 超出范围 (1-{len(pages)})")

        return pages[page_number - 1]["text"]

    def _generate_pdf_id(self, file_path: str) -> str:
        """生成 PDF 内容的 SHA256 哈希作为唯一标识"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # 分块读取以处理大文件
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]  # 使用前16个字符

    def get_page_count(self, file_path: str) -> int:
        """快速获取总页数而不进行完整解析"""
        reader = PdfReader(file_path)
        return len(reader.pages)


# 单例实例
pdf_parser = PDFParserService()
