# -*- coding: utf-8 -*-
"""
RAG服务模块 - LangChain增强上下文检索
"""

import os
from typing import List, Optional

LANGCHAIN_AVAILABLE = False
HuggingFaceEmbeddings = None
FAISS = None
RecursiveCharacterTextSplitter = None
Document = None

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    pass

KNOWLEDGE_BASE = """
=== 游戏开发基础流程 ===
1. 概念设计阶段：确定游戏类型、目标玩家、核心玩法
2. 原型开发阶段：制作最小可玩原型，验证核心机制
3. 生产阶段：美术资源制作、程序开发、音效制作并行进行
4. 测试阶段：内部测试、封闭测试、公开测试
5. 发布阶段：上线运营、持续更新

=== 程序员工作要点 ===
- 核心玩法编程：角色控制、游戏逻辑、物理系统
- 游戏引擎使用：Unity(C#)、Unreal(C++)、Godot(GDScript)
- 网络同步：多人游戏的客户端预测、服务器校验
- 性能优化：内存管理、渲染优化、资源加载
- 工具开发：关卡编辑器、配置工具、自动化脚本

=== 美术师工作要点 ===
- 角色设计：主角、NPC、敌人、Boss的概念图和建模
- 场景设计：背景、地形、建筑、植被
- UI设计：界面布局、图标、动效、交互反馈
- 特效设计：粒子效果、光影效果、技能特效
- 动画设计：角色动画、场景动画、过场动画

=== 音效师工作要点 ===
- 背景音乐：主菜单音乐、战斗音乐、场景音乐
- 音效设计：角色音效、环境音效、UI音效、技能音效
- 语音设计：角色配音、系统提示音、旁白
- 音频引擎：Wwise、FMOD集成

=== 编剧工作要点 ===
- 世界观设定：时代背景、地理环境、势力分布、历史事件
- 角色设计：主角性格背景、配角功能定位、反派动机手段
- 剧情结构：开篇引入、冲突升级、高潮对决、结局收尾
- 叙事方式：线性叙事、分支剧情、开放世界叙事

=== 常见游戏类型 ===
动作游戏：战斗系统、判定机制、连招系统、Boss设计
RPG游戏：成长系统、装备系统、技能树、任务系统、剧情分支
策略游戏：资源管理、单位控制、科技树、AI策略
射击游戏：射击手感、关卡设计、敌人AI、武器平衡
塔防游戏：塔类型设计、敌人波次、地图设计、经济系统
"""


class RAGKnowledgeBase:
    """RAG知识库类"""
    
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.is_initialized = False
        self.user_documents = []
    
    def initialize(self) -> bool:
        """初始化知识库"""
        if not LANGCHAIN_AVAILABLE:
            print("LangChain未安装，RAG功能禁用")
            return False
        
        try:
            print("初始化RAG知识库...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = [Document(page_content=KNOWLEDGE_BASE, metadata={"source": "base"})]
            split_docs = text_splitter.split_documents(docs)
            
            self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
            self.is_initialized = True
            print("RAG知识库初始化成功")
            return True
        except Exception as e:
            print(f"RAG初始化失败: {e}")
            return False
    
    def add_document(self, content: str, source: str = "user_upload") -> bool:
        """添加文档到知识库"""
        if not self.is_initialized or not content:
            return False
        
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            doc = Document(page_content=content, metadata={"source": source})
            split_docs = text_splitter.split_documents([doc])
            
            self.vectorstore.add_documents(split_docs)
            self.user_documents.append({"source": source, "content": content[:200] + "..."})
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
    
    def search(self, query: str, k: int = 3) -> str:
        """搜索知识库"""
        if not self.is_initialized:
            return ""
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return "\n\n".join([doc.page_content for doc in docs])
        except:
            return ""
    
    def enhance_prompt(self, game_idea: str, role: str, template: str) -> str:
        """增强提示词"""
        if not self.is_initialized:
            return template.format(game_idea=game_idea)
        
        role_keywords = {
            "programmer": "程序员 游戏开发 技术",
            "artist": "美术 角色设计 场景设计",
            "audio": "音效 背景音乐 声音设计",
            "writer": "编剧 剧情 世界观 角色"
        }
        
        query = f"{role_keywords.get(role, '')} {game_idea}"
        context = self.search(query)
        
        if context:
            return f"""参考以下游戏开发知识：

{context}

---

{template.format(game_idea=game_idea)}

请结合以上专业知识，给出更详细专业的工作安排。"""
        return template.format(game_idea=game_idea)
    
    def clear_user_documents(self):
        """清除用户文档"""
        self.user_documents = []


rag_kb = RAGKnowledgeBase()


def init_rag() -> bool:
    """初始化RAG知识库"""
    return rag_kb.initialize()


def add_document(content: str, source: str = "user_upload") -> bool:
    """添加文档到知识库"""
    return rag_kb.add_document(content, source)


def search_knowledge(query: str, k: int = 3) -> str:
    """搜索知识库"""
    return rag_kb.search(query, k)


def enhance_prompt(game_idea: str, role: str, template: str) -> str:
    """增强提示词"""
    return rag_kb.enhance_prompt(game_idea, role, template)


def clear_documents():
    """清除用户文档"""
    rag_kb.clear_user_documents()
