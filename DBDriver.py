from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from logger import setup_logger
from models import Configuration

logger = setup_logger(__name__)

class DBDriver:
    def __init__(self, host):
        self.host = host
        self.client: Union[AsyncIOMotorClient, None] = None
        self.db: Union[AsyncIOMotorDatabase, None] = None
    
    @property
    def conf_collection(self) -> AsyncIOMotorCollection:
        if self.db is None:
            raise RuntimeError("Database not initialized")
        return self.db.get_collection("configuration")

    
    async def connect(self):
        self.client = AsyncIOMotorClient(self.host)
        self.db = self.client.get_database('ScribeDB')
        await self.conf_collection.create_index('guild_id')
        logger.info(f'Connected to MongoDB at {self.host}')
    
    async def close(self):
        if self.client:
            self.client.close()
            logger.info(f'MongoDB connection closed')
            
    def get_database(self, name: str) -> AsyncIOMotorDatabase:
        if self.client is None:
            raise RuntimeError("MongoDB client not initialized")
        return self.client.get_database(name)
    
    
    # Configuration CRUD        
    async def create_configuration(self, configuration: Configuration):
        await self.conf_collection.insert_one(configuration.model_dump())