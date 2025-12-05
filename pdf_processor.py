"""
PDF处理模块 - 负责将PDF转换为图像
"""
import os
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple
from PIL import Image
import io

class PDFProcessor:
    """PDF处理器"""
    
    def __init__(self, pdf_path: str, dpi: int = 200):
        """
        初始化PDF处理器
        
        Args:
            pdf_path: PDF文件路径
            dpi: 图像分辨率
        """
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.doc = None
        
    def __enter__(self):
        """上下文管理器入口"""
        self.doc = fitz.open(self.pdf_path)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        if self.doc:
            self.doc.close()
            
    def get_page_count(self) -> int:
        """获取PDF总页数"""
        if not self.doc:
            raise RuntimeError("PDF文档未打开")
        return len(self.doc)
    
    def extract_page_as_image(self, page_num: int) -> Image.Image:
        """
        提取指定页面为图像
        
        Args:
            page_num: 页码(从1开始)
            
        Returns:
            PIL Image对象
        """
        if not self.doc:
            raise RuntimeError("PDF文档未打开")
            
        if page_num < 1 or page_num > len(self.doc):
            raise ValueError(f"页码 {page_num} 超出范围 (1-{len(self.doc)})")
        
        # 获取页面(PyMuPDF使用0-based索引)
        page = self.doc[page_num - 1]
        
        # 计算缩放比例
        zoom = self.dpi / 72  # 72 DPI是默认值
        mat = fitz.Matrix(zoom, zoom)
        
        # 渲染页面为图像
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # 转换为PIL Image
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        return image
    
    def extract_all_pages(self, output_dir: str) -> List[Tuple[int, str]]:
        """
        提取所有页面为图像文件
        
        Args:
            output_dir: 输出目录
            
        Returns:
            List of (page_num, image_path) tuples
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        page_count = self.get_page_count()
        
        for page_num in range(1, page_count + 1):
            image = self.extract_page_as_image(page_num)
            image_filename = f"page_{page_num:04d}.png"
            image_path = output_path / image_filename
            
            # 保存图像
            image.save(image_path, 'PNG', optimize=True)
            results.append((page_num, str(image_path)))
            
        return results
    
    def extract_pages_range(self, output_dir: str, start_page: int = 1, 
                           end_page: int = None) -> List[Tuple[int, str]]:
        """
        提取指定范围的页面
        
        Args:
            output_dir: 输出目录
            start_page: 起始页码(从1开始)
            end_page: 结束页码(包含),None表示到最后一页
            
        Returns:
            List of (page_num, image_path) tuples
        """
        if end_page is None:
            end_page = self.get_page_count()
            
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for page_num in range(start_page, end_page + 1):
            image = self.extract_page_as_image(page_num)
            image_filename = f"page_{page_num:04d}.png"
            image_path = output_path / image_filename
            
            image.save(image_path, 'PNG', optimize=True)
            results.append((page_num, str(image_path)))
            
        return results
    
    def extract_text(self, page_num: int) -> str:
        """
        提取指定页面的文本内容(可选功能,用于辅助)
        
        Args:
            page_num: 页码(从1开始)
            
        Returns:
            页面文本内容
        """
        if not self.doc:
            raise RuntimeError("PDF文档未打开")
            
        page = self.doc[page_num - 1]
        return page.get_text()
