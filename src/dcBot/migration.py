import json
import os
from typing import Dict, List, Tuple

from dcBot.data_handler import load_bot_data, save_bot_data

LEGACY_PLAYERS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "players.json")
)


def _read_legacy_players() -> List[Dict[str, object]]:
    players: List[Dict[str, object]] = []
    try:
        with open(LEGACY_PLAYERS_FILE, "r", encoding="utf-8") as legacy_file:
            legacy_payload = json.load(legacy_file)
            if isinstance(legacy_payload, dict):
                legacy_players = legacy_payload.get("players", []) or []
            elif isinstance(legacy_payload, list):
                legacy_players = legacy_payload
            else:
                legacy_players = []

            for player in legacy_players:
                if isinstance(player, dict):
                    players.append(player)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"⚠️  Failed to read legacy players file: {exc}. Continuing with empty list.")

    return players


def _player_key(player: Dict[str, object]) -> Tuple[str, str]:
    player_id = str(player.get("player_id")) if player.get("player_id") else ""
    if player_id:
        return ("id", player_id)

    player_nick = str(player.get("player_nick")) if player.get("player_nick") else ""
    if player_nick:
        return ("nick", player_nick.lower())

    return ("raw", json.dumps(player, sort_keys=True, default=str))


def migrate_legacy_players_file() -> bool:
    if not os.path.exists(LEGACY_PLAYERS_FILE):
        return False

    print(f"🔁 Legacy players file detected at {LEGACY_PLAYERS_FILE}. Migrating...")

    legacy_players = _read_legacy_players()

    bot_data = load_bot_data()
    bot_data.setdefault("botConfig", {})

    existing_players = bot_data.get("players", [])
    if not isinstance(existing_players, list):
        existing_players = []

    merged_players: Dict[Tuple[str, str], Dict[str, object]] = {}

    for player in existing_players:
        if isinstance(player, dict):
            merged_players[_player_key(player)] = player

    added_count = 0
    for legacy_player in legacy_players:
        key = _player_key(legacy_player)
        if key not in merged_players:
            merged_players[key] = legacy_player
            added_count += 1

    bot_data["players"] = list(merged_players.values())
    save_bot_data(bot_data)

    if added_count:
        print(f"✅ Migration complete. Added {added_count} player(s) from legacy data into botData.json.")
    else:
        print("ℹ️  Migration complete. No new players were added because they already existed.")

    try:
        os.remove(LEGACY_PLAYERS_FILE)
    except OSError as exc:
        print(f"⚠️  Could not delete legacy players file: {exc}")

    legacy_dir = os.path.dirname(LEGACY_PLAYERS_FILE)
    try:
        os.rmdir(legacy_dir)
    except OSError:
        pass

    return True
