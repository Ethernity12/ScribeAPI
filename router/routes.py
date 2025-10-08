from fastapi import APIRouter, Request
from models import Configuration
from DBDriver import DBDriver

router = APIRouter()

@router.post("/create_configuration")
async def create_configuration(request: Request, configuration: Configuration):
    db_driver: DBDriver = request.app.state.db_driver
    await db_driver.create_configuration(configuration)
    
@router.get("/search_configuration", response_model=Configuration)
async def search_configuration(request: Request, guild_id: int):
    db_driver: DBDriver = request.app.state.db_driver
    return await db_driver.search_configuration(guild_id)
    
    