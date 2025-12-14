import json
import os
import discord
from discord import app_commands

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

from browser_automation.redeem import redeem_giftcode_for_all_players  # noqa: E402


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
    
    @client.event
    async def on_ready():
        await tree.sync()
        print(f"✅ Logged in as {client.user}")
    
    @tree.command(name="redeem", description="Redeem a Kingshot gift code for all players")
    @app_commands.describe(gift_code="The gift code to redeem")
    async def redeem(interaction: discord.Interaction, gift_code: str):
        await interaction.response.defer(thinking=True)
        
        try:
            players = load_players()
            results = await redeem_giftcode_for_all_players(players, gift_code)
            failed = 0
            updated = False
            
            # Discord message
            failed_players = []
            for idx, item in enumerate(results):
                # We want to keep track of names for human readability
                page_nick = item.get("page_player_nick")
                stored_nick = item.get("stored_player_nick")
                if page_nick and stored_nick != page_nick:
                    players[idx]["player_nick"] = page_nick
                    updated = True

                success = item.get("success")
                if success:
                    continue
                
                result = item.get("result", {})
                player_id = item.get("player_id", "Unknown")
                player_nick = result.get("player_nick", "N/A")
                message = result.get("message", "No message")
                failed += 1

                failed_players.append(f"❌ `{player_id}` ({player_nick}): {message}")
            
            response_message = f"🎁 **Redeem Results for `{gift_code}`**\n📋`{len(results) - failed}/{len(results)}` succeeded!\n\n"
            response_message += "\n".join(failed_players)
            if updated:
                save_players(players)
                response_message += "\n\n💾 Updated player names from page"
            
            # Discord message limit safety
            if len(response_message) > 1900:
                response_message = response_message[:1900] + "\n…(truncated)"
            
            await interaction.followup.send(response_message)
            
        except Exception as e:
            error_message = f"❌ Error during redemption: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in redeem command: {e}")
    
    return client


async def start_bot(token: str):
    client = init_bot(token)
    await client.start(token)
