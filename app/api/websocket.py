from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Optional
import json
import asyncio
from uuid import uuid4

from ..core.mcp_server import MCPServer
from ..core.client_manager import ClientManager

class WebSocketAPI:
    def __init__(self, mcp_server: MCPServer, client_manager: ClientManager):
        self.mcp_server = mcp_server
        self.client_manager = client_manager

    async def handle_websocket(self, websocket: WebSocket):
        client_id = str(uuid4())
        try:
            await self.mcp_server.register_client(websocket, client_id)
            
            while True:
                message = await websocket.receive_json()
                await self._process_websocket_message(client_id, message)
                
        except WebSocketDisconnect:
            await self.client_manager.disconnect(client_id)
        except Exception as e:
            await self.client_manager.disconnect(client_id)
            raise e

    async def _process_websocket_message(self, client_id: str, message: dict):
        """Process incoming WebSocket messages"""
        try:
            if message.get("type") == "subscribe":
                topics = message.get("topics", [])
                for topic in topics:
                    await self.client_manager.subscribe(client_id, topic)
                    
            elif message.get("type") == "unsubscribe":
                topics = message.get("topics", [])
                for topic in topics:
                    await self.client_manager.unsubscribe(client_id, topic)
                    
            elif message.get("type") == "query":
                response = await self.mcp_server.handle_client_message(
                    client_id=client_id,
                    message=message
                )
                await self.client_manager.send_message(client_id, response)
                
            else:
                await self.mcp_server.handle_client_message(
                    client_id=client_id,
                    message=message
                )
                
        except Exception as e:
            error_message = {
                "type": "error",
                "error": str(e)
            }
            await self.client_manager.send_message(client_id, error_message)