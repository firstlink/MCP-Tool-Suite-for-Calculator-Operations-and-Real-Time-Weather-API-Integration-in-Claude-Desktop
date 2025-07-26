from typing import Any
import httpx
import json
import asyncio
from aiohttp import web, ClientSession
import aiohttp_cors
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-mcp-http/1.0"

class WeatherMCPServer:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        self.setup_cors()
        
    def setup_cors(self):
        """Setup CORS for cross-origin requests"""
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*", 
                allow_headers="*",
                allow_methods="*"
            )
        })
        for route in list(self.app.router.routes()):
            cors.add(route)
    
    def setup_routes(self):
        """Setup HTTP routes for M