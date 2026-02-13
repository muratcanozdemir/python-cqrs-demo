from db import db
from projector import project_ticket

db.reads.delete_many({})
for t in db.commands.find():
    project_ticket(db, t["_id"])
