# -*- coding: utf-8 -*-
"""
路由模块 - Flask Web API路由
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import shutil
import zipfile
import tempfile
import atexit
import signal
import threading

from app.core import (
    generate_game_plan, ROLE_TEMPLATES, OUTPUT_DIR,
    get_available_roles, get_default_roles, MODEL_PRESETS
)
from app.core.api_client import resolve_model
from app.core.generator import init_rag
from app.core.config import OUTPUT_DIR_ABS, BASE_DIR

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)

temp_files = []
reference_content = ""


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
        from app.services import clear_uploaded_documents, clear_documents
        clear_uploaded_documents()
        clear_documents()
    except:
        pass
    
    temp_files = []
    reference_content = ""
    print("清理完成")


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """生成策划案API"""
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
    
    result = generate_game_plan(
        game_idea, api_key, model_id, base_url,
        use_rag=use_rag, reference_content=reference_content, roles=roles
    )
    return jsonify(result)


@app.route('/api/models', methods=['GET'])
def api_models():
    """获取模型预设列表"""
    return jsonify({'models': MODEL_PRESETS})


@app.route('/api/roles', methods=['GET'])
def api_roles():
    """获取角色列表"""
    try:
        return jsonify({
            'success': True,
            'roles': get_available_roles(),
            'default_roles': get_default_roles()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """上传文档API"""
    global reference_content
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    try:
        from app.services import process_upload_file
        result = process_upload_file(file)
        
        if result['success']:
            reference_content = result['text']
            
            try:
                from app.services import add_document
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
    """获取文档列表API"""
    try:
        from app.services import get_uploaded_documents
        docs = get_uploaded_documents()
        return jsonify({'success': True, 'documents': docs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/document/<int:index>', methods=['DELETE'])
def api_remove_document(index):
    """删除文档API"""
    try:
        from app.services import remove_document
        success = remove_document(index)
        if success:
            return jsonify({'success': True, 'message': '已删除文档'})
        return jsonify({'success': False, 'error': '文档不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/clear-documents', methods=['POST'])
def api_clear_documents():
    """清除所有文档API"""
    global reference_content
    reference_content = ""
    
    try:
        from app.services import clear_uploaded_documents, clear_documents
        clear_uploaded_documents()
        clear_documents()
    except:
        pass
    
    return jsonify({'success': True, 'message': '已清除所有文档'})


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """下载单个文件API"""
    filepath = os.path.join(OUTPUT_DIR_ABS, filename)
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': '文件不存在'}), 404
    return send_file(filepath, as_attachment=True, download_name=filename)


@app.route('/api/download-zip', methods=['GET'])
def download_zip():
    """打包下载所有文件API"""
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
    """信号处理器"""
    print("\n正在清理...")
    cleanup()
    sys.exit(0)


def run_web_app(host='0.0.0.0', port=5000, debug=False):
    """
    启动Web应用
    
    Args:
        host: 监听地址
        port: 监听端口
        debug: 是否开启调试模式
    """
    if os.path.exists(OUTPUT_DIR_ABS):
        try:
            shutil.rmtree(OUTPUT_DIR_ABS)
            print(f"启动时清理旧文件: {OUTPUT_DIR_ABS}")
        except:
            pass
    
    if os.name != 'nt':
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    print(f"服务启动: http://{host}:{port}")
    print("正在初始化RAG知识库（后台运行）...")
    
    rag_thread = threading.Thread(target=init_rag, daemon=True)
    rag_thread.start()
    
    app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
