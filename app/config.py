import os
import yaml
from typing import Dict, Any
from pathlib import Path
from .models.schema import InsightFlowConfig, ServerConfig, DatabaseConfig, AnalyticsConfig, AIModelConfig, LogConfig

class Config:
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from environment variables and config files"""
        # Default config path
        config_path = os.getenv("INSIGHTFLOW_CONFIG", "config/config.yaml")
        
        # Load from file if exists
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        
        # Override with environment variables
        self._config = self._override_from_env(self._config)
        
        # Validate and create config objects
        self.config = InsightFlowConfig(
            server=ServerConfig(
                host=self._config.get("server", {}).get("host", "0.0.0.0"),
                port=int(self._config.get("server", {}).get("port", 8000)),
                debug=bool(self._config.get("server", {}).get("debug", False)),
                workers=int(self._config.get("server", {}).get("workers", 4)),
                request_timeout=int(self._config.get("server", {}).get("request_timeout", 30))
            ),
            database=DatabaseConfig(
                url=os.getenv("DATABASE_URL", self._config.get("database", {}).get("url", "sqlite:///data.db")),
                pool_size=int(self._config.get("database", {}).get("pool_size", 5)),
                max_overflow=int(self._config.get("database", {}).get("max_overflow", 10)),
                timeout=int(self._config.get("database", {}).get("timeout", 30))
            ),
            analytics=AnalyticsConfig(
                metrics=self._config.get("analytics", {}).get("metrics", ["count", "average", "sum"]),
                interval=int(self._config.get("analytics", {}).get("interval", 60)),
                batch_size=int(self._config.get("analytics", {}).get("batch_size", 1000)),
                cache_ttl=int(self._config.get("analytics", {}).get("cache_ttl", 300))
            ),
            ai=AIModelConfig(
                model_name=os.getenv("AI_MODEL_NAME", self._config.get("ai", {}).get("model_name", "claude-2")),
                api_key=os.getenv("CLAUDE_API_KEY", self._config.get("ai", {}).get("api_key", "")),
                temperature=float(self._config.get("ai", {}).get("temperature", 0.7)),
                max_tokens=int(self._config.get("ai", {}).get("max_tokens", 2000)),
                context_window=int(self._config.get("ai", {}).get("context_window", 4000))
            ),
            logging=LogConfig(
                level=os.getenv("LOG_LEVEL", self._config.get("logging", {}).get("level", "INFO")),
                format=self._config.get("logging", {}).get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                file_path=os.getenv("LOG_FILE", self._config.get("logging", {}).get("file_path"))
            ),
            data_sources=self._config.get("data_sources", {})
        )

    def _override_from_env(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Override configuration with environment variables"""
        env_prefix = "INSIGHTFLOW_"
        for key in os.environ:
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                config[config_key] = os.environ[key]
        return config

    def get_config(self) -> InsightFlowConfig:
        """Get the current configuration"""
        return self.config

config = Config()