import discord
from typing import Dict, Any


SETUP_INCOMPLETE_MESSAGE = "Bot setup is not complete. Please use `/setup` to configure the bot."


def ensure_bot_setup(bot_data: Dict[str, Any]) -> str:
    bot_config = bot_data.get("botConfig", {})
    allowed_channel_id = bot_config.get("allowed_channel")
    admin_role_id = bot_config.get("admin_role")

    if not allowed_channel_id or not admin_role_id:
        return SETUP_INCOMPLETE_MESSAGE

    return ""


def check_permissions(interaction: discord.Interaction, bot_data: Dict[str, Any]) -> str:
    setup_error = ensure_bot_setup(bot_data)
    if setup_error:
        return setup_error

    bot_config = bot_data.get("botConfig", {})
    allowed_channel_id = bot_config.get("allowed_channel")
    admin_role_id = bot_config.get("admin_role")

    if interaction.channel.id != allowed_channel_id:
        allowed_channel = interaction.guild.get_channel(allowed_channel_id)
        return f"This command can only be used in {allowed_channel.mention if allowed_channel else 'the configured channel'}."

    admin_role = discord.utils.get(interaction.guild.roles, id=admin_role_id)
    if not admin_role or admin_role not in interaction.user.roles:
        return "You do not have the required role to use this command."

    return ""
