# -*- coding: utf-8 -*-
"""
Flask Web前端 - 集成RAG/OCR/MCP
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import shutil
import zipfile
import tempfile
import atexit
import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_game_plan, ROLE_TEMPLATES, OUTPUT_DIR, init_rag

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR_ABS = os.path.join(BASE_DIR, OUTPUT_DIR)

app = Flask(__name__)

MODEL_PRESETS = {
    "deepseek": {"name": "DeepSeek", "model_id": "deepseek-chat", "base_url": "https://api.deepseek.com/v1/chat/completions"},
    "openai": {"name": "OpenAI", "model_id": "gpt-4o", "base_url": "https://api.openai.com/v1/chat/completions"},
    "qwen": {"name": "通义千问", "model_id": "qwen-turbo", "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"},
    "zhipu": {"name": "智谱AI", "model_id": "glm-4", "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions"},
    "custom": {"name": "自定义", "model_id": "", "base_url": ""}
}

temp_files = []
reference_content = ""

def resolve_model(model_preset: str, model_id: str, base_url: str):
    if model_preset in MODEL_PRESETS and model_preset != 'custom':
        preset = MODEL_PRESETS[model_preset]
        return model_id or preset['model_id'], base_url or preset['base_url']
    return model_id or "deepseek-chat", base_url or "https://api.deepseek.com/v1/chat/completions"

def cleanup():
    """清理临时文件和记录"""
    global temp_files, reference_content
    
    for f in temp_files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass
    
    if os.path.exists(OUTPUT_DIR_ABS):
        import time
        for _ in range(3):
            try:
                shutil.rmtree(OUTPUT_DIR_ABS)
                print(f"已清理: {OUTPUT_DIR_ABS}")
                break
            except Exception as e:
                print(f"清理尝试失败: {e}")
                time.sleep(0.5)
    
    try:
        from ocr_handler import clear_uploaded_documents
        clear_uploaded_documents()
    except:
        pass
    
    try:
        from rag_knowledge import clear_documents
        clear_documents()
    except:
        pass
    
    temp_files = []
    reference_content = ""
    print("清理完成")

atexit.register(cleanup)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    global reference_content
    data = request.get_json()
    game_idea = data.get('game_idea', '')
    api_key = data.get('api_key')
    model_preset = data.get('model_preset', 'deepseek')
    model_id = data.get('model_id', '')
    base_url = data.get('base_url', '')
    use_rag = data.get('use_rag', True)
    roles = data.get('roles')
    
    if not game_idea or len(game_idea.strip()) < 3:
        return jsonify({'success': False, 'error': '游戏想法太短'})
    
    if not api_key:
        return jsonify({'success': False, 'error': '请输入API Key'})
    
    model_id, base_url = resolve_model(model_preset, model_id, base_url)
    
    result = generate_game_plan(game_idea, api_key, model_id, base_url, use_rag=use_rag, reference_content=reference_content, roles=roles)
    return jsonify(result)

@app.route('/api/models', methods=['GET'])
def api_models():
    return jsonify({'models': MODEL_PRESETS})

@app.route('/api/roles', methods=['GET'])
def api_roles():
    try:
        from core import get_available_roles, get_default_roles
        return jsonify({
            'success': True,
            'roles': get_available_roles(),
            'default_roles': get_default_roles()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    global reference_content
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    try:
        from ocr_handler import process_upload_file
        result = process_upload_file(file)
        
        if result['success']:
            reference_content = result['text']
            
            try:
                from rag_knowledge import add_document
                add_document(result['text'], result['filename'])
            except:
                pass
            
            return jsonify({
                'success': True,
                'filename': result['filename'],
                'text_preview': result['text'][:500] + '...' if len(result['text']) > 500 else result['text'],
                'text_length': len(result['text'])
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', '解析失败')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/documents', methods=['GET'])
def api_documents():
    try:
        from ocr_handler import get_uploaded_documents
        docs = get_uploaded_documents()
        return jsonify({'success': True, 'documents': docs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/document/<int:index>', methods=['DELETE'])
def api_remove_document(index):
    try:
        from ocr_handler import remove_document
        success = remove_document(index)
        if success:
            return jsonify({'success': True, 'message': '已删除文档'})
        return jsonify({'success': False, 'error': '文档不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear-documents', methods=['POST'])
def api_clear_documents():
    global reference_content
    reference_content = ""
    
    try:
        from ocr_handler import clear_uploaded_documents
        clear_uploaded_documents()
    except:
        pass
    
    try:
        from rag_knowledge import clear_documents
        clear_documents()
    except:
        pass
    
    return jsonify({'success': True, 'message': '已清除所有文档'})

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(OUTPUT_DIR_ABS, filename)
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': '文件不存在'}), 404
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/api/download-zip', methods=['GET'])
def download_zip():
    if not os.path.exists(OUTPUT_DIR_ABS):
        return jsonify({'success': False, 'error': '没有文件'}), 404
    
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temp_zip.close()
    temp_files.append(temp_zip.name)
    
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(OUTPUT_DIR_ABS):
            filepath = os.path.join(OUTPUT_DIR_ABS, filename)
            if os.path.isfile(filepath):
                zipf.write(filepath, filename)
    
    return send_file(temp_zip.name, as_attachment=True, download_name='游戏策划案.zip')

def signal_handler(signum=None, frame=None):
    print("\n正在清理...")
    cleanup()
    sys.exit(0)

def run_web_app(host='0.0.0.0', port=5000, debug=False):
    if os.path.exists(OUTPUT_DIR_ABS):
        try:
            shutil.rmtree(OUTPUT_DIR_ABS)
            print(f"启动时清理旧文件: {OUTPUT_DIR_ABS}")
        except:
            pass
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"服务启动: http://{host}:{port}")
    print("正在初始化RAG知识库（后台运行）...")
    
    import threading
    rag_thread = threading.Thread(target=init_rag, daemon=True)
    rag_thread.start()
    
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    finally:
        cleanup()

if __name__ == '__main__':
    import sys
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    run_web_app(port=port)
