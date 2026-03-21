---
name: "project-env-setup"
description: "安装本项目技术栈并启动服务。IDE打开仓库或CI初始化时调用。"
---

# 项目技术栈安装前置

## 目标与触发
- 目标：为本仓库提供可复现的环境安装与启动流程，确保 Web 服务可运行，RAG/OCR 等能力可选启用
- 触发：AI IDE 打开本仓库后、首次部署、CI/CD 节点初始化、团队新成员入场时调用

## 支持平台
- Windows 10/11（推荐）
- macOS / Linux（等价命令见下）
- Python 最低版本 3.8（推荐 3.10+）

## 技术栈概览
- 后端：Python + Flask（Web）、Requests（HTTP）
- RAG（可选）：LangChain 社区版 + FAISS + HuggingFace Embeddings
- OCR（可选）：PyMuPDF（PDF）、python-docx（Word）
- 前端：HTML/CSS/JavaScript（内置页面）

## 快速步骤（Windows PowerShell）
1) 检查 Python
```powershell
py -3 --version
```
若无 Python，请先安装（从 python.org 或应用商店）。

2) 创建虚拟环境并启用
```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -U pip setuptools wheel
```

3) 安装基础依赖（必装）
```powershell
pip install flask requests
```

4) 安装可选能力
- OCR（解析 PDF/Word）
```powershell
pip install pymupdf python-docx
```
- RAG（检索增强；如无需可跳过）
```powershell
pip install langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers
```
若安装 sentence-transformers 失败，可先安装 CPU 版 torch：
```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers
```

5) 启动服务并验证
```powershell
python start.py
```
默认端口 8001；若直接运行：
```powershell
python web_app.py
```
默认端口 5000。浏览器访问对应地址后，输入 API Key 即可生成策划案。

## macOS / Linux 等价命令
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install flask requests
# OCR 可选
pip install pymupdf python-docx
# RAG 可选
pip install langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers
# 如需 CPU 版 torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
python start.py
```

## 功能开关与说明
- RAG：首次启动时后台初始化；未安装相关依赖时会自动降级为关闭状态
- OCR：未安装 PyMuPDF/python-docx 时，文件解析接口会返回“请安装”提示
- 多模型：页面“模型预设”选择对应供应商，输入 API Key 即可

## 验收检查
- 打开首页可用，生成至少 1 份策划案
- 启用 OCR 后能够解析上传的 PDF/Word/Markdown
- 启用 RAG 后生成内容更贴合知识库（无依赖则跳过）

## 常见问题
- pip 安装缓慢：可配置镜像源（如阿里云、清华镜像）
- faiss-cpu 安装失败：可暂时跳过 RAG，或改用 Linux/macOS 部署
- sentence-transformers/torch 安装失败：先安装 CPU 版 torch 再安装

## 何时调用本 SKILL
- 当 IDE 打开本仓库，需要“一键装好环境并启动服务”
- 当 CI 或新机器需要初始化运行本项目
- 当需要启用 OCR/RAG 扩展能力
