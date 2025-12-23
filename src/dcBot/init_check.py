import os
from dcBot.data_handler import BOT_DATA_FILE, save_bot_data


def ensure_bot_data_json_exists() -> None:
    if not os.path.exists(BOT_DATA_FILE):
        print(f"📝 Creating {BOT_DATA_FILE}...")
        default_data = {"players": [], "botConfig": {}}
        save_bot_data(default_data)
        print(f"✅ Created {BOT_DATA_FILE} with default structure.")
    else:
        print("✅ Found bot data file!")
