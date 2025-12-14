import discord
from discord import app_commands
from typing import Callable, List, Dict, Any

from browser_automation.redeem import redeem_giftcode_for_all_players


def register_redeem_command(
    tree: app_commands.CommandTree,
    load_players: Callable[[], List[Dict[str, Any]]],
    save_players: Callable[[List[Dict[str, Any]]], None],
):

    @tree.command(name="redeem", description="Redeem a Kingshot gift code for all players")
    @app_commands.describe(gift_code="The gift code to redeem")
    async def redeem(interaction: discord.Interaction, gift_code: str):
        await interaction.response.defer(thinking=True)

        try:
            players = load_players()
            results = await redeem_giftcode_for_all_players(players, gift_code)
            failed = 0
            updated = False

            failed_players = []
            for idx, item in enumerate(results):
                # Keep player nicknames synced for readability
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

            response_message = (
                f"🎁 **Redeem Results for `{gift_code}`**\n"
                f"🚀`{len(results) - failed}/{len(results)}` succeeded!\n\n"
            )
            response_message += "\n".join(failed_players)
            if updated:
                save_players(players)
                response_message += "\n\n💾 Updated player names from page"

            if len(response_message) > 1900:
                response_message = response_message[:1900] + "\n…(truncated)"

            await interaction.followup.send(response_message)

        except Exception as e:
            error_message = f"❌ Error during redemption: {str(e)}"
            await interaction.followup.send(error_message)
            print(f"Error in redeem command: {e}")
