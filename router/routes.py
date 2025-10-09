from fastapi import APIRouter, Request, Response, HTTPException
from models import Configuration, DeleteConfiguration, UpdateConfiguration
from DBDriver import DBDriver

router = APIRouter()

@router.post("/create_configuration")
async def create_configuration(request: Request, configuration: Configuration):
    db_driver: DBDriver = request.app.state.db_driver
    result = await db_driver.create_configuration(configuration)
    if result is False:
        raise HTTPException(status_code=409, detail="Configuration already exists")
    return Response(status_code=201)
        
@router.get("/search_configuration", response_model=Configuration)
async def search_configuration(request: Request, guild_id: int):
    db_driver: DBDriver = request.app.state.db_driver
    result = await db_driver.search_configuration(guild_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return result

    
@router.post("/update_configuration")
async def update_configuration(request: Request, update_configuration: UpdateConfiguration):
    db_driver: DBDriver = request.app.state.db_driver
    result = await db_driver.update_configuration(update_configuration)
    if result is False:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return Response(status_code=202)
    
@router.post("/delete_configuration")
async def delete_configuration(request: Request, delete_config: DeleteConfiguration):
    db_driver: DBDriver = request.app.state.db_driver
    result = await db_driver.delete_configuration(delete_config.guild_id)
    if not result:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return Response(status_code=204)