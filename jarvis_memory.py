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

def get_profile_text():
    """Возвращает профиль пользователя как текст"""
    data = _load()
    profile = data.get("profile", {})
    if not profile:
        return "О пользователе пока ничего неизвестно"
    lines = [f"- {k}: {v}" for k, v in profile.items()]
    return "\n".join(lines)

def update_profile(key, value):
    "Обновляет или добавляет факт о пользователе"
    data = _load()
    data["profile"][key] = value
    _save(data)
    return f"Запомнил: {key} = {value}"

def remember_fact(fact):
    """Сохраняет факт или вывод с меткой времени"""
    data = _load()
    data["facts"].append({"text": fact, "date": datetime.now().isoformat()})
    _save(data)
    return f"Запомнил: {fact}"