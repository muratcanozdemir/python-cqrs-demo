from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class TicketCreate(BaseModel):
    subject: str
    message: str

class UpdateStatus(BaseModel):
    status: Literal["open", "triaged", "closed"]

class AddNote(BaseModel):
    note: str

class TicketRead(BaseModel):
    id: str
    subject: str
    status: str
    updated_at: datetime
    preview: str
    has_note: bool
