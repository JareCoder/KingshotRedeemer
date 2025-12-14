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
            player_ids = load_players()
            results = await redeem_giftcode_for_all_players(player_ids, gift_code)
            failed = 0
            
            # Discord message
            failed_players = []
            for item in results:
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
