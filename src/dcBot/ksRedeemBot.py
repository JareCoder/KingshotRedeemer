import json
import os
import discord
from discord import app_commands

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

from dcBot.commands.redeemCmd import register_redeem_command  # noqa: E402


def load_players():
    players_file = os.path.join(DATA_DIR, "players.json")
    with open(players_file, "r", encoding="utf-8") as f:
        return json.load(f)["players"]


def save_players(players):
    players_file = os.path.join(DATA_DIR, "players.json")
    with open(players_file, "w", encoding="utf-8") as f:
        json.dump({"players": players}, f, indent=4)


def init_bot(token: str) -> discord.Client:
    if not token:
        raise ValueError("Discord token cannot be empty")
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    # Register commands
    register_redeem_command(tree, load_players, save_players)
    
    @client.event
    async def on_ready():
        await tree.sync()
        print(f"✅ Logged in as {client.user}")
    
    return client


async def start_bot(token: str):
    client = init_bot(token)
    await client.start(token)
