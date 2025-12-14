import discord
from discord import app_commands
from typing import Callable, List, Dict, Any


class PlayerListView(discord.ui.View):
    def __init__(self, players: List[Dict[str, Any]], page: int = 0):
        super().__init__(timeout=180)
        self.players = players
        self.page = page
        self.per_page = 10
        self.max_page = max(0, (len(players) - 1) // self.per_page)
        self._update_buttons()

    def _update_buttons(self):
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page >= self.max_page

    def get_embed(self) -> discord.Embed:
        start_idx = self.page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.players))
        page_players = self.players[start_idx:end_idx]

        embed = discord.Embed(
            title="📋 Registered Players",
            description=f"Showing players {start_idx + 1}-{end_idx} of {len(self.players)}",
            color=discord.Color.blue(),
        )

        for player in page_players:
            player_id = player.get("player_id", "Unknown")
            player_nick = player.get("player_nick", "N/A")
            embed.add_field(
                name=f"{player_nick}",
                value=f"ID: `{player_id}`",
                inline=False,
            )

        embed.set_footer(text=f"Page {self.page + 1}/{self.max_page + 1}")
        return embed

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.primary)
    async def previous_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.page = max(0, self.page - 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.primary)
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.page = min(self.max_page, self.page + 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


def register_list_command(
    tree: app_commands.CommandTree,
    load_players: Callable[[], List[Dict[str, Any]]],
):

    @tree.command(name="list", description="List all registered players")
    async def list_players(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        try:
            players = load_players()

            if not players:
                await interaction.followup.send("❌ No players registered.")
                return

            view = PlayerListView(players)
            await interaction.followup.send(embed=view.get_embed(), view=view)

        except Exception as e:
            error_message = f"❌ Error loading players: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in list command: {e}")
