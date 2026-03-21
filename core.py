# -*- coding: utf-8 -*-
"""
游戏策划核心模块 - 集成RAG和OCR
"""

import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

OUTPUT_DIR = "游戏任务书"

DEFAULT_ROLES = ["programmer", "artist", "audio", "writer"]

ROLE_TEMPLATES = {
    "programmer": {
        "filename": "1_程序员.md",
        "role_name": "程序员",
        "type": "plan",
        "template": '''你是游戏程序员。基于用户的游戏想法："{game_idea}"。

请严格按 SKILL 标准格式输出完整文档（包含 frontmatter 与正文），并直接生成策划案内容：
---
name: "game-plan-programmer"
description: "生成程序程序员策划案；在新建项目或迭代技术方案时调用"
---

# 程序员策划案

## 需求分析
- 明确目标平台、目标用户与核心玩法循环
- 列出关键性能与内存目标（帧率、分辨率、设备约束）
- 基于用户想法提炼3-5个必须实现的核心功能与验收口径

## 技术选型
- 引擎：Godot（推荐当前稳定版本），以其为基底进行开发
- 语言：GDScript 优先；必要时使用 C# 扩展性能关键路径
- 编程工具：内置 ClaudeCode 作为编程助手，规范提示词与代码审阅流程
- 资产协作：约定与 NanoBanana2 输出资产格式与命名规则（纹理、动画、材质）
- 包管理与版本控制：Git + 约定式提交；CI 持续集成与自动构建

## 系统设计
- 模块分层：渲染与场景、输入、UI、战斗/玩法逻辑、数据与存档、资源管理
- 关键系统清单与接口约定：为每个系统给出职责、主要API与数据流
- Godot 资源与场景结构组织规范（节点命名、目录结构）

## 实施步骤
1. 初始化 Godot 项目与目录结构
2. 接入 ClaudeCode 工作流（代码生成、评审与单元测试约定）
3. 落地最小可玩的核心Loop原型（MVP）
4. 扩展功能迭代：按里程碑推进，保持可运行与可回归
5. 打包与发布管线配置（导出模板、平台目标）

## 交付物
- 源码与场景资产目录结构
- 核心系统设计说明与接口文档
- 可运行的原型包与构建脚本

## 风险与缓解
- 性能风险：采用分析器与剖析日志，必要时以 C# 优化
- 工具链风险：固定 Godot 版本与依赖镜像；提供降级方案
- 协作风险：以规范化命名与代码评审流程约束

## 工具与集成
- ClaudeCode：内置为编程助手，定义指令模板与审阅清单
- NanoBanana2：美术资产对接规范（贴图尺寸、导入参数、压缩设置）
'''
    },
    "artist": {
        "filename": "2_美术师.md",
        "role_name": "美术师",
        "type": "plan",
        "template": '''你是游戏美术师。基于用户的游戏想法："{game_idea}"。

请严格按 SKILL 标准格式输出完整文档（包含 frontmatter 与正文），并直接生成策划案内容：
---
name: "game-plan-artist"
description: "生成美术策划案；在设定风格与资产规范时调用"
---

# 美术策划案

## 需求分析
- 明确美术风格基调与参考（写实/卡通/像素等）
- 目标平台与分辨率适配要求
- 角色、场景、UI 的工作范围与优先级

## 技术选型
- 资产生产工具：NanoBanana2 为核心工具，定义输出规格与批处理流程
- 引擎兼容：Godot 导入管线与材质/纹理/动画配置规范
- 文件与命名：统一贴图尺寸、压缩格式、PBR 通道与命名规则

## 资产清单
- 角色与NPC：形象设定、动作列表、LOD/骨骼要求
- 场景与道具：模块化与复用策略、光照与烘焙需求
- UI 与特效：图标、界面套件、粒子/屏幕后期特效

## 实施步骤
1. 建立风格基线与风格板
2. 使用 NanoBanana2 批量生成初稿与变体
3. 与程序协作验证 Godot 导入与运行表现
4. 打磨阶段：统一风格、优化体积与性能

## 交付物
- 资产清单与交付包（源文件与导入设置）
- 风格指南与使用说明
- Godot 导入配置与材质模板

## 风险与缓解
- 性能与体积：约束贴图尺寸与压缩，复用材质
- 迭代返工：建立评审检查表与里程碑评审点
'''
    },
    "audio": {
        "filename": "3_音效师.md",
        "role_name": "音效师",
        "type": "plan",
        "template": '''你是游戏音频设计师。基于用户的游戏想法："{game_idea}"。

请严格按 SKILL 标准格式输出完整文档（包含 frontmatter 与正文），并直接生成策划案内容：
---
name: "game-plan-audio"
description: "生成音频策划案；在确立音乐/音效方向与集成方案时调用"
---

# 音频策划案

## 需求分析
- 明确音乐风格、氛围与交互触发点
- 列出演出点与关键反馈音效清单

## 技术选型
- 引擎集成：优先使用 Godot 内置音频系统；可选集成 FMOD
- 资源规范：采样率/比特率/通道数统一；循环点与淡入淡出规范
- 协作工具：与程序对接事件表；与美术统一特效联动

## 实施步骤
1. 搭建音频事件表与命名规范
2. 设计主旋律与环境氛围，产出试听样
3. 与程序在 Godot 中完成事件触发与混音配置
4. 平台适配与性能优化

## 交付物
- 音频资源包与事件表
- Godot 项目中的音频总线与混音配置
- 声音风格指南
'''
    },
    "writer": {
        "filename": "4_编剧.md",
        "role_name": "编剧",
        "type": "plan",
        "template": '''你是游戏编剧。基于用户的游戏想法："{game_idea}"。

请严格按 SKILL 标准格式输出完整文档（包含 frontmatter 与正文），并直接生成策划案内容：
---
name: "game-plan-writer"
description: "生成剧情与文本策划案；在确立世界观与任务线时调用"
---

# 编剧策划案

## 需求分析
- 核心主题与叙事基调、受众画像与内容边界
- 游戏玩法与叙事耦合点

## 架构设计
- 世界观设定与时间线
- 角色设定表：动机、成长线与关键关系
- 主线/支线任务结构与章节规划

## 文本规范
- 对白格式、分镜/旁白标注
- 本地化可扩展与变量占位规范

## 实施步骤
1. 世界观与设定集
2. 主线大纲与关键剧情节点
3. 任务与事件脚本，输出到 Godot 资源或外部表
4. 与程序/UI 对齐展示与触发时机

## 交付物
- 设定集与剧情大纲
- 任务/事件脚本与导入说明
- 本地化词条与占位符规范
'''
    },
    "system_plan": {
        "filename": "5_系统策划案.md",
        "role_name": "系统策划",
        "type": "plan",
        "template": '''你是游戏系统策划。用户想法："{game_idea}"

用Markdown格式写系统策划案：
1. 游戏核心系统设计
2. 玩家成长系统
3. 经济系统设计
4. 社交系统设计'''
    },
    "level_plan": {
        "filename": "6_关卡策划案.md",
        "role_name": "关卡策划",
        "type": "plan",
        "template": '''你是游戏关卡策划。用户想法："{game_idea}"

用Markdown格式写关卡策划案：
1. 关卡设计理念
2. 关卡结构布局
3. 难度曲线设计
4. 关卡奖励机制'''
    },
    "combat_plan": {
        "filename": "7_战斗策划案.md",
        "role_name": "战斗策划",
        "type": "plan",
        "template": '''你是游戏战斗策划。用户想法："{game_idea}"

用Markdown格式写战斗策划案：
1. 战斗系统设计
2. 技能系统设计
3. 敌人AI设计
4. 战斗平衡性调整'''
    },
    "system_breakdown": {
        "filename": "8_系统拆解案.md",
        "role_name": "系统拆解",
        "type": "breakdown",
        "template": '''你是游戏系统拆解师。用户想法："{game_idea}"

用Markdown格式写系统拆解案：
1. 系统功能拆解
2. 模块划分
3. 开发优先级
4. 技术实现要点'''
    },
    "level_breakdown": {
        "filename": "9_关卡拆解案.md",
        "role_name": "关卡拆解",
        "type": "breakdown",
        "template": '''你是游戏关卡拆解师。用户想法："{game_idea}"

用Markdown格式写关卡拆解案：
1. 关卡元素拆解
2. 关卡流程拆解
3. 资源需求分析
4. 开发工作量评估'''
    },
    "combat_breakdown": {
        "filename": "10_战斗拆解案.md",
        "role_name": "战斗拆解",
        "type": "breakdown",
        "template": '''你是游戏战斗拆解师。用户想法："{game_idea}"

用Markdown格式写战斗拆解案：
1. 战斗机制拆解
2. 数值体系拆解
3. 交互逻辑拆解
4. 性能优化要点'''
    }
}

