import json
import os
from datetime import datetime

DB_PATH = "database/reservations.json"

def init_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({"reservations": []}, f, indent=4)

def get_reservations():
    init_db()
    with open(DB_PATH, 'r') as f:
        return json.load(f)["reservations"]

def save_reservation(data):
    init_db()
    with open(DB_PATH, 'r+') as f:
        db_data = json.load(f)
        data["id"] = len(db_data["reservations"]) + 1
        data["date_creation"] = datetime.now().isoformat()
        db_data["reservations"].append(data)
        f.seek(0)
        json.dump(db_data, f, indent=4)
        f.truncate()