import logging
from typing import Dict, Any, List
import pandas as pd
from .storage import DataStorage
from ..models.schema import DataSource

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.storage = DataStorage()
        self._processors = {}
        self._initialize_processors()

    def _initialize_processors(self):
        """Initialize default data processors"""
        self._processors = {
            "stream": self._process_stream_data,
            "batch": self._process_batch_data,
            "api": self._process_api_data
        }

    async def process_data(self, data: Any, source: DataSource) -> Dict[str, Any]:
        """Process incoming data based on source type"""
        try:
            processor = self._processors.get(source.type)
            if not processor:
                raise ValueError(f"No processor found for source type: {source.type}")

            processed_data = await processor(data, source)
            await self.storage.store(processed_data, source)
            return processed_data

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise

    async def _process_stream_data(self, data: Dict[str, Any], source: DataSource) -> Dict[str, Any]:
        """Process streaming data"""
        # Validate against schema
        self._validate_data(data, source.schema)
        
        # Transform data
        transformed_data = self._transform_data(data, source)
        
        return transformed_data

    async def _process_batch_data(self, data: List[Dict[str, Any]], source: DataSource) -> List[Dict[str, Any]]:
        """Process batch data"""
        processed_batch = []
        for item in data:
            self._validate_data(item, source.schema)
            processed_item = self._transform_data(item, source)
            processed_batch.append(processed_item)
        
        return processed_batch

    def _validate_data(self, data: Dict[str, Any], schema: Dict[str, Any]):
        """Validate data against schema"""
        for field, field_type in schema.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            # Add type validation logic here

    def _transform_data(self, data: Dict[str, Any], source: DataSource) -> Dict[str, Any]:
        """Transform data according to source configuration"""
        # Add transformation logic here
        return data
