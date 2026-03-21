# -*- coding: utf-8 -*-
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("正在启动服务...")
try:
    from web_app import run_web_app
    print("模块加载成功")
    run_web_app(port=8001)
except Exception as e:
    print(f"启动错误: {e}")
    import traceback
    traceback.print_exc()
