# 创星游戏策划 AI 助理

一款智能游戏策划文档生成工具：基于游戏创意，自动生成程序员/美术师/音效师/编剧四类策划案，按 SKILL 标准结构化输出。集成多模型调用、RAG 检索增强、OCR 文档识别、MCP 协议调用，支持在线预览、下载与 ZIP 打包。

## 功能特性
- 默认四案生成（程序员/美术师/音效师/编剧），SKILL 标准 Markdown 输出
- 可选策划/拆解案（系统/关卡/战斗）
- 线程池并发生成，稳定排序与错误汇总
- 多模型支持：DeepSeek/OpenAI/通义千问/智谱AI，自定义 Base URL + Model ID
- RAG 检索增强（可选）：LangChain + FAISS + Embeddings，用户上传文档扩展
- OCR 文档识别（可选）：PDF/Word/Markdown 解析
- MCP 工具：对接外部 Agent 的 tools/list、tools/call
- 文件落盘与清理：保存"游戏任务书/"，支持单个下载与 ZIP 打包，启动/退出清理

## 项目结构

```
game-AI-SKILLmaker/
├── app/                      # 应用主目录
│   ├── api/                 # API路由层
│   │   ├── __init__.py
│   │   └── routes.py        # Flask Web API端点
│   ├── core/                # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── config.py        # 全局配置（模型预设、输出目录）
│   │   ├── templates.py     # 策划案角色模板定义
│   │   ├── api_client.py    # AI模型API客户端
│   │   └── generator.py     # 策划案生成器（并发、排序、文件落盘）
│   ├── services/            # 服务层
│   │   ├── __init__.py
│   │   ├── rag_service.py   # RAG知识库服务（LangChain/FAISS/Embeddings）
│   │   ├── ocr_service.py   # OCR文档解析服务（PDF/Word/Markdown）
│   │   └── mcp_service.py   # MCP协议服务（tools/list、tools/call）
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── cleanup.py       # 清理函数
├── templates/               # 前端模板
│   └── index.html           # Web界面
├── scripts/                 # 脚本工具
│   └── deploy.ps1           # Windows一键部署脚本
├── config/                  # 配置文件目录
├── static/                  # 静态资源目录
├── main.py                  # 主入口
├── README.md
└── .trae/skills/            # SKILL文件
```

## 技术栈
- 后端：Python 3.8+、Flask、Requests、concurrent.futures（线程池并发）
- RAG：LangChain Community、FAISS、HuggingFace Embeddings、sentence-transformers
- OCR：PyMuPDF、python-docx（Markdown 原生读取）
- 前端：原生 HTML/CSS/JavaScript（localStorage 保存 API Key）
- 协议：MCP（Model Context Protocol）

## 优势亮点
- 产出结构标准：默认四案按 SKILL 标准输出，便于其他 AI IDE/Agent 直接消费
- 并发稳健：线程池并发 + 结果稳定排序 + 指数退避重试，提升吞吐与稳定性
- 易于扩展：多模型/自定义接口可插拔，RAG/OCR 可选安装自动降级
- 一键上手：提供环境安装 SKILL 与 Windows 部署脚本，IDE 打开即装即跑
- 面向协作：支持文档上传、知识扩展与远程工具调用，适配多角色工作流

## 快速开始
1) 安装依赖（基础）
```bash
pip install flask requests
```

2) 可选能力
```bash
# OCR
pip install pymupdf python-docx

# RAG
pip install langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers
```

3) 启动服务
```bash
# Web模式（端口 8001）
python main.py

# 命令行模式
python main.py --cli

# MCP服务模式
python main.py --mcp

# 指定端口
python main.py --port 9000
```

4) 访问地址
- http://127.0.0.1:8001 （默认）

## 环境安装 SKILL 与一键脚本
- SKILL：.trae/skills/project-env-setup/SKILL.md（IDE/CI 打开仓库时调用，自动装好环境并启动）
- Windows：scripts/deploy.ps1（-InstallOCR/-InstallRAG 可选）

## API 速览
- POST /api/generate：生成策划案（支持 roles、use_rag、自定义模型）
- GET /api/roles：获取可用角色
- POST /api/upload：上传文档（PDF/Word/Markdown）
- GET /api/documents / DELETE /api/document/<index> / POST /api/clear-documents
- GET /api/download-zip：打包下载所有产出
- GET /api/models：获取模型预设

## MCP 工具
- generate_game_plan：根据想法生成策划案（参数：game_idea、api_key、model_id、base_url）
- get_roles：获取可生成角色列表
- upload_document：上传文档扩展知识库

## 许可证
未指定许可证，若需开源协议可后续补充（MIT/Apache-2.0 等）。
