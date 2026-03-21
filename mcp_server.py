# -*- coding: utf-8 -*-
"""
MCP协议服务 - 兼容其他Agent调用
"""

import json
import sys
from typing import Dict, Any, Optional

class MCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "generate_game_plan",
                "description": "根据游戏想法生成策划案",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "game_idea": {"type": "string", "description": "游戏创意描述"},
                        "api_key": {"type": "string", "description": "AI模型API Key"},
                        "model_id": {"type": "string", "description": "模型ID，默认deepseek-chat"},
                        "base_url": {"type": "string", "description": "API地址"}
                    },
                    "required": ["game_idea", "api_key"]
                }
            },
            {
                "name": "get_roles",
                "description": "获取可生成的角色列表",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "upload_document",
                "description": "上传策划案文档用于参考",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "文档内容"},
                        "source": {"type": "string", "description": "文档来源"}
                    },
                    "required": ["content"]
                }
            }
        ]
    
    def handle_request(self, request: Dict) -> Dict:
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": self.tools}}
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "generate_game_plan":
                    from core import generate_game_plan
                    result = generate_game_plan(
                        arguments.get("game_idea"),
                        arguments.get("api_key"),
                        arguments.get("model_id"),
                        arguments.get("base_url")
                    )
                    return {"jsonrpc": "2.0", "id": request_id, "result": result}
                
                elif tool_name == "get_roles":
                    from core import ROLE_TEMPLATES
                    roles = [{"key": k, "name": v["role_name"]} for k, v in ROLE_TEMPLATES.items()]
                    return {"jsonrpc": "2.0", "id": request_id, "result": {"roles": roles}}
                
                elif tool_name == "upload_document":
                    from rag_knowledge import add_document
                    success = add_document(arguments.get("content"), arguments.get("source", "mcp"))
                    return {"jsonrpc": "2.0", "id": request_id, "result": {"success": success}}
                
                else:
                    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"未知工具: {tool_name}"}}
            
            else:
                return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"未知方法: {method}"}}
        
        except Exception as e:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": str(e)}}
    
    def run(self):
        print("MCP服务启动，等待输入...")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError as e:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"JSON解析错误: {e}"}}), flush=True)

def run_mcp_server():
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    run_mcp_server()
