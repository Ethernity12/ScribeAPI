from fastapi import APIRouter, Request
from models import Configuration, UpdateConfiguration
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
    
@router.post("/update_configuration")
async def update_configuration(request: Request, update_configuration: UpdateConfiguration):
    db_driver: DBDriver = request.app.state.db_driver
    await db_driver.update_configuration(update_configuration)