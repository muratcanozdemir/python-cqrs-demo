"""
Replay script: rebuild the read model from the command collection.
Intended to be run after deployment or as a maintenance task.
"""

from pymongo import MongoClient
from datetime import datetime
from src.db import get_db, str_to_oid, oid_to_str
from src.commands import project_ticket

import sys

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "cqrs_demo"

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    commands_col = db["tickets_commands"]
    reads_col = db["tickets_reads"]

    # Clear read collection
    reads_col.delete_many({})

    # Rebuild projections from commands
    for ticket in commands_col.find():
        ticket_id = ticket["_id"]
        try:
            project_ticket(db, ticket_id)
            print(f"Projected ticket {oid_to_str(ticket_id)}")
        except Exception as e:
            print(f"Failed projecting {oid_to_str(ticket_id)}: {e}", file=sys.stderr)

    print("Replay complete.")

if __name__ == "__main__":
    main()
