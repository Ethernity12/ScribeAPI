import os
from fastapi import FastAPI
from DBDriver import DBDriver
from contextlib import asynccontextmanager
from dotenv import dotenv_values


config = {
    **dotenv_values(".env"),
    **os.environ,  
}

db_driver = DBDriver(
    host=config.get('HOST', 'mongodb://localhost:27017')
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_driver.connect()
    yield
    await db_driver.close()
    
    
app = FastAPI(lifespan=lifespan)

