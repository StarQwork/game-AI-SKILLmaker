# -*- coding: utf-8 -*-
"""
生成器模块 - 策划案生成核心逻辑
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

from .config import OUTPUT_DIR, DEFAULT_ROLES
from .templates import ROLE_TEMPLATES
from .api_client import call_api

RAG_INITIALIZED = False


def init_rag() -> bool:
    """初始化RAG知识库"""
    global RAG_INITIALIZED
    try:
        from app.services.rag_service import init_rag as rag_init
        RAG_INITIALIZED = rag_init()
        return RAG_INITIALIZED
    except ImportError:
        return False


def generate_single(
    game_idea: str,
    role: str,
    api_key: str,
    model_id: str,
    base_url: str,
    use_rag: bool = True,
    reference_content: str = ""
) -> Dict[str, Any]:
    """
    生成单个角色的策划案
    
    Args:
        game_idea: 游戏创意描述
        role: 角色标识
        api_key: API密钥
        model_id: 模型ID
        base_url: API地址
        use_rag: 是否使用RAG增强
        reference_content: 参考内容
    
    Returns:
        生成结果字典
    """
    if role not in ROLE_TEMPLATES:
        return {"success": False, "error": f"未知角色: {role}"}
    
    info = ROLE_TEMPLATES[role]
    question = info["template"].format(game_idea=game_idea)
    
    if use_rag and RAG_INITIALIZED:
        try:
            from app.services.rag_service import enhance_prompt
            question = enhance_prompt(game_idea, role, info["template"])
        except:
            pass
    
    if reference_content:
        question = f"""参考以下用户上传的策划案内容：

{reference_content[:2000]}

---

{question}

请结合参考内容，生成更符合用户需求的策划案。"""
    
    answer = call_api(question, api_key, model_id, base_url)
    
    if answer.startswith("API错误") or answer.startswith("请求错误"):
        return {"success": False, "error": answer, "role": info["role_name"]}
    
    return {
        "success": True,
        "role": info["role_name"],
        "filename": info["filename"],
        "content": answer
    }


def generate_all(
    game_idea: str,
    api_key: str,
    model_id: str,
    base_url: str,
    use_rag: bool = True,
    reference_content: str = "",
    roles: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    并发生成多个角色的策划案
    
    Args:
        game_idea: 游戏创意描述
        api_key: API密钥
        model_id: 模型ID
        base_url: API地址
        use_rag: 是否使用RAG增强
        reference_content: 参考内容
        roles: 角色列表
    
    Returns:
        生成结果列表（按角色顺序排列）
    """
    roles = roles or DEFAULT_ROLES
    workers = max(1, min(len(roles), 6))
    results: List[Dict[str, Any]] = []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                generate_single, game_idea, role, api_key, model_id, base_url, use_rag, reference_content
            ): role
            for role in roles if role in ROLE_TEMPLATES
        }
        for future in as_completed(futures):
            results.append(future.result())
    
    by_role_name: Dict[str, Dict[str, Any]] = {r.get("role"): r for r in results if r}
    ordered = []
    for role in roles:
        if role in ROLE_TEMPLATES:
            rn = ROLE_TEMPLATES[role]["role_name"]
            if rn in by_role_name:
                ordered.append(by_role_name[rn])
    
    return ordered


def save_file(filename: str, content: str, output_dir: Optional[str] = None) -> str:
    """
    保存文件到磁盘
    
    Args:
        filename: 文件名
        content: 文件内容
        output_dir: 输出目录
    
    Returns:
        文件路径
    """
    directory = output_dir or OUTPUT_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def generate_game_plan(
    game_idea: str,
    api_key: str,
    model_id: Optional[str] = None,
    base_url: Optional[str] = None,
    output_dir: Optional[str] = None,
    use_rag: bool = True,
    reference_content: str = "",
    roles: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    生成游戏策划案（主入口函数）
    
    Args:
        game_idea: 游戏创意描述
        api_key: API密钥
        model_id: 模型ID
        base_url: API地址
        output_dir: 输出目录
        use_rag: 是否使用RAG增强
        reference_content: 参考内容
        roles: 角色列表
    
    Returns:
        生成结果字典
    """
    from .config import DEFAULT_MODEL_ID, DEFAULT_BASE_URL
    
    if not game_idea or len(game_idea.strip()) < 3:
        return {"success": False, "error": "游戏想法太短"}
    
    model_id = model_id or DEFAULT_MODEL_ID
    base_url = base_url or DEFAULT_BASE_URL
    
    results = generate_all(game_idea, api_key, model_id, base_url, use_rag, reference_content, roles)
    
    saved_files = []
    errors = []
    for r in results:
        if r["success"]:
            filepath = save_file(r["filename"], r["content"], output_dir)
            saved_files.append({
                "role": r["role"],
                "filename": r["filename"],
                "filepath": filepath,
                "content": r["content"]
            })
        else:
            errors.append({"role": r.get("role", "未知"), "error": r.get("error", "未知错误")})
    
    if not saved_files and errors:
        return {"success": False, "error": "; ".join([f"{e['role']}: {e['error']}" for e in errors])}
    
    return {
        "success": True,
        "saved_files": saved_files,
        "errors": errors,
        "output_dir": output_dir or OUTPUT_DIR
    }
