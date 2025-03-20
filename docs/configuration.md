# Configuration Guide

## Server Configuration

The server can be configured through `config.yaml` or environment variables.

### Basic Configuration

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false
  workers: 4
```

### Database Configuration

```yaml
database:
  url: "sqlite:///data.db"
  pool_size: 5
  max_overflow: 10
```

### Analytics Configuration

```yaml
analytics:
  metrics:
    - "count"
    - "average"
    - "sum"
  interval: 60  # seconds
  batch_size: 1000
```

### AI Configuration

```yaml
ai:
  model_name: "claude-2"
  temperature: 0.7
  max_tokens: 2000
```

## Environment Variables

Priority environment variables:

- `INSIGHTFLOW_CONFIG`: Path to config file
- `CLAUDE_API_KEY`: Anthropic API key
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level

## Data Sources

### Stream Source Example

```yaml
data_sources:
  example_stream:
    name: "Example Stream"
    type: "stream"
    config:
      url: "ws://example.com/stream"
      auth_token: ""
    schema:
      timestamp: "datetime"
      value: "float"
```

### Batch Source Example

```yaml
data_sources:
  example_batch:
    name: "Example Batch"
    type: "batch"
    config:
      path: "/data/batch"
      pattern: "*.csv"
    schema:
      timestamp: "datetime"
      value: "float"
```