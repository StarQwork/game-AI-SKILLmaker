# -*- coding: utf-8 -*-
"""
创星游戏策划AI助理 - 主入口

用法:
    python main.py              # Web模式 (端口8001)
    python main.py --cli        # 命令行模式
    python main.py --mcp        # MCP服务模式
    python main.py --port 9000  # 指定端口
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.cleanup import register_cleanup


def run_cli():
    """命令行模式"""
    from app.core import generate_game_plan, init_rag
    
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
    """打印用法"""
    print("用法：")
    print("  python main.py              Web模式 (端口8001)")
    print("  python main.py --cli        命令行模式")
    print("  python main.py --mcp        MCP服务模式")
    print("  python main.py --port 9000  指定端口")


def main():
    """主函数"""
    register_cleanup()
    
    args = sys.argv[1:]
    
    if not args:
        from app.api import run_web_app
        run_web_app(port=8001)
    elif args[0] == "--cli":
        run_cli()
    elif args[0] == "--mcp":
        from app.services.mcp_service import run_mcp_server
        run_mcp_server()
    elif args[0] == "--port":
        from app.api import run_web_app
        port = 8001
        if len(args) > 1:
            try:
                port = int(args[1])
            except:
                pass
        run_web_app(port=port)
    elif args[0] in ["--help", "-h"]:
        print_usage()
    else:
        print(f"未知参数: {args[0]}")
        print_usage()


if __name__ == "__main__":
    main()
