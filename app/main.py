import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .config import config
from .core.mcp_server import MCPServer
from .core.message_handler import MessageHandler
from .core.client_manager import ClientManager
from .data.processors import DataProcessor
from .data.ingestion import DataSourceAdapter
from .data.storage import DataStorage
from .analytics.engine import AnalyticsEngine
from .analytics.insights import InsightGenerator
from .ai.claude_connector import ClaudeConnector
from .ai.nlp_processor import NLPProcessor
from .api.rest import RestAPI

# Configure logging
logging.basicConfig(
    level=config.get_config().logging.level,
    format=config.get_config().logging.format,
    filename=config.get_config().logging.file_path
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize components
    try:
        # Core components
        mcp_server = MCPServer()
        message_handler = MessageHandler()
        client_manager = ClientManager()

        # Data components
        data_processor = DataProcessor()
        data_storage = DataStorage(None)  # Initialize with appropriate backend

        # Analytics components
        analytics_engine = AnalyticsEngine()
        insight_generator = InsightGenerator()

        # AI components
        claude_connector = ClaudeConnector()
        nlp_processor = NLPProcessor()

        # Initialize MCP server
        await mcp_server.initialize()

        # Store components in app state
        app.state.mcp_server = mcp_server
        app.state.message_handler = message_handler
        app.state.client_manager = client_manager
        app.state.data_processor = data_processor
        app.state.analytics_engine = analytics_engine
        app.state.claude_connector = claude_connector

        logger.info("InsightFlow initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        raise
    finally:
        # Cleanup
        await mcp_server.shutdown()
        logger.info("InsightFlow shutdown complete")

# Initialize FastAPI application
app = FastAPI(
    title="InsightFlow",
    description="AI-powered data analytics and insights platform",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize REST API
rest_api = RestAPI(
    mcp_server=app.state.mcp_server,
    data_processor=app.state.data_processor,
    ai_connector=app.state.claude_connector
)

# Include REST API routes
app.include_router(rest_api.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config.get_config().server.host,
        port=config.get_config().server.port,
        reload=config.get_config().server.debug,
        workers=config.get_config().server.workers
    )