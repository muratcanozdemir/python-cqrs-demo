import time
from db import db
from projector import project_ticket

MAX_ATTEMPTS = 5

while True:
    evt = db.events.find_one_and_update(
        {
            "processed": False,
            "attempts": {"$lt": MAX_ATTEMPTS}
        },
        {
            "$inc": {"attempts": 1}
        }
    )

    if not evt:
        time.sleep(0.2)
        continue

    try:
        project_ticket(db, evt["ticket_id"])
        db.events.update_one(
            {"_id": evt["_id"]},
            {"$set": {"processed": True}}
        )
    except Exception as e:
        db.events.update_one(
            {"_id": evt["_id"]},
            {"$set": {"error": str(e)}}
        )
