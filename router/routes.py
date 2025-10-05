from fastapi import APIRouter, Request
from models import Configuration
from DBDriver import DBDriver

router = APIRouter()

@router.post("/create_configuration")
async def create_configuration(request: Request):
    db_driver: DBDriver = request.app.state.db_driver
    await db_driver.create_configuration()
    
    