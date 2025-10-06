from fastapi import FastAPI, HTTPException, UploadFile, File

from pydantic import BaseModel
from src.pdf_parser import PDFParser
from pathlib import Path
from typing import Optional
import uvicorn
from fastapi import Form
from fastapi import UploadFile, File
from tempfile import NamedTemporaryFile
import shutil

app = FastAPI(title="PDF to Markdown Converter API")

class ConversionResponse(BaseModel):
    markdown_content: str
    output_path: Optional[str] = None

@app.post("/convert", response_model=ConversionResponse)
async def convert_pdf_to_markdown(
    pdf_file: Optional[UploadFile] = File(None),
    pdf_url: Optional[str] = Form(None),
    output_file: Optional[str] = Form(None)
):
    """
    Convert a PDF document to Markdown format from either an uploaded file or a URL.
    Args:
        pdf_file: Uploaded PDF file (optional)
        pdf_url: URL to PDF file (optional)
        output_file: Optional output file name
    Returns:
        ConversionResponse containing the markdown content and output file path if saved
    """
    pdf_parser = PDFParser()
    output_path = Path("data") / output_file if output_file else None
    if pdf_file:
        try:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(pdf_file.file, tmp)
                tmp_path = tmp.name
            markdown_content = pdf_parser.parse_to_markdown(tmp_path, output_path)
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass
    elif pdf_url:
        markdown_content = pdf_parser.parse_to_markdown(pdf_url, output_path)
    else:
        raise HTTPException(status_code=400, detail="Either pdf_file or pdf_url must be provided.")
    return ConversionResponse(
        markdown_content=markdown_content,
        output_path=str(output_path) if output_path else None
    )

def main():
    """Run the FastAPI application using uvicorn."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