RAG_INITIALIZED = False

def init_rag():
    global RAG_INITIALIZED
    try:
        from rag_knowledge import init_rag as rag_init
        RAG_INITIALIZED = rag_init()
        return RAG_INITIALIZED
    except ImportError:
        return False

def call_api(question: str, api_key: str, model_id: str = "deepseek-chat", base_url: str = "https://api.deepseek.com/v1/chat/completions", max_retries: int = 3) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(base_url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)
                    continue
                return f"API错误：请求过于频繁，请稍后再试"
            if response.status_code >= 500:
                if attempt < max_retries - 1:
                    import time
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
                import time
                time.sleep(1)
                continue
            return "请求错误：网络连接失败"
        except Exception as e:
            return f"请求错误：{e}"
    
    return "请求错误：已达到最大重试次数"

def generate_single(game_idea: str, role: str, api_key: str, model_id: str, base_url: str, use_rag: bool = True, reference_content: str = "") -> Dict[str, Any]:
    if role not in ROLE_TEMPLATES:
        return {"success": False, "error": f"未知角色: {role}"}
    
    info = ROLE_TEMPLATES[role]
    question = info["template"].format(game_idea=game_idea)
    
    if use_rag and RAG_INITIALIZED:
        try:
            from rag_knowledge import enhance_prompt
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
    return {"success": True, "role": info["role_name"], "filename": info["filename"], "content": answer}

