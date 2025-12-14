import asyncio
import sys

from config.config import DISCORD_TOKEN, TIMEOUT_MS  # noqa: E402
from dcBot.ksRedeemBot import start_bot  # noqa: E402


async def main():
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