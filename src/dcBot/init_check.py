import os

from dcBot.data_handler import BOT_DATA_FILE, save_bot_data
from dcBot.migration import migrate_legacy_players_file


def ensure_bot_data_json_exists() -> None:
    migrated = migrate_legacy_players_file()

    if not os.path.exists(BOT_DATA_FILE):
        print(f"📝 Creating {BOT_DATA_FILE}...")
        default_data = {"botConfig": {}, "players": []}
        save_bot_data(default_data)
        print("✅ Created {BOT_DATA_FILE} with default structure.")
    elif not migrated:
        print("✅ Found bot data file!")
