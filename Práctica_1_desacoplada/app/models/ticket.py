from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, date
import uuid

class Ticket(BaseModel):
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = Field(..., min_length=9, max_length=9)
    event_name: str = "University Fin de Año"
    client_name: str = Field(..., min_length=1, max_length=64)
    ticket_type: Literal['NORMAL', 'VIP', 'SUPERVIP'] = 'NORMAL'
    comments: Optional[str] = None
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    event_date: date = date(2026, 1, 1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "12345678K",
                "client_name": "Dylan",
                "ticket_type": "SUPERVIP",
                "comments": "+18 ticket"
            }
        }

    def update_timestamp(self):
        self.purchase_date = datetime.utcnow()
