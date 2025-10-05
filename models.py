from typing import List
from pydantic import BaseModel

class Configuration(BaseModel):
    guild_id: int
    ticket_channel: int
    questionnaire_channel: int
    consideration_channel: int
    moderator_roles: List[int]
    administrator_roles: List[int]