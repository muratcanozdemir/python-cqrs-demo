from fastapi import FastAPI, HTTPException
from bson import ObjectId
from datetime import datetime
from .db import tickets
from .models import *

app = FastAPI()

def preview(msg: str, n=50):
    return msg[:n] + ("..." if len(msg) > n else "")

@app.post("/tickets")
def create(t: TicketCreate):
    doc = {
        "subject": t.subject,
        "message": t.message,
        "status": "open",
        "agent_note": None,
        "updated_at": datetime.utcnow()
    }
    res = tickets.insert_one(doc)
    return {"id": str(res.inserted_id)}

@app.patch("/tickets/{tid}")
def update(tid: str, u: TicketUpdate):
    t = tickets.find_one({"_id": ObjectId(tid)})
    if not t:
        raise HTTPException(404)

    if t["status"] == "closed":
        raise HTTPException(400, "cannot reopen")

    updates = {}
    if u.status:
        updates["status"] = u.status
    if u.agent_note:
        updates["agent_note"] = u.agent_note

    updates["updated_at"] = datetime.utcnow()

    tickets.update_one({"_id": ObjectId(tid)}, {"$set": updates})
    return {"ok": True}

@app.get("/tickets")
def list_tickets():
    out = []
    for t in tickets.find():
        out.append({
            "id": str(t["_id"]),
            "subject": t["subject"],
            "status": t["status"],
            "preview": preview(t["message"]),
            "has_note": bool(t["agent_note"])
        })
    return out

@app.get("/health")
def health():
    return {"status": "ok"}
