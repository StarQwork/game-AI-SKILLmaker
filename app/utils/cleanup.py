# -*- coding: utf-8 -*-
"""
清理模块 - 文件和资源清理
"""

import os
import sys
import signal
import atexit


def cleanup_handler():
    """清理函数"""
    print("\n正在清理...")
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, "游戏任务书")
        if os.path.exists(output_dir):
            import shutil
            import time
            for i in range(3):
                try:
                    shutil.rmtree(output_dir)
                    print(f"已清理: {output_dir}")
                    break
                except Exception as e:
                    if i < 2:
                        time.sleep(0.3)
    except Exception as e:
        print(f"清理出错: {e}")
    
    try:
        from app.services.ocr_service import clear_uploaded_documents
        clear_uploaded_documents()
    except:
        pass
    
    try:
        from app.services.rag_service import clear_documents
        clear_documents()
    except:
        pass
    
    print("清理完成")


def signal_handler(signum=None, frame=None):
    """信号处理器"""
    cleanup_handler()
    sys.exit(0)


def register_cleanup():
    """注册清理函数"""
    pass
