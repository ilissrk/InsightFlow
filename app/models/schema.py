from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class SourceType(str, Enum):
    STREAM = "stream"
    BATCH = "batch"
    API = "api"
    DATABASE = "database"

class DataSource(BaseModel):
    name: str
    type: SourceType
    config: Dict[str, Any]
    schema: Dict[str, Any]
    enabled: bool = True

class AnalyticsConfig(BaseModel):
    metrics: List[str]
    interval: int = Field(default=60, description="Processing interval in seconds")
    batch_size: int = 1000
    cache_ttl: int = 300

class AIModelConfig(BaseModel):
    model_name: str
    api_key: str
    temperature: float = 0.7
    max_tokens: int = 2000
    context_window: int = 4000

class ServerConfig(BaseModel):
    host: str
    port: int
    debug: bool = False
    workers: int = 4
    request_timeout: int = 30

class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = 5
    max_overflow: int = 10
    timeout: int = 30

class LogConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None

class InsightFlowConfig(BaseModel):
    server: ServerConfig
    database: DatabaseConfig
    analytics: AnalyticsConfig
    ai: AIModelConfig
    logging: LogConfig
    data_sources: Dict[str, DataSource]