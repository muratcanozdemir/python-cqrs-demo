def backlog(db):
    return db.events.count_documents({"processed": False})

def errors(db):
    return db.events.count_documents({
        "processed": False,
        "attempts": {"$gte": 5}
    })
