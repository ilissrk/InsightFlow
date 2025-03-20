import logging
from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine
from ..config import config

logger = logging.getLogger(__name__)

class DataStorage:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or config.get_config().database.url
        self.engine = create_engine(self.connection_string)
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize storage backend"""
        try:
            # Create necessary tables
            with self.engine.connect() as conn:
                # Add table creation logic here
                pass
        except Exception as e:
            logger.error(f"Error initializing storage: {str(e)}")
            raise

    async def store(self, data: Dict[str, Any], source_id: str) -> bool:
        """Store processed data"""
        try:
            df = pd.DataFrame([data])
            table_name = f"data_{source_id}"
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            return True
        except Exception as e:
            logger.error(f"Error storing data: {str(e)}")
            raise

    async def query(self, query: str, params: Dict[str, Any] = None) -> pd.DataFrame:
        """Query stored data"""
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error querying data: {str(e)}")
            raise

    async def get_latest(self, source_id: str, limit: int = 100) -> pd.DataFrame:
        """Get latest records for a source"""
        query = f"""
        SELECT * FROM data_{source_id}
        ORDER BY timestamp DESC
        LIMIT {limit}
        """
        return await self.query(query)
