import logging
from typing import Dict, Any, Optional
from ..models.schema import DataSource
from .client_manager import ClientManager

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.client_manager = ClientManager()
        self._message_processors = {}

    async def process_message(self, message: Dict[str, Any], source: DataSource) -> Optional[Dict[str, Any]]:
        """Process incoming messages from various sources"""
        try:
            message_type = message.get("type", "default")
            processor = self._message_processors.get(message_type)
            
            if processor:
                processed_message = await processor(message)
                await self._broadcast_to_clients(processed_message)
                return processed_message
            
            logger.warning(f"No processor found for message type: {message_type}")
            return None
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    async def _broadcast_to_clients(self, message: Dict[str, Any]):
        """Broadcast processed messages to connected clients"""
        await self.client_manager.broadcast(message)

    def register_processor(self, message_type: str, processor_func):
        """Register a new message processor"""
        self._message_processors[message_type] = processor_func
