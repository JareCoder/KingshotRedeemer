import json
import os
import discord
from discord import app_commands

from dcBot.commands.redeemCmd import register_redeem_command  # noqa: E402
from dcBot.commands.listCmd import register_list_command  # noqa: E402
from dcBot.commands.addCmd import register_add_command  # noqa: E402
from dcBot.commands.removeCmd import register_remove_command  # noqa: E402
from dcBot.commands.findCmd import register_find_command  # noqa: E402
from dcBot.commands.helpCmd import register_help_command  # noqa: E402
from dcBot.commands.setupCmd import register_setup_command
from config.config import load_bot_data, save_bot_data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))




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

    bot_data = load_bot_data()

    # Register commands
    register_redeem_command(tree, load_players, save_players, bot_data)
    register_list_command(tree, load_players)
    register_add_command(tree, load_players, save_players, bot_data)
    register_remove_command(tree, load_players, save_players, bot_data)
    register_find_command(tree, load_players)
    register_help_command(tree)
    register_setup_command(tree, save_bot_data, bot_data)
    
    @client.event
    async def on_ready():
        await tree.sync()
        print(f"✅ Logged in as {client.user}")
    
    return client


async def start_bot(token: str):
    client = init_bot(token)
    await client.start(token)
