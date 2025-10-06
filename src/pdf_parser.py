"""PDF to Markdown parser module."""

import requests
from docling.document_converter import DocumentConverter
from pathlib import Path
from typing import Union, Optional


class PDFParser:
    """Parser class to convert PDF documents to Markdown format."""

    def __init__(self):
        """Initialize the PDF parser with a document converter."""
        self.converter = DocumentConverter()

    def parse_to_markdown(self, source: Union[str, Path], output_path: Optional[Path] = None) -> str:
        """
        Parse a PDF document and convert it to Markdown format.

        Args:
            source (Union[str, Path]): The source of the PDF document.
                Can be a URL or a local file path.
            output_path (Optional[Path]): If provided, saves the markdown content
                to this file path. If None, only returns the content.

        Returns:
            str: The document content in Markdown format.

        Raises:
            ValueError: If the source is invalid or the document can't be parsed.
            OSError: If there's an error saving the output file.
        """
        try:
            doc = self.converter.convert(source).document
            markdown_content = doc.export_to_markdown()
            
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(markdown_content, encoding='utf-8')
            
            return markdown_content
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")
