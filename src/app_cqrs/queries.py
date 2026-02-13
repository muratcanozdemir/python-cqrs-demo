def list_tickets(db):
    return [
        {
            "id": str(t["_id"]),
            "subject": t["subject"],
            "status": t["status"],
            "updated_at": t["updated_at"],
            "preview": t["preview"],
            "has_note": t["has_note"]
        }
        for t in db.reads.find().sort("updated_at", -1)
    ]
