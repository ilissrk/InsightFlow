import asyncio
import logging
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from fastapi import WebSocket
import json
from ..config import config
from ..models.schema import AIModelConfig

logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.ai_config: AIModelConfig = config.get_config().ai
        self.anthropic_client = Anthropic(api_key=self.ai_config.api_key)
        self.active_sessions: Dict[str, Any] = {}
        self.tools = self._initialize_tools()
        self.websocket_connections: List[WebSocket] = []

    def _initialize_tools(self):
        """Initialize available MCP tools"""
        return {
            "data_analysis": {
                "name": "analyze_data",
                "description": "Analyze data and generate insights",
                "parameters": {
                    "data": "object",
                    "metrics": "array",
                    "timeframe": "string"
                }
            },
            "query_data": {
                "name": "query_data",
                "description": "Query historical data",
                "parameters": {
                    "query": "string",
                    "filters": "object",
                    "limit": "integer"
                }
            }
        }

    async def initialize(self):
        """Initialize the MCP server"""
        try:
            # Initialize core components
            self.data_processor = DataProcessor()
            self.analytics_engine = AnalyticsEngine()
            
            # Register default tools
            await self._register_default_tools()
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MCP server: {e}")
            raise

    async def _register_default_tools(self):
        """Register default MCP tools"""
        self.tools.update({
            "data_analysis": {
                "name": "analyze_data",
                "description": "Analyze data and generate insights",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_source": {"type": "string"},
                        "metrics": {"type": "array", "items": {"type": "string"}},
                        "timeframe": {"type": "string"}
                    },
                    "required": ["data_source", "metrics"]
                }
            },
            "query_data": {
                "name": "query_data",
                "description": "Query historical data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "filters": {"type": "object"},
                        "limit": {"type": "integer"}
                    },
                    "required": ["query"]
                }
            },
            "generate_insight": {
                "name": "generate_insight",
                "description": "Generate AI-powered insights from data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_source": {"type": "string"},
                        "context": {"type": "string"}
                    },
                    "required": ["data_source"]
                }
            }
        })

    async def handle_client_message(self, message: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """Handle incoming MCP client messages"""
        try:
            message_type = message.get("type")
            if message_type == "tool_call":
                return await self.handle_tool_call(message["tool"], message["parameters"], client_id)
            elif message_type == "list_tools":
                return {"tools": self.tools}
            else:
                raise ValueError(f"Unsupported message type: {message_type}")
        except Exception as e:
            return {"error": str(e)}

    async def shutdown(self):
        """Gracefully shutdown the MCP server"""
        try:
            # Close all active WebSocket connections
            for ws in self.websocket_connections:
                await ws.close()
            
            # Cleanup resources
            self.active_sessions.clear()
            self.websocket_connections.clear()
            
            logger.info("MCP server shutdown complete")
        except Exception as e:
            logger.error(f"Error during MCP server shutdown: {e}")
            raise

    async def _cleanup_session(self, session_id: str):
        """Clean up a specific session"""
        if session_id in self.active_sessions:
            try:
                # Get session data before cleanup
                session_data = self.active_sessions[session_id]
                
                # Perform any necessary cleanup tasks
                if 'resources' in session_data:
                    await self._release_resources(session_data['resources'])
                
                # Remove session from active sessions
                del self.active_sessions[session_id]
                
                logger.info(f"Successfully cleaned up session: {session_id}")
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {str(e)}")
                raise
