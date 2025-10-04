from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient
from logger import setup_logger

logger = setup_logger(__name__)

class DBDriver:
    def __init__(self, host):
        self.host = host
        self.client: Union[AsyncIOMotorClient, None] = None
    
    async def connect(self):
        self.client = AsyncIOMotorClient(self.host)
        logger.info(f'Connected to MongoDB at {self.host}')
    
    async def close(self):
        if self.client:
            self.client.close()
            logger.info(f'MongoDB connection closed')