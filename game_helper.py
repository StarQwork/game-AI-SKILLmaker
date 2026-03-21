# -*- coding: utf-8 -*-
"""
游戏策划小助手 - 集成RAG/OCR/MCP
"""

import sys
import os
import signal
import atexit

def cleanup_handler():
    """清理函数"""
    print("\n正在清理...")
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
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
        from ocr_handler import clear_uploaded_documents
        clear_uploaded_documents()
    except:
        pass
    
    try:
        from rag_knowledge import clear_documents
        clear_documents()
    except:
        pass
    
    print("清理完成")

def signal_handler(signum=None, frame=None):
    cleanup_handler()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup_handler)

def run_cli():
    """命令行模式"""
    from core import generate_game_plan, OUTPUT_DIR, init_rag
    
    init_rag()
    
    print("=" * 50)
    print("游戏策划小助手")
    print("=" * 50)
    
    game_idea = input("请输入游戏想法：")
    if len(game_idea) < 3:
        print("输入太短")
        return
    
    api_key = input("请输入API Key：")
    if not api_key:
        print("需要API Key")
        return
    
    print("\n生成中...")
    result = generate_game_plan(game_idea, api_key)
    
    if result["success"]:
        print(f"\n完成！文件在 {result['output_dir']}")
        for f in result["saved_files"]:
            print(f"  - {f['role']}: {f['filename']}")
    else:
        print(f"失败：{result.get('error')}")

def print_usage():
    print("用法：")
    print("  python game_helper.py              命令行模式")
    print("  python game_helper.py --web        Web模式")
    print("  python game_helper.py --web --port 8001  指定端口")
    print("  python game_helper.py --mcp        MCP服务模式")

def main():
    args = sys.argv[1:]
    
    if not args:
        run_cli()
    elif args[0] == "--web":
        from web_app import run_web_app
        port = 5000
        if "--port" in args:
            idx = args.index("--port")
            if idx + 1 < len(args):
                port = int(args[idx + 1])
        run_web_app(port=port)
    elif args[0] == "--mcp":
        from mcp_server import run_mcp_server
        run_mcp_server()
    elif args[0] in ["--help", "-h"]:
        print_usage()
    else:
        print(f"未知参数: {args[0]}")
        print_usage()

if __name__ == "__main__":
    main()
