import asyncio
import os
import sys

from config.config import DISCORD_TOKEN, TIMEOUT_MS  # noqa: E402
from dcBot.init_check import ensure_players_json_exists  # noqa: E402
from dcBot.ksRedeemBot import start_bot  # noqa: E402


async def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    ensure_players_json_exists(data_dir)
    
    print("🚀 Starting Kingshot Redeemer Bot...")
    print(f"⏱️  Timeout set to {TIMEOUT_MS}ms")
    
    if DISCORD_TOKEN is None:
        print("❌ DISCORD_TOKEN is not set")
        sys.exit(1)
    
    try:
        await start_bot(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())