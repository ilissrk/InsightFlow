# InsightFlow

InsightFlow is an advanced analytics platform that combines real-time data processing with AI-powered insights using the Model Context Protocol (MCP). It provides seamless integration with Claude AI for intelligent data analysis and decision support.

## 🚀 Features

- **MCP Integration**: Full support for Model Context Protocol, enabling advanced AI capabilities
- **Real-time Analytics**: Process and analyze data streams in real-time
- **AI-Powered Insights**: Leverage Claude AI for intelligent data interpretation
- **Flexible Data Processing**: Support for multiple data sources and formats
- **RESTful & WebSocket APIs**: Comprehensive API support for various integration needs

## 🛠️ Technology Stack

- **Backend**: Python 3.9+, FastAPI
- **AI Integration**: Anthropic Claude API
- **Data Processing**: Pandas, NumPy
- **Database**: SQLAlchemy (supports multiple databases)
- **API**: REST + WebSocket
- **Protocol**: Model Context Protocol (MCP)

## 📋 Prerequisites

- Python 3.9 or higher
- Anthropic API key
- Redis (for caching and message queuing)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/insightflow.git
cd insightflow
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your settings
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🚀 Quick Start

### Running Locally

1. Start the server:
```bash
python app/main.py
```

2. Access the API documentation:
```
http://localhost:8000/docs
```


## 📚 API Documentation

### REST API Endpoints

- `GET /tools` - List available MCP tools
- `POST /tool/{tool_name}` - Execute specific tool
- `WS /ws` - WebSocket endpoint for real-time communication

### MCP Tools

1. **Data Analysis**
   - Analyze datasets with configurable metrics
   - Generate statistical insights
   - Support for time-series analysis

2. **Query Data**
   - Flexible data querying capabilities
   - Filter and aggregate data
   - Export results in multiple formats

3. **Generate Insight**
   - AI-powered data interpretation
   - Trend identification
   - Anomaly detection

## 🔧 Configuration

The system can be configured through `config.yaml` or environment variables:

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false

mcp:
  enabled: true
  websocket_path: "/ws"
  max_connections: 100

ai:
  model_name: "claude-2"
  temperature: 0.7
  max_tokens: 2000
```

## 🔍 Development

### Project Structure
```
insightflow/
├── app/
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration management
│   ├── core/             # Core MCP and server logic
│   ├── data/             # Data processing modules
│   ├── analytics/        # Analytics engine
│   ├── ai/               # AI integration
│   ├── api/              # API endpoints
│   └── models/           # Data models
└── requirements.txt      # Python dependencies
```

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions, please open an issue in the GitHub repository or contact the maintainers.

## 🙏 Acknowledgments

- Anthropic for Claude AI integration
- Model Context Protocol community
- All contributors and users of InsightFlow

---

Made with ❤️ by the Ilias RAFIK ;