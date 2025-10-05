from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from logger import setup_logger
from models import Configuration

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
            
    def get_database(self, name: str) -> AsyncIOMotorDatabase:
        if not self.client:
            raise RuntimeError("MongoDB client not initialized")
        return self.client.get_database(name)
            
    async def create_configuration(self):
        db = self.get_database('11111111')
        collection = db.get_collection('configuration')
        await collection.insert_one({'test': 'test'})