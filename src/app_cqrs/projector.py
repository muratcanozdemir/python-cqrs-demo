def preview(msg: str, n=50):
    return msg[:n] + ("..." if len(msg) > n else "")

SCHEMA_VERSION = 1

def project_ticket(db, tid):
    t = db.commands.find_one({"_id": tid})
    if not t:
        return

    existing = db.reads.find_one({"_id": tid})
    if existing and existing.get("version", 0) >= t["version"]:
        return  # stale event, ignore

    read_doc = {
        "_id": tid,
        "subject": t["subject"],
        "status": t["status"],
        "updated_at": t["updated_at"],
        "preview": preview(t["message"]),
        "has_note": bool(t["agent_note"]),
        "version": t["version"],
        "schema_version": SCHEMA_VERSION
    }

    db.reads.replace_one({"_id": tid}, read_doc, upsert=True)
