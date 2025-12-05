"""PDF parsing service using LlamaParse with PyPDF2 fallback."""
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from llama_parse import LlamaParse
from PyPDF2 import PdfReader
from app.config import get_settings

settings = get_settings()


class PDFParserService:
    """Handles PDF parsing with LlamaParse and PyPDF2 fallback."""

    def __init__(self):
        """Initialize LlamaParse client."""
        self.use_fallback = False
        try:
            self.parser = LlamaParse(
                api_key=settings.llama_cloud_api_key,
                result_type="markdown",  # Get structured text
                language="en",  # Default to English, will auto-detect other languages
                verbose=True,
                show_progress=True,
            )
            print("✅ LlamaParse initialized")
        except Exception as e:
            print(f"⚠️  LlamaParse initialization failed: {e}")
            print("📝 Will use PyPDF2 fallback for text extraction")
            self.use_fallback = True

    def _parse_with_pypdf2(self, file_path: str) -> Dict[str, any]:
        """Fallback method using PyPDF2 for local PDF parsing."""
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
        Parse PDF and return page-by-page content.

        Args:
            file_path: Absolute path to the PDF file

        Returns:
            {
                "pdf_id": "sha256_hash",
                "total_pages": 42,
                "pages": [
                    {
                        "page_number": 1,
                        "text": "extracted markdown text...",
                        "image_path": "temp/pdf_id_page_1.png"  # Optional
                    },
                    ...
                ]
            }
        """
        # Generate unique ID for this PDF
        pdf_id = self._generate_pdf_id(file_path)

        # Try LlamaParse first, fallback to PyPDF2
        if self.use_fallback:
            print("📝 Using PyPDF2 for text extraction")
            return self._parse_with_pypdf2(file_path)

        try:
            # Parse the PDF with LlamaParse
            documents = await self.parser.aload_data(file_path)

            # LlamaParse returns a list of Document objects
            pages = []
            for idx, doc in enumerate(documents, start=1):
                page_data = {
                    "page_number": idx,
                    "text": doc.text,  # Markdown formatted text
                    "metadata": doc.metadata,  # Contains page info
                }
                pages.append(page_data)

            return {
                "pdf_id": pdf_id,
                "total_pages": len(pages),
                "pages": pages,
            }
        except Exception as e:
            print(f"⚠️  LlamaParse failed: {e}")
            print("📝 Falling back to PyPDF2")
            self.use_fallback = True
            return self._parse_with_pypdf2(file_path)

    async def parse_single_page(self, file_path: str, page_number: int) -> str:
        """
        Extract text from a specific page.

        Args:
            file_path: Path to PDF
            page_number: 1-indexed page number

        Returns:
            Extracted text in markdown format
        """
        # For efficiency, parse whole document once and cache
        # In production, you'd check cache first
        result = await self.parse_pdf(file_path)
        pages = result["pages"]

        if page_number < 1 or page_number > len(pages):
            raise ValueError(f"Page {page_number} out of range (1-{len(pages)})")

        return pages[page_number - 1]["text"]

    def _generate_pdf_id(self, file_path: str) -> str:
        """Generate SHA256 hash of PDF content for unique identification."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]  # Use first 16 chars

    def get_page_count(self, file_path: str) -> int:
        """Quick method to get total pages without full parsing."""
        from PyPDF2 import PdfReader

        reader = PdfReader(file_path)
        return len(reader.pages)


# Singleton instance
pdf_parser = PDFParserService()
