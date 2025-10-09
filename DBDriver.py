from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from logger import DBOperationLogger, setup_logger
from models import Configuration, UpdateConfiguration

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
        await self.conf_collection.create_index(
            'guild_id',
            unique=True,             
            name='guild_id_idx'   
        )
        logger.info(f'Connected to MongoDB at {self.host}')
    
    async def close(self):
        if self.client:
            self.client.close()
            logger.info(f'MongoDB connection closed')
            
    @DBOperationLogger(logger)
    def get_database(self, name: str) -> AsyncIOMotorDatabase:
        if self.client is None:
            raise RuntimeError("MongoDB client not initialized")
        return self.client.get_database(name)
    
    # Configuration CRUD     
    @DBOperationLogger(logger)   
    async def create_configuration(self, configuration: Configuration):
        await self.conf_collection.insert_one(configuration.model_dump())
        
    @DBOperationLogger(logger)
    async def search_configuration(self, guild_id: int):
        result = await self.conf_collection.find_one({'guild_id': guild_id})
        if result is None:
            return None
        conf = Configuration(**result)
        return conf
    
    @DBOperationLogger(logger)
    async def update_configuration(self, update_data: UpdateConfiguration):
        guild_id = update_data.guild_id
        update_data = update_data.model_dump(exclude={'guild_id'}, exclude_unset=True)
        result = await self.conf_collection.update_one({'guild_id': guild_id}, {'$set': update_data})
        return result.matched_count > 0
    
    @DBOperationLogger(logger)
    async def delete_configuration(self, guild_id: int):
        result = await self.conf_collection.delete_one({'guild_id': guild_id})
        return result.deleted_count > 0
        