"""PDF解析服务 - 使用 PyMuPDF 将页面转为图像"""
import hashlib
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict
from PIL import Image
import io
import base64


class PDFParserService:
    """PDF解析服务 - 使用 PyMuPDF 将页面渲染为图像"""

    def __init__(self, dpi: int = 150):
        """
        初始化 PDF 解析器

        Args:
            dpi: 图像分辨率，默认150（平衡质量和大小）
        """
        self.dpi = dpi
        print(f"✅ PDF解析器已初始化 (使用 PyMuPDF, DPI={dpi})")

    async def extract_page_as_image(self, file_path: str, page_number: int) -> Image.Image:
        """
        提取指定页面为PIL图像

        Args:
            file_path: PDF文件路径
            page_number: 页码(从1开始)

        Returns:
            PIL Image对象
        """
        doc = fitz.open(file_path)

        try:
            if page_number < 1 or page_number > len(doc):
                raise ValueError(f"页码 {page_number} 超出范围 (1-{len(doc)})")

            # 获取页面(PyMuPDF使用0-based索引)
            page = doc[page_number - 1]

            # 计算缩放比例
            zoom = self.dpi / 72  # 72 DPI是默认值
            mat = fitz.Matrix(zoom, zoom)

            # 渲染页面为图像
            pix = page.get_pixmap(matrix=mat, alpha=False)

            # 转换为PIL Image
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))

            return image
        finally:
            doc.close()

    async def parse_single_page(self, file_path: str, page_number: int) -> Image.Image:
        """
        提取特定页面的图像（用于传给Gemini Vision）

        Args:
            file_path: PDF 路径
            page_number: 页码 (1-indexed)

        Returns:
            PIL Image对象
        """
        return await self.extract_page_as_image(file_path, page_number)

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
        doc = fitz.open(file_path)
        count = len(doc)
        doc.close()
        return count


# 单例实例
pdf_parser = PDFParserService()
