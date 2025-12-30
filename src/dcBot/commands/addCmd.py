import discord
from discord import app_commands
from typing import Callable, Dict, Any

from dcBot.permissions import check_permissions


def register_add_command(
    tree: app_commands.CommandTree,
    bot_data: Dict[str, Any],
    save_bot_data: Callable[[Dict[str, Any]], None],
):
    @tree.command(name="add", description="Add a new player by ID")
    @app_commands.describe(player_id="The player ID to add")
    async def add_player(interaction: discord.Interaction, player_id: str):
        
        permission_error = check_permissions(interaction, bot_data)
        if permission_error:
            await interaction.response.send_message(permission_error, ephemeral=True)
            return
        
        await interaction.response.defer(thinking=True)

        try:
            players = bot_data.get("players", [])

            existing = next(
                (p for p in players if p.get("player_id") == player_id), None
            )
            if existing:
                await interaction.followup.send(
                    f"❌ Player with ID `{player_id}` already exists as `{existing.get('player_nick', 'N/A')}`."
                )
                return

            new_player = {"player_id": player_id, "player_nick": f"Player {player_id}"}
            players.append(new_player)
            bot_data["players"] = players
            save_bot_data(bot_data)

            await interaction.followup.send(
                f"✅ Added player `{player_id}` with placeholder nick `Player {player_id}`.\n"
                f"💡 The nick will be updated when they redeem a code."
            )

        except Exception as e:
            error_message = f"❌ Error adding player: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in add command: {e}")