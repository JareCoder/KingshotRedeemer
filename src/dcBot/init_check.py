import json
import os


def ensure_players_json_exists(data_dir: str) -> None:
    players_file = os.path.join(data_dir, "players.json")

    if not os.path.exists(players_file):
        print(f"📝 Creating {players_file}...")
        os.makedirs(data_dir, exist_ok=True)
        
        default_data = {"players": []}
        with open(players_file, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        
        print(f"✅ Created {players_file} with empty players list")
    else:
        print("✅ Found players data file!")
