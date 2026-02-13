# consistency.py

READ_LAG_MS = 500  # SLA

def assert_fresh(db, tid):
    from datetime import datetime
    t = db.reads.find_one({"_id": tid})
    if not t:
        return False
    lag = (datetime.utcnow() - t["updated_at"]).total_seconds() * 1000
    return lag < READ_LAG_MS
