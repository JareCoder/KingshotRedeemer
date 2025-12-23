import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..", "..")))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "data"))
BOT_DATA_FILE = os.path.join(DATA_DIR, "botData.json")


def load_bot_data():
    if not os.path.exists(BOT_DATA_FILE):
        return {}
    try:
        with open(BOT_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_bot_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(BOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
