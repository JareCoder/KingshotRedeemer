import discord
from discord import app_commands
from typing import Callable, Dict, Any

def register_setup_command(
    tree: app_commands.CommandTree,
    save_bot_data: Callable[[Dict[str, Any]], None],
    bot_data: Dict[str, Any],
):
    @tree.command(name="setup", description="Set up the bot's channel and admin role.")
    @app_commands.describe(
        channel="The channel where the bot should respond.",
        admin_role="The role required for admin commands.",
    )
    async def setup(
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        admin_role: discord.Role,
    ):
        await interaction.response.defer(thinking=True)
        try:
            if "botConfig" not in bot_data:
                bot_data["botConfig"] = {}

            bot_data["botConfig"]["allowed_channel"] = channel.id
            bot_data["botConfig"]["admin_role"] = admin_role.id
            save_bot_data(bot_data)

            await interaction.followup.send(
                f"✅ Bot configured successfully!\n"
                f"- Allowed Channel: {channel.mention}\n"
                f"- Admin Role: {admin_role.mention}"
            )
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred during setup: {e}")
