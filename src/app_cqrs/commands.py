from datetime import datetime

d
def create_ticket(db, t):
    doc = {
        "subject": t.subject,
        "message": t.message,
        "status": "open",
        "agent_note": None,
        "version": 1,
        "updated_at": datetime.utcnow()
    }
    emit_event(db, "TicketCreated", tid)
    return db.commands.insert_one(doc).inserted_id

def update_status(db, tid, cmd):
    t = db.commands.find_one({"_id": tid})
    if not t:
        raise ValueError("not found")
    if t["status"] == "closed":
        raise ValueError("cannot reopen")

    db.commands.update_one(
        {"_id": tid},
        {"$set": {
            "status": cmd.status,
            "updated_at": datetime.utcnow()
        },
         "$inc": {"version": 1}}
    )
    emit_event(db, "StatusUpdated", tid)


def add_note(db, tid, cmd):
    t = db.commands.find_one({"_id": tid})
    if not t:
        raise ValueError("not found")
    if t["status"] == "closed":
        raise ValueError("cannot reopen")

    db.commands.update_one(
        {"_id": tid},
        {"$set": {
            "status": cmd.status,
            "updated_at": datetime.utcnow()
        },
         "$inc": {"version": 1}}
    )
    emit_event(db, "NoteAdded", tid)

def emit_event(db, type_, tid):
    db.events.insert_one({
        "type": type_,
        "ticket_id": tid,
        "processed": False,
        "attempts": 0,
        "error": None
    })