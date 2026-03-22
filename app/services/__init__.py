# -*- coding: utf-8 -*-
"""
服务模块 - 外部服务集成层
"""

from .rag_service import init_rag, add_document, search_knowledge, enhance_prompt, clear_documents
from .ocr_service import (
    extract_text_from_file,
    get_uploaded_documents,
    remove_document,
    clear_uploaded_documents,
    process_upload_file
)
from .mcp_service import MCPServer, run_mcp_server

__all__ = [
    'init_rag', 'add_document', 'search_knowledge', 'enhance_prompt', 'clear_documents',
    'extract_text_from_file', 'get_uploaded_documents', 'remove_document',
    'clear_uploaded_documents', 'process_upload_file',
    'MCPServer', 'run_mcp_server'
]
