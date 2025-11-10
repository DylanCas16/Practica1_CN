from pydantic import BaseModel, Field
from typing import Optional, Literal
import uuid

class Ticket(BaseModel):
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = Field(..., min_length=6, max_length=10)
    event_name: Optional[str] = "University Fin de Año"
    client_name: str = Field(..., min_length=1, max_length=64)
    ticket_type: Literal['NORMAL', 'VIP', 'SUPERVIP'] = 'NORMAL'
    comments: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "12345678K",
                "client_name": "Dylan",
                "ticket_type": "SUPERVIP",
                "comments": "+18 ticket"
            }
        }
