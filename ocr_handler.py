# -*- coding: utf-8 -*-
"""
OCR识别模块 - 支持Word和PDF文档识别
"""

import os
import tempfile
from typing import Optional, Dict, List

PYMUPDF_AVAILABLE = False
PYTHON_DOCX_AVAILABLE = False

try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    pass

try:
    from docx import Document as DocxDocument
    PYTHON_DOCX_AVAILABLE = True
except ImportError:
    pass

uploaded_documents = []

def extract_text_from_pdf(file_path: str) -> str:
    if not PYMUPDF_AVAILABLE:
        return "错误：请安装 pymupdf (pip install pymupdf)"
    
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        return f"PDF解析错误: {e}"

def extract_text_from_docx(file_path: str) -> str:
    if not PYTHON_DOCX_AVAILABLE:
        return "错误：请安装 python-docx (pip install python-docx)"
    
    try:
        doc = DocxDocument(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Word解析错误: {e}"

def extract_text_from_md(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        return f"Markdown解析错误: {e}"

def extract_text_from_file(file_path: str) -> Dict:
    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)
    
    result = {
        "filename": filename,
        "success": False,
        "text": "",
        "error": None
    }
    
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        if text.startswith("错误") or text.startswith("PDF解析错误"):
            result["error"] = text
        else:
            result["success"] = True
            result["text"] = text
    elif ext in [".docx", ".doc"]:
        text = extract_text_from_docx(file_path)
        if text.startswith("错误") or text.startswith("Word解析错误"):
            result["error"] = text
        else:
            result["success"] = True
            result["text"] = text
    elif ext == ".md":
        text = extract_text_from_md(file_path)
        if text.startswith("Markdown解析错误"):
            result["error"] = text
        else:
            result["success"] = True
            result["text"] = text
    else:
        result["error"] = f"不支持的文件格式: {ext}"
    
    if result["success"]:
        uploaded_documents.append({
            "filename": filename,
            "text_preview": result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"],
            "text_length": len(result["text"]),
            "text": result["text"]
        })
    
    return result

def get_uploaded_documents() -> List[Dict]:
    return list(uploaded_documents)

def remove_document(index: int) -> bool:
    global uploaded_documents
    if 0 <= index < len(uploaded_documents):
        uploaded_documents.pop(index)
        return True
    return False

def clear_uploaded_documents():
    global uploaded_documents
    uploaded_documents = []
    print("已清除上传文档记录")

def process_upload_file(file_storage) -> Dict:
    try:
        filename = file_storage.filename
        ext = os.path.splitext(filename)[1].lower()
        
        if ext not in [".pdf", ".docx", ".doc", ".md"]:
            return {"success": False, "error": f"不支持的格式: {ext}"}
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        file_storage.save(temp_file.name)
        temp_file.close()
        
        result = extract_text_from_file(temp_file.name)
        
        try:
            os.remove(temp_file.name)
        except:
            pass
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
