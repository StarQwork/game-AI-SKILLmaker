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
- 文件落盘与清理：保存“游戏任务书/”，支持单个下载与 ZIP 打包，启动/退出清理

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
# 推荐（端口 8001）
python start.py

# 或直接运行（端口 5000）
python web_app.py
```

4) 访问地址
- http://127.0.0.1:8001 （start.py）
- http://127.0.0.1:5000 （web_app.py）

## 环境安装 SKILL 与一键脚本
- SKILL：.trae/skills/project-env-setup/SKILL.md（IDE/CI 打开仓库时调用，自动装好环境并启动）
- Windows：tools/deploy.ps1（-InstallOCR/-InstallRAG 可选）

## API 速览
- POST /api/generate：生成策划案（支持 roles、use_rag、自定义模型）
- GET /api/roles：获取可用角色
- POST /api/upload：上传文档（PDF/Word/Markdown）
- GET /api/documents / DELETE /api/document/<index> / POST /api/clear-documents
- GET /api/download-zip：打包下载所有产出
- GET /api/models：获取模型预设

## 目录结构
```
AIcehuazhuli/
├── core.py            # 核心生成（并发、排序、文件落盘、错误映射）
├── web_app.py         # Flask Web 服务（API、打包下载、清理）
├── rag_knowledge.py   # RAG（LangChain/FAISS/Embeddings，后台初始化与降级）
├── ocr_handler.py     # OCR（PDF/Word/Markdown 解析与文档管理）
├── mcp_server.py      # MCP 服务（tools/list、tools/call）
├── start.py           # 快速启动（固定端口 8001，含启动前清理）
├── templates/index.html
└── .trae/skills/project-env-setup/SKILL.md
```

## MCP 工具
- generate_game_plan：根据想法生成策划案（参数：game_idea、api_key、model_id、base_url）
- get_roles：获取可生成角色列表
- upload_document：上传文档扩展知识库

## 许可证
未指定许可证，若需开源协议可后续补充（MIT/Apache-2.0 等）。

