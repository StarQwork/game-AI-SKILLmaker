# -*- coding: utf-8 -*-
"""
配置模块 - 全局配置常量
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = "游戏任务书"
OUTPUT_DIR_ABS = os.path.join(BASE_DIR, OUTPUT_DIR)

DEFAULT_ROLES = ["programmer", "artist", "audio", "writer"]

MODEL_PRESETS = {
    "deepseek": {
        "name": "DeepSeek",
        "model_id": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1/chat/completions"
    },
    "openai": {
        "name": "OpenAI",
        "model_id": "gpt-4o",
        "base_url": "https://api.openai.com/v1/chat/completions"
    },
    "qwen": {
        "name": "通义千问",
        "model_id": "qwen-turbo",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    },
    "zhipu": {
        "name": "智谱AI",
        "model_id": "glm-4",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    },
    "custom": {
        "name": "自定义",
        "model_id": "",
        "base_url": ""
    }
}

DEFAULT_MODEL_ID = "deepseek-chat"
DEFAULT_BASE_URL = "https://api.deepseek.com/v1/chat/completions"
