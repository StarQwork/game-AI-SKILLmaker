# 创星游戏策划AI助理 - 技术与流程说明

## 项目概述

一款智能游戏策划文档生成工具。支持基于游戏创意自动生成四个基础策划案（程序员、美术师、音效师、编剧），并按 SKILL 标准结构输出。内置并发生成、RAG 检索增强、OCR 文档识别与 MCP 协议调用，提供可下载与打包能力。

## 功能实现总览

- 策划案生成
  - 默认四案：程序员/美术师/音效师/编剧，按 SKILL 标准输出结构化 Markdown
  - 可选策划/拆解：系统/关卡/战斗策划案与对应拆解案
  - 并发生成：线程池并发请求，按角色顺序稳定返回；失败项汇总错误信息
  - 文件落盘：保存到“游戏任务书/”，支持单个下载与 ZIP 打包
- 模型支持
  - 预设 DeepSeek/OpenAI/通义千问/智谱AI，自定义 Base URL 与 Model ID
  - 带指数退避与错误映射的请求重试
- RAG 检索增强（可选）
  - LangChain + FAISS 内置知识库；支持用户上传文档扩展
  - 后台线程初始化；未安装依赖自动降级为关闭
- OCR 文档识别（可选）
  - 支持 PDF/Word/Markdown，解析文本作为 RAG/提示参考
  - 文档列表支持预览、删除与清空
- MCP 协议
  - 提供 tools/list 与 tools/call，外部 Agent 可远程调用生成与上传
- 清理与稳健性
  - 启动/退出时清理生成文件与上传记录；异常时返回一致性错误信息

## 核心功能

### 1. 策划案生成
- 输入游戏创意描述
- 支持两种模式：新建模式和拆解模式
  - **新建模式**：默认生成4份基础策划案（程序员、美术师、音效师、编剧），可选生成额外策划案（系统策划案、关卡策划案、战斗策划案）
  - **拆解模式**：只生成拆解案（系统拆解案、关卡拆解案、战斗拆解案），不生成默认策划案和额外策划案
- 支持 Markdown 格式输出
- 支持单个下载和 ZIP 打包下载
- 支持在线预览和复制内容

### 2. 多模型支持
- DeepSeek（默认）
- OpenAI
- 通义千问
- 智谱AI
- 自定义模型（可配置 API 地址和模型 ID）

### 3. RAG 增强上下文检索
- 基于 LangChain + FAISS 的知识库
- 内置游戏开发专业知识
- 支持用户上传文档扩展知识库
- 可开关的 RAG 功能

### 4. OCR 文档识别
- 支持 PDF 文档解析
- 支持 Word(.docx/.doc) 文档解析
- 支持 Markdown(.md) 文档解析
- 拖拽上传支持
- 识别内容作为参考模板
- 文档预览和下载功能
- 单个文档删除（垃圾桶图标）

### 5. MCP 协议支持
- 兼容其他 Agent 调用
- 提供 tools/list 和 tools/call 接口
- 支持远程生成策划案

### 6. 安全与清理
- API Key 使用 localStorage 保存，刷新页面后保留
- 上传文档记录，关闭服务后清除
- 生成文件在服务启动时自动清理

## 项目结构

```
AIcehuazhuli/
├── game_helper.py      # 主入口（CLI/Web/MCP）
├── core.py             # 核心生成逻辑
├── web_app.py          # Flask Web 服务
├── rag_knowledge.py    # RAG 知识库模块
├── ocr_handler.py      # OCR 文档识别模块
├── mcp_server.py       # MCP 协议服务
├── start.py            # 快速启动脚本
├── templates/
│   └── index.html      # 前端页面
└── 创星游戏策划AI助理.md  # 需求文档
```

## 运行方式

### 安装依赖
```bash
pip install flask requests
pip install langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers
pip install pymupdf python-docx
```

### 启动服务
```bash
# 快速启动（推荐，端口 8001）
python start.py

# 直接运行 Web（端口 5000）
python web_app.py

# 命令行模式
python game_helper.py

# MCP 服务（需要 STDIN 驱动）
python mcp_server.py
```

### 访问地址
- Web 界面（start.py）：http://127.0.0.1:8001
- Web 界面（web_app.py）：http://127.0.0.1:5000

## API 接口

### 生成策划案
```
POST /api/generate
{
    "game_idea": "游戏创意描述",
    "api_key": "API密钥",
    "model_preset": "deepseek",
    "model_id": "模型ID（可选）",
    "base_url": "API地址（可选）",
    "use_rag": true,
    "roles": ["programmer", "artist", "audio", "writer", "system_plan", "level_plan", "combat_plan", "system_breakdown", "level_breakdown", "combat_breakdown"]
}
```

### 获取角色列表
```
GET /api/roles
```

### 上传文档
```
POST /api/upload
Content-Type: multipart/form-data
file: 文档文件（支持 PDF、Word、Markdown）
```