def generate_all(game_idea: str, api_key: str, model_id: str, base_url: str, use_rag: bool = True, reference_content: str = "", roles: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    roles = roles or DEFAULT_ROLES
    workers = max(1, min(len(roles), 6))
    results: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(generate_single, game_idea, role, api_key, model_id, base_url, use_rag, reference_content): role
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
    directory = output_dir or OUTPUT_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def get_available_roles() -> Dict[str, Dict[str, str]]:
    return {
        role_key: {
            "name": role_info["role_name"],
            "type": role_info["type"],
            "filename": role_info["filename"]
        }
        for role_key, role_info in ROLE_TEMPLATES.items()
    }

def get_default_roles() -> List[str]:
    return DEFAULT_ROLES

def generate_game_plan(game_idea: str, api_key: str, model_id: Optional[str] = None, base_url: Optional[str] = None, output_dir: Optional[str] = None, use_rag: bool = True, reference_content: str = "", roles: Optional[List[str]] = None) -> Dict[str, Any]:
    if not game_idea or len(game_idea.strip()) < 3:
        return {"success": False, "error": "游戏想法太短"}
    
    model_id = model_id or "deepseek-chat"
    base_url = base_url or "https://api.deepseek.com/v1/chat/completions"
    
    results = generate_all(game_idea, api_key, model_id, base_url, use_rag, reference_content, roles)
    
    saved_files = []
    errors = []
    for r in results:
        if r["success"]:
            filepath = save_file(r["filename"], r["content"], output_dir)
            saved_files.append({"role": r["role"], "filename": r["filename"], "filepath": filepath, "content": r["content"]})
        else:
            errors.append({"role": r.get("role", "未知"), "error": r.get("error", "未知错误")})
    
    if not saved_files and errors:
        return {"success": False, "error": "; ".join([f"{e['role']}: {e['error']}" for e in errors])}
    
    return {"success": True, "saved_files": saved_files, "errors": errors, "output_dir": output_dir or OUTPUT_DIR}
