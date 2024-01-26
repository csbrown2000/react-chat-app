import json
from datetime import date
from uuid import uuid4

# Open 'db' and begin reading the json file
with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)
    
