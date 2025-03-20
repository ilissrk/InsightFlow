from fastapi import APIRouter, HTTPException, Depends, WebSocket
from typing import Dict, Any, List
from ..models.schema import DataSource, AnalyticsConfig
from ..core.mcp_server import MCPServer

class RestAPI:
    def __init__(self, mcp_server: MCPServer, data_processor: DataProcessor, ai_connector: ClaudeConnector):
        self.router = APIRouter()
        self.mcp_server = mcp_server
        self.data_processor = data_processor
        self.ai_connector = ai_connector
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/tools")
        async def list_tools():
            """List all available MCP tools"""
            return {"tools": self.mcp_server.tools}

        @self.router.post("/tool/{tool_name}")
        async def call_tool(tool_name: str, parameters: Dict[str, Any]):
            """Execute an MCP tool"""
            try:
                result = await self.mcp_server.handle_tool_call(tool_name, parameters, "rest-api")
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time MCP communication"""
            await websocket.accept()
            self.mcp_server.websocket_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    response = await self.mcp_server.handle_client_message(data, str(websocket))
                    await websocket.send_json(response)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                self.mcp_server.websocket_connections.remove(websocket)
