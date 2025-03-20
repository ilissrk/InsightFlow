# InsightFlow API Documentation

## REST API Endpoints

### Data Sources

#### List Sources
```http
GET /sources
```

Returns a list of all configured data sources.

#### Create Source
```http
POST /sources
```

Create a new data source configuration.

Request body:
```json
{
    "name": "example_source",
    "type": "stream",
    "config": {
        "url": "ws://example.com/stream"
    },
    "schema": {
        "timestamp": "datetime",
        "value": "float"
    }
}
```

### Analytics

#### Get Analytics
```http
GET /analytics/{source_id}?metrics=count,average&start_time=2024-01-01T00:00:00
```

Get analytics results for a specific data source.

#### Get Insights
```http
GET /insights/{source_id}
```

Get AI-generated insights for a data source.

### Custom Queries

#### Execute Query
```http
POST /query
```

Execute a custom SQL query against the data storage.

Request body:
```json
{
    "sql": "SELECT * FROM data_source_1 WHERE value > :threshold",
    "params": {
        "threshold": 100
    }
}
```

## WebSocket API

Connect to the WebSocket endpoint for real-time updates:

```
ws://your-server/ws
```

### Subscribe to Updates

Send a subscription message:
```json
{
    "type": "subscribe",
    "topic": "source_1"
}
```

### Message Format

Incoming messages follow this format:
```json
{
    "type": "update",
    "source": "source_1",
    "data": {
        "timestamp": "2024-01-01T00:00:00",
        "value": 42.0
    }
}
```