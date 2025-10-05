import os
from fastapi import FastAPI
from DBDriver import DBDriver
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from router.routes import router


config = {
    **dotenv_values(".env"),
    **os.environ,  
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_driver = DBDriver(host=config.get('HOST', 'mongodb://localhost:27017'))
    await app.state.db_driver.connect()
    yield
    await app.state.db_driver.close()
    
    
app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1")