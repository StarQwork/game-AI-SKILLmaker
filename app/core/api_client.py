# -*- coding: utf-8 -*-
"""
API客户端模块 - 处理与AI模型的HTTP通信
"""

import requests
import time
from typing import Optional

from .config import DEFAULT_MODEL_ID, DEFAULT_BASE_URL


def call_api(
    question: str,
    api_key: str,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: str = DEFAULT_BASE_URL,
    max_retries: int = 3
) -> str:
    """
    调用AI模型API
    
    Args:
        question: 问题内容
        api_key: API密钥
        model_id: 模型ID
        base_url: API地址
        max_retries: 最大重试次数
    
    Returns:
        API响应内容或错误信息
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(base_url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return "API错误：请求过于频繁，请稍后再试"
            
            if response.status_code >= 500:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return f"API错误：{response.status_code}"
            
            return f"API错误：{response.status_code}"
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                continue
            return "请求错误：连接超时，请检查网络"
            
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return "请求错误：网络连接失败"
            
        except Exception as e:
            return f"请求错误：{e}"
    
    return "请求错误：已达到最大重试次数"


def resolve_model(model_preset: str, model_id: str, base_url: str) -> tuple:
    """
    解析模型配置
    
    Args:
        model_preset: 预设模型名称
        model_id: 自定义模型ID
        base_url: 自定义API地址
    
    Returns:
        (model_id, base_url) 元组
    """
    from .config import MODEL_PRESETS
    
    if model_preset in MODEL_PRESETS and model_preset != 'custom':
        preset = MODEL_PRESETS[model_preset]
        return model_id or preset['model_id'], base_url or preset['base_url']
    
    return model_id or DEFAULT_MODEL_ID, base_url or DEFAULT_BASE_URL
