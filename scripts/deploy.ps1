param(
  [switch]$InstallOCR,
  [switch]$InstallRAG,
  [switch]$NoStart,
  [string]$PythonCommand = ""
)

function Write-Step($text) { Write-Host "==> $text" -ForegroundColor Cyan }
function Test-Command { param([string]$Name) try { $null = Get-Command $Name -ErrorAction Stop; $true } catch { $false } }

$py = $PythonCommand
if (-not $py) {
  if (Test-Command "py") { $py = "py" }
  elseif (Test-Command "python") { $py = "python" }
  else { Write-Host "未找到 Python，可从 python.org 安装" -ForegroundColor Red; exit 1 }
}

Write-Step "创建虚拟环境"
if (-not (Test-Path ".venv")) {
  & $py -3 -m venv .venv
  if ($LASTEXITCODE -ne 0) { & $py -m venv .venv }
}

$activate = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activate) { . $activate } else { Write-Host "未找到虚拟环境激活脚本 .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Red; exit 1 }

Write-Step "升级 pip"
& python -m pip install -U pip setuptools wheel
if ($LASTEXITCODE -ne 0) { Write-Host "pip 升级失败" -ForegroundColor Red; exit 1 }

Write-Step "安装基础依赖"
& pip install flask requests
if ($LASTEXITCODE -ne 0) { Write-Host "基础依赖安装失败" -ForegroundColor Red; exit 1 }

if ($InstallOCR) {
  Write-Step "安装 OCR 依赖"
  & pip install pymupdf python-docx
  if ($LASTEXITCODE -ne 0) { Write-Host "OCR 依赖安装失败" -ForegroundColor Yellow }
}

if ($InstallRAG) {
  Write-Step "安装 RAG 依赖"
  & pip install langchain-community langchain-core langchain-text-splitters faiss-cpu
  if ($LASTEXITCODE -ne 0) { Write-Host "部分 RAG 依赖安装失败" -ForegroundColor Yellow }
  & pip install sentence-transformers
  if ($LASTEXITCODE -ne 0) {
    & pip install torch --index-url https://download.pytorch.org/whl/cpu
    & pip install sentence-transformers
    if ($LASTEXITCODE -ne 0) { Write-Host "sentence-transformers 安装失败" -ForegroundColor Yellow }
  }
}

if (-not $NoStart) {
  Write-Step "启动服务"
  & python main.py
}
