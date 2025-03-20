import pytest
from app.data.processors import DataProcessor
from app.models.schema import DataSource, SourceType

@pytest.fixture
def data_processor():
    return DataProcessor()

@pytest.fixture
def sample_source():
    return DataSource(
        name="test_source",
        type=SourceType.STREAM,
        config={},
        schema={
            "timestamp": "datetime",
            "value": "float"
        }
    )

async def test_process_stream_data(data_processor, sample_source):
    data = {
        "timestamp": "2024-01-01T00:00:00",
        "value": 42.0
    }
    
    processed_data = await data_processor.process_data(data, sample_source)
    assert processed_data["value"] == 42.0

async def test_invalid_data(data_processor, sample_source):
    invalid_data = {
        "timestamp": "2024-01-01T00:00:00"
        # Missing required 'value' field
    }
    
    with pytest.raises(ValueError):
        await data_processor.process_data(invalid_data, sample_source)