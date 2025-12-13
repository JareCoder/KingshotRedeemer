import asyncio
import sys
import os

from dcBot.ksRedeemBot import start_bot  # noqa: E402
from dotenv import load_dotenv


async def main():
    load_dotenv()

    discord_token = os.getenv("DISCORD_TOKEN")

    if not discord_token:
        print("❌ Error: DISCORD_TOKEN environment variable is not set.")
        print("Please set it using: $env:DISCORD_TOKEN='your_token_here'")
        sys.exit(1)
    
    print("🚀 Starting Kingshot Redeemer Bot...")
    
    try:
        await start_bot(discord_token)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())