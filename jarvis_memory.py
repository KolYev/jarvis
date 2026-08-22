import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

def _load():
    if not os.path.exists(MEMORY_FILE):
        return {"profile": {}, "facts": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

