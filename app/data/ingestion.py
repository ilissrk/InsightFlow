from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import asyncio
from pydantic import BaseModel
from collections import deque

class DataSource(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]
    schema: Dict[str, Any]

class DataValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate(self, data: Dict) -> bool:
        try:
            # Implement schema validation logic
            return True
        except Exception as e:
            raise ValueError(f"Validation error: {str(e)}")

class DataSourceAdapter(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def read(self) -> Dict:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

class StreamAdapter(DataSourceAdapter):
    def __init__(self, config: Dict):
        self.config = config
        self.buffer = deque(maxlen=1000)
        self.connected = False

    async def connect(self) -> None:
        # Implement stream connection logic
        self.connected = True

    async def read(self) -> Dict:
        if not self.connected:
            raise ConnectionError("Stream not connected")
        return self.buffer.popleft() if self.buffer else None

    async def disconnect(self) -> None:
        self.connected = False

class BatchAdapter(DataSourceAdapter):
    def __init__(self, config: Dict):
        self.config = config

    async def connect(self) -> None:
        # Implement batch connection logic
        pass

    async def read(self) -> Dict:
        # Implement batch read logic
        pass

    async def disconnect(self) -> None:
        # Implement disconnect logic
        pass

class DataIngestion:
    def __init__(self):
        self.sources: Dict[str, DataSource] = {}
        self.adapters: Dict[str, DataSourceAdapter] = {}
        self.validators: Dict[str, DataValidator] = {}
        self.rate_limits: Dict[str, float] = {}

    async def register_source(self, source: DataSource) -> None:
        """Register a new data source"""
        try:
            self.sources[source.name] = source
            self.validators[source.name] = DataValidator(source.schema)
            
            if source.type == "stream":
                self.adapters[source.name] = StreamAdapter(source.config)
            elif source.type == "batch":
                self.adapters[source.name] = BatchAdapter(source.config)
            else:
                raise ValueError(f"Unsupported source type: {source.type}")
            
            await self.adapters[source.name].connect()
        except Exception as e:
            raise Exception(f"Error registering source: {str(e)}")

    async def ingest_data(self, source_name: str, data: Dict) -> Dict:
        """Ingest data from a source"""
        try:
            if source_name not in self.sources:
                raise ValueError(f"Unknown source: {source_name}")

            if not self.validators[source_name].validate(data):
                raise ValueError("Data validation failed")

            # Apply rate limiting
            if source_name in self.rate_limits:
                await asyncio.sleep(1 / self.rate_limits[source_name])

            # Add metadata
            enriched_data = {
                "source": source_name,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }

            return enriched_data
        except Exception as e:
            raise Exception(f"Ingestion error: {str(e)}")

    async def start_streaming(self, source_name: str) -> None:
        """Start streaming from a source"""
        try:
            if source_name not in self.sources:
                raise ValueError(f"Unknown source: {source_name}")

            adapter = self.adapters[source_name]
            while True:
                data = await adapter.read()
                if data:
                    await self.ingest_data(source_name, data)
                await asyncio.sleep(0.1)
        except Exception as e:
            raise Exception(f"Streaming error: {str(e)}")

    def set_rate_limit(self, source_name: str, rate: float) -> None:
        """Set rate limit for a source in requests per second"""
        self.rate_limits[source_name] = rate

    async def cleanup(self) -> None:
        """Cleanup and disconnect all sources"""
        for adapter in self.adapters.values():
            await adapter.disconnect()