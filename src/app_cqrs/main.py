from fastapi import FastAPI, HTTPException
from .db import db, oid
from .models import *
from .commands import *
from .projector import project_ticket
from .queries import list_tickets

app = FastAPI()

@app.post("/tickets")
def create(t: TicketCreate):
    tid = create_ticket(db, t)
    project_ticket(db, tid)
    return {"id": str(tid)}

@app.patch("/tickets/{tid}/status")
def patch_status(tid: str, cmd: UpdateStatus):
    try:
        update_status(db, oid(tid), cmd)
        emit_event(db, "StatusUpdated", {"id": tid})
        project_ticket(db, oid(tid))
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.patch("/tickets/{tid}/note")
def patch_note(tid: str, cmd: AddNote):
    try:
        add_note(db, oid(tid), cmd)
        project_ticket(db, oid(tid))
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.get("/tickets", response_model=list[TicketRead])
def list_all():
    return list_tickets(db)

@app.get("/metrics")
def metrics():
    return {
        "projection_backlog": backlog(db),
        "projection_errors": errors(db)
    }

@app.get("/health")
def health():
    return {"status": "ok"}
