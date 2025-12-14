import discord
from discord import app_commands
from typing import Callable, List, Dict, Any


def register_find_command(
    tree: app_commands.CommandTree,
    load_players: Callable[[], List[Dict[str, Any]]],
):
    @tree.command(name="find", description="Find a player by ID or nickname")
    @app_commands.describe(query="Player ID or nickname (partial match supported)")
    async def find_player(interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)

        try:
            players = load_players()
            query_lower = query.lower()

            matches: List[Dict[str, Any]] = [
                p for p in players if p.get("player_id") == query
            ]

            if not matches:
                matches = [
                    p for p in players if query_lower in p.get("player_nick", "").lower()
                ]

            if not matches:
                await interaction.followup.send(
                    f"❌ No player found matching `{query}`. Try `/list` to see all players."
                )
                return

            embed = discord.Embed(
                title="🔎 Player Search Results",
                description=f"Query: `{query}`",
                color=discord.Color.green(),
            )

            for p in matches[:10]:
                player_id = p.get("player_id", "Unknown")
                player_nick = p.get("player_nick", "N/A")
                embed.add_field(
                    name=player_nick,
                    value=f"ID: `{player_id}`",
                    inline=False,
                )

            if len(matches) > 10:
                embed.set_footer(text=f"Showing 10 of {len(matches)} results")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            error_message = f"❌ Error finding player: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in find command: {e}")
