from typing import List, Optional
from pydantic import BaseModel

class Configuration(BaseModel):
    guild_id: int
    ticket_channel: int
    questionnaire_channel: int
    consideration_channel: int
    moderator_roles: List[int]
    administrator_roles: List[int]
    
class UpdateConfiguration(BaseModel):
    guild_id: int
    ticket_channel: Optional[int] = None
    questionnaire_channel: Optional[int] = None
    consideration_channel: Optional[int] = None
    moderator_roles: Optional[List[int]] = None
    administrator_roles: Optional[List[int]] = None