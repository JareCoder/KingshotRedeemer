import discord
from discord import app_commands


def register_help_command(tree: app_commands.CommandTree):
    @tree.command(name="help", description="Display all available commands and usage")
    async def help_command(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        try:
            embed = discord.Embed(
                title="📚 Kingshot Redeemer Bot - Help",
                description="Here are all available commands:",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="🎁 /redeem <gift_code>",
                value=(
                    "Redeem a Kingshot gift code for all registered players.\n"
                    "**Example:** `/redeem KSFB15K`\n"
                    "• Automatically redeems for all players\n"
                    "• Updates player nicknames from the game\n"
                    "• Shows success/failure for each player"
                ),
                inline=False,
            )

            embed.add_field(
                name="➕ /add <player_id>",
                value=(
                    "Add a new player to the redemption list.\n"
                    "**Example:** `/add 48666532`\n"
                    "• Checks if player already exists\n"
                    "• Creates placeholder nickname\n"
                    "• Nickname auto-updates on first redemption"
                ),
                inline=False,
            )

            embed.add_field(
                name="➖ /remove <query>",
                value=(
                    "Remove a player by ID or nickname.\n"
                    "**Examples:**\n"
                    "• `/remove 48666532` (exact ID)\n"
                    "• `/remove Jareggie` (partial nickname match)"
                ),
                inline=False,
            )

            embed.add_field(
                name="📋 /list",
                value=(
                    "View all registered players with pagination.\n"
                    "• Shows 10 players per page\n"
                    "• Navigate with ◀️ Previous / Next ▶️ buttons\n"
                    "• Displays player nicknames and IDs"
                ),
                inline=False,
            )

            embed.add_field(
                name="🔎 /find <query>",
                value=(
                    "Search for a specific player by ID or nickname.\n"
                    "**Examples:**\n"
                    "• `/find 48666532` (exact ID)\n"
                    "• `/find Syde` (partial nickname match)\n"
                    "• Shows up to 10 matching results"
                ),
                inline=False,
            )

            embed.add_field(
                name="❓ /help",
                value="Display this help message.",
                inline=False,
            )

            embed.set_footer(
                text="💡 Tip: Player data persists across bot restarts • Nicknames auto-sync from the game"
            )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            error_message = f"❌ Error displaying help: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in help command: {e}")
