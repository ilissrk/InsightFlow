import logging
from typing import Dict, Set, Any
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ClientManager:
    def __init__(self):
        self.active_clients: Set[WebSocket] = set()
        self.client_subscriptions: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        """Connect a new client"""
        await websocket.accept()
        self.active_clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.active_clients)}")

    async def disconnect(self, websocket: WebSocket):
        """Disconnect a client"""
        self.active_clients.remove(websocket)
        for subscriptions in self.client_subscriptions.values():
            subscriptions.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.active_clients)}")

    async def subscribe(self, websocket: WebSocket, topic: str):
        """Subscribe a client to a topic"""
        if topic not in self.client_subscriptions:
            self.client_subscriptions[topic] = set()
        self.client_subscriptions[topic].add(websocket)

    async def broadcast(self, message: Dict[str, Any], topic: str = None):
        """Broadcast message to all clients or topic subscribers"""
        disconnected_clients = set()

        target_clients = (self.client_subscriptions.get(topic, set()) 
                        if topic else self.active_clients)

        for client in target_clients:
            try:
                await client.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to client: {str(e)}")
                disconnected_clients.add(client)

        for client in disconnected_clients:
            await self.disconnect(client)
