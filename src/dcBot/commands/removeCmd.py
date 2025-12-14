import discord
from discord import app_commands
from typing import Callable, List, Dict, Any


def register_remove_command(
    tree: app_commands.CommandTree,
    load_players: Callable[[], List[Dict[str, Any]]],
    save_players: Callable[[List[Dict[str, Any]]], None],
):
    @tree.command(name="remove", description="Remove a player by ID or name")
    @app_commands.describe(
        query="Player ID or nickname to remove (partial match supported)"
    )
    async def remove_player(interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)

        try:
            players = load_players()

            player_to_remove = None
            for p in players:
                if p.get("player_id") == query:
                    player_to_remove = p
                    break

            if not player_to_remove:
                for p in players:
                    if query.lower() in p.get("player_nick", "").lower():
                        player_to_remove = p
                        break

            if not player_to_remove:
                await interaction.followup.send(
                    f"❌ No player found matching `{query}`. Use `/list` to see all players."
                )
                return

            removed_nick = player_to_remove.get("player_nick", "N/A")
            removed_id = player_to_remove.get("player_id", "Unknown")
            players.remove(player_to_remove)
            save_players(players)

            await interaction.followup.send(
                f"✅ Removed player `{removed_id}` ({removed_nick})."
            )

        except Exception as e:
            error_message = f"❌ Error removing player: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in remove command: {e}")
