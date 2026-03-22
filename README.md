# 创星游戏策划 AI 助理

一款智能游戏策划文档生成工具：基于游戏创意，自动生成程序员/美术师/音效师/编剧四类策划案，按 SKILL 标准结构化输出。集成多模型调用、RAG 检索增强、OCR 文档识别、MCP 协议调用，支持在线预览、下载与 ZIP 打包。

## 功能特性

- **默认四案生成**：程序员/美术师/音效师/编剧，SKILL 标准 Markdown 输出
- **可选策划/拆解案**：系统/关卡/战斗策划案与拆解案
- **并发生成**：线程池并发（最大6线程）+ 结果稳定排序 + 错误汇总
- **多模型支持**：DeepSeek/OpenAI/通义千问/智谱AI，自定义 Base URL + Model ID
- **RAG 检索增强**（可选）：LangChain + FAISS + HuggingFace Embeddings，支持用户上传文档扩展
- **OCR 文档识别**（可选）：PDF/Word/Markdown 解析
- **MCP 工具**：对接外部 Agent 的 tools/list、tools/call
- **文件落盘与清理**：保存到"游戏任务书/"，支持单个下载与 ZIP 打包，启动/退出自动清理

## 项目结构

```
game-AI-SKILLmaker/
├── app/                      # 应用主目录
│   ├── __init__.py
│   ├── api/                  # API路由层
│   │   ├── __init__.py
│   │   └── routes.py         # Flask Web API端点
│   ├── core/                 # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── config.py         # 全局配置（模型预设、输出目录）
│   │   ├── templates.py      # 策划案角色模板定义
│   │   ├── api_client.py     # AI模型API客户端
│   │   └── generator.py      # 策划案生成器（并发、排序、文件落盘）
│   ├── services/             # 服务层
│   │   ├── __init__.py
│   │   ├── rag_service.py    # RAG知识库服务（LangChain/FAISS/Embeddings）
│   │   ├── ocr_service.py    # OCR文档解析服务（PDF/Word/Markdown）
│   │   └── mcp_service.py    # MCP协议服务（tools/list、tools/call）
│   └── utils/                # 工具函数
│       ├── __init__.py
│       └── cleanup.py        # 清理函数
├── templates/                # 前端模板
│   └── index.html            # Web界面
├── scripts/                  # 脚本工具
│   └── deploy.ps1            # Windows一键部署脚本
├── .trae/skills/             # SKILL文件
│   └── project-env-setup/
│       └── SKILL.md          # 环境安装SKILL
├── main.py                   # 主入口
├── README.md
└── 创星游戏策划AI助理.md      # 详细技术文档
```

## 技术栈

### 后端
- **Python 3.8+**
- **Flask**：Web 框架
- **Requests**：HTTP 请求
- **concurrent.futures**：线程池并发（最大6线程）

### 前端
- **HTML5/CSS3/JavaScript**：原生实现
- **localStorage**：本地存储 API Key
- **AbortController**：请求超时控制（180s）

### AI
- 支持多种大模型 API（DeepSeek、OpenAI、通义千问、智谱AI 等）
- 自定义模型支持
- API 超时：120s，max_tokens：4000

### RAG（可选）
- **LangChain Community**：LLM 应用框架
- **FAISS**：向量数据库
- **HuggingFace Embeddings**：文本向量化
- **sentence-transformers**：句子嵌入

### OCR（可选）
- **PyMuPDF**：PDF 文档解析
- **python-docx**：Word 文档解析
- **原生读取**：Markdown 文档解析

### 协议
- **MCP (Model Context Protocol)**：Agent 通信协议

## 优势亮点

- **产出结构标准**：默认四案按 SKILL 标准输出，便于其他 AI IDE/Agent 直接消费
- **并发稳健**：线程池并发 + 结果稳定排序 + 指数退避重试，提升吞吐与稳定性
- **易于扩展**：多模型/自定义接口可插拔，RAG/OCR 可选安装自动降级
- **一键上手**：提供环境安装 SKILL 与 Windows 部署脚本，IDE 打开即装即跑
- **面向协作**：支持文档上传、知识扩展与远程工具调用，适配多角色工作流
- **跨平台兼容**：支持 Windows/Linux/macOS，自动适配信号处理

## 快速开始

### 1. 安装依赖（基础）

```bash
pip install flask requests
```

### 2. 可选能力

```bash
# OCR 文档识别
pip install pymupdf python-docx

# RAG 检索增强
pip install langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers
```

### 3. 启动服务

```bash
# Web模式（默认端口 8001）
python main.py

# 命令行模式
python main.py --cli

# MCP服务模式
python main.py --mcp

# 指定端口
python main.py --port 9000
```

### 4. 访问地址

- http://127.0.0.1:8001 （默认）

## 环境安装 SKILL 与一键脚本

- **SKILL**：`.trae/skills/project-env-setup/SKILL.md`（IDE/CI 打开仓库时调用，自动装好环境并启动）
- **Windows**：`scripts/deploy.ps1`（`-InstallOCR`/`-InstallRAG` 可选）

```powershell
# 基础安装
.\scripts\deploy.ps1

# 包含OCR
.\scripts\deploy.ps1 -InstallOCR

# 包含RAG
.\scripts\deploy.ps1 -InstallRAG

# 全部安装
.\scripts\deploy.ps1 -InstallOCR -InstallRAG
```

## API 速览

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/generate` | POST | 生成策划案（支持 roles、use_rag、自定义模型） |
| `/api/roles` | GET | 获取可用角色列表 |
| `/api/upload` | POST | 上传文档（PDF/Word/Markdown） |
| `/api/documents` | GET | 获取文档列表 |
| `/api/document/<index>` | DELETE | 删除单个文档 |
| `/api/clear-documents` | POST | 清除所有文档 |
| `/api/download/<filename>` | GET | 下载单个文件 |
| `/api/download-zip` | GET | 打包下载所有产出 |
| `/api/models` | GET | 获取模型预设列表 |

### 生成策划案示例

```json
POST /api/generate
{
    "game_idea": "一款像素风格的 Roguelike 地牢探险游戏",
    "api_key": "your-api-key",
    "model_preset": "deepseek",
    "model_id": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1/chat/completions",
    "use_rag": true,
    "roles": ["programmer", "artist", "audio", "writer"]
}
```

## MCP 工具

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `generate_game_plan` | 根据想法生成策划案 | game_idea, api_key, model_id, base_url |
| `get_roles` | 获取可生成角色列表 | - |
| `upload_document` | 上传文档扩展知识库 | content, source |

## 性能优化

- **并发生成**：最大6线程并发，按角色顺序稳定返回
- **API 超时**：120秒请求超时，max_tokens 4000
- **前端控制**：180秒超时自动中断，带进度提示
- **RAG 优化**：网络超时30秒，初始化失败自动降级

## 许可证

未指定许可证，若需开源协议可后续补充（MIT/Apache-2.0 等）。