### 获取文档列表
```
GET /api/documents
```

### 删除单个文档
```
DELETE /api/document/<index>
```

### 清除所有文档
```
POST /api/clear-documents
```

### 下载文件
```
GET /api/download/<filename>
GET /api/download-zip
```

### 获取模型列表
```
GET /api/models
```

## MCP 工具列表

### generate_game_plan
生成游戏策划案
- 参数：game_idea, api_key, model_id, base_url

### get_roles
获取角色列表

### upload_document
上传参考文档
- 参数：content, source

## 技术栈

### 后端
- **Python 3.8+**
- **Flask**：Web 框架
- **Requests**：HTTP 请求
- **concurrent.futures**：线程池并发

### 前端
- **HTML5**：页面结构
- **CSS3**：样式设计（蓝橘色主题、对话框布局）
- **JavaScript**：交互逻辑
- **localStorage**：本地存储 API Key

### AI
- 支持多种大模型 API（DeepSeek、OpenAI、通义千问、智谱AI 等）
- 自定义模型支持
- 模型请求：指数退避与错误映射，提升稳定性

### RAG
- **LangChain**：LLM 应用框架
- **FAISS**：向量数据库
- **HuggingFace Embeddings**：文本向量化
- **sentence-transformers**：句子嵌入
- 可用性：后台初始化，缺依赖自动禁用

### OCR
- **PyMuPDF**：PDF 文档解析
- **python-docx**：Word 文档解析
- **原生读取**：Markdown 文档解析

### 协议
- **MCP (Model Context Protocol)**：Agent 通信协议

## 工作流程

### 1. 策划案生成流程
```
用户输入游戏创意 → 选择模型 → 输入 API Key
    ↓
选择策划案类型（默认4个 + 可选额外策划案 + 可选拆解案）
    ↓
启用 RAG（可选）→ 检索相关知识增强上下文
    ↓
并行调用 AI（线程池）生成选定的策划案，按角色稳定排序
    ↓
保存为 Markdown 文件 → 返回前端展示
    ↓
用户预览/下载/复制
```

### 2. 文档上传流程
```
用户上传文档（PDF/Word/MD）
    ↓
OCR 解析提取文本内容
    ↓
保存到内存列表 + RAG 知识库
    ↓
用户预览/下载/删除
    ↓
生成时作为参考模板
```

### 3. 服务启动流程
```
启动服务
    ↓
清理旧的生成文件
    ↓
初始化 RAG 知识库（后台）
    ↓
启动 Flask Web 服务
    ↓
等待用户请求
```

### 4. 服务关闭流程
```
收到关闭信号
    ↓
清理生成的策划案文件
    ↓
清理上传文档记录
    ↓
清理 RAG 知识库缓存
    ↓
退出服务
```

## 界面功能

### 策划案类型选择
- 模式切换：新建模式 / 拆解模式
- **新建模式**：
  - 默认生成：程序员、美术师、音效师、编剧（必选）
  - 额外策划案：系统策划案、关卡策划案、战斗策划案（可选）
  - 拆解案：禁用
- **拆解模式**：
  - 默认生成：禁用
  - 额外策划案：禁用
  - 拆解案：系统拆解案、关卡拆解案、战斗拆解案（可选）
- 多选框样式，支持勾选/取消勾选
- 模式切换时自动调整可选选项

### 上传文档区域
- 拖拽或点击上传
- 支持格式：PDF、Word(.docx/.doc)、Markdown(.md)
- 文档列表显示：文件名、字符数
- 操作按钮：预览、下载、删除（🗑️）

### 策划案结果区域
- 角色标题：程序员、美术师、音效师、编剧、系统策划、关卡策划、战斗策划、系统拆解、关卡拆解、战斗拆解
- 操作按钮：预览（绿色）、下载（蓝色）、复制（橙色）
- 内容展示：可展开/收起的 Markdown 渲染

### 模型配置区域
- 预设模型选择
- API Key 输入（localStorage 保存）
- 自定义模型配置（模型ID、API地址）
- RAG 开关

## SKILL 与一键部署

- 环境安装 SKILL：`.trae/skills/project-env-setup/SKILL.md`
  - 为 IDE/CI 提供“打开仓库即安装并启动”的步骤指南
- Windows 一键脚本：`tools/deploy.ps1`（可选安装 OCR/RAG）
  - 示例：`.\tools\deploy.ps1 -InstallOCR -InstallRAG` 或直接 `.\tools\deploy.ps1`

## 注意事项

1. 需要有效的 API Key 才能使用生成功能
2. RAG 功能需要安装 LangChain 相关依赖
3. OCR 功能需要安装 pymupdf 和 python-docx
4. API Key 保存在浏览器 localStorage，刷新页面后保留
5. 关闭服务会自动清理所有临时文件和记录
6. 服务启动时会自动清理上次残留的生成文件
