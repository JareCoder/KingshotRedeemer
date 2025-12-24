import aiohttp
import discord
from discord.ext import tasks
from typing import Dict, Any, Callable

class UpdateChecker:
    def __init__(self, bot: discord.Client, bot_data: Dict[str, Any], save_data_func: Callable[[Dict[str, Any]], None]):
        self.bot = bot
        self.bot_data = bot_data
        self.save_data = save_data_func
        self.image_name = "jarecoder/kingshot-redeemer"
        self.check_updates.start()

    def unload(self):
        self.check_updates.cancel()

    @tasks.loop(hours=24)
    async def check_updates(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://hub.docker.com/v2/repositories/{self.image_name}/tags/latest"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        remote_digest = data.get("digest")
                        
                        if not remote_digest:
                            print("⚠️ Could not retrieve digest from Docker Hub.")
                            return

                        if "botConfig" not in self.bot_data:
                            self.bot_data["botConfig"] = {}
                        
                        config = self.bot_data["botConfig"]
                        stored_digest = config.get("last_docker_digest")
                        
                        if stored_digest is None:
                            print(f"ℹ️ First run or no stored digest. Saving current digest: {remote_digest}")
                            config["last_docker_digest"] = remote_digest
                            self.save_data(self.bot_data)
                        elif stored_digest != remote_digest:
                            print(f"📢 Update available! Remote: {remote_digest}, Stored: {stored_digest}")
                            channel_id = config.get("allowed_channel")
                            if channel_id:
                                channel = self.bot.get_channel(channel_id)
                                if channel:
                                    try:
                                        await channel.send(
                                            "📢 **Update Available!**\n"
                                            "A new version of the Kingshot Redeemer bot is available on Docker Hub.\n"
                                            "Please pull the latest image and restart the container to update."
                                        )
                                    except discord.Forbidden:
                                        print("❌ Cannot send message to channel: Forbidden")
                                    except Exception as e:
                                        print(f"❌ Error sending update message: {e}")
                                else:
                                    print(f"⚠️ Configured channel {channel_id} not found.")
                            else:
                                print("⚠️ No channel configured for notifications.")
                            
                            # Update stored digest so we don't notify again for this version
                            config["last_docker_digest"] = remote_digest
                            self.save_data(self.bot_data)
                        else:
                            print("✅ Bot is up to date.")
                    else:
                        print(f"❌ Failed to check for updates: HTTP {response.status}")
        except Exception as e:
            print(f"❌ Error checking for updates: {e}")

    @check_updates.before_loop
    async def before_check_updates(self):
        await self.bot.wait_until_ready()
