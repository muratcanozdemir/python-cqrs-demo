from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class TicketCreate(BaseModel):
    subject: str
    message: str

class TicketUpdate(BaseModel):
    status: Optional[Literal["open", "triaged", "closed"]] = None
    agent_note: Optional[str] = None

class Ticket(BaseModel):
    id: str
    subject: str
    status: str
    message: str
    agent_note: Optional[str]
    updated_at: datetime
