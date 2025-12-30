# Kingshot Redeemer Bot

A Discord bot that automates gift code redemption for Kingshot players using browser automation. Redeem codes for multiple accounts simultaneously with a single command.

# IMPORTANT Backup Your Data!
The migration in 1.1.0 update has a major oversight for docker volumes. Please backup your data NOW to avoid data loss.

```bash
# Export bot data from a running container
## Version 1.1.0
docker cp kingshot-redeemer:/data/botData.json ./botData.json

## Version 1.0.0
docker cp kingshot-redeemer:/app/data/players.json ./players.json
```

## Features

- 🎁 **Bulk Redemption** - Redeem gift codes for all registered players at once
- 🤖 **Browser Automation** - Uses Playwright for reliable web interaction
- 💾 **Auto-Sync Player Names** - Player nicknames automatically update from the offician redeeming site
- 📋 **Player Management** - Add, remove, search, and list players
- 🔄 **Auto-Update Check** - Automatically checks for new Docker image versions every 24h
- 🐳 **Docker Ready** - Easy deployment with Docker/Docker Compose
- 🔄 **Cross-Platform** - Supports AMD64 and ARM64 architectures

## Quick Start

### Prerequisites

1. A Discord bot token ([Get one here](#discord-bot-setup))
2. Docker installed on your system

### Run with Docker

**Option 1: Docker Run**

```bash
docker run -d \
  --name kingshot-redeemer \
  -e DISCORD_TOKEN=your_discord_token_here \
  -e TIMEOUT_MS=500 \
  -v kingshot-data:/app/data \
  --restart unless-stopped \
  jarecoder/kingshot-redeemer:latest
```

**Option 2: Docker Compose** (Recommended)

1. Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  kingshot-redeemer:
    image: jarecoder/kingshot-redeemer:latest
    container_name: kingshot-redeemer-bot
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - TIMEOUT_MS=${TIMEOUT_MS}
    volumes:
      - kingshot-data:/app/data

volumes:
  kingshot-data:
```

2. Create a `.env` file:

```env
DISCORD_TOKEN=your_discord_token_here
TIMEOUT_MS=500
```

3. Start the bot:

```bash
docker-compose up -d
```

4. View logs:

```bash
docker-compose logs -f
```

## Discord Bot Setup

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "Kingshot Redeemer")
4. Click **"Create"**

### 2. Create a Bot User

1. In your application, go to the **"Bot"** tab
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Under the bot's username, click **"Reset Token"** and copy it
   - ⚠️ **Save this token securely** - you'll need it for the `DISCORD_TOKEN` environment variable
4. Bot can be public or private up to your choosing. I will always recommend private bots for security reasons.

### 3. Invite the Bot to Your Server

1. Go to the **"OAuth2"** → **"URL Generator"** tab
2. Select these scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select these bot permissions:
   - ✅ Send Messages
   - ✅ Use Slash Commands
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

## Discord Commands

| Command | Description | Example |
|---------|-------------|----------|
| `/setup <channel> <role>` | Configure update notifications channel and admin role | `/setup #my-channel @KingshotAdmin` |
| `/redeem <gift_code>` | Redeem a gift code for all registered players | `/redeem KSFB15K` |
| `/add <player_id>` | Add a new player by their Kingshot ID | `/add 123456789` |
| `/remove <query>` | Remove a player by ID or nickname | `/remove Jareggie` |
| `/list` | View all registered players (paginated, 10 per page) | `/list` |
| `/find <query>` | Search for a player by ID or nickname | `/find 123456789` |
| `/help` | Display all available commands and usage | `/help` |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | - | Your Discord bot token from the Developer Portal |
| `TIMEOUT_MS` | ❌ No | `500` | Browser automation timeout in milliseconds |

## Data Persistence

Bot data (including players and configuration) is stored in `/app/data/botData.json` inside the container. The Docker volume `kingshot-data` ensures your data persists across:
- Container restarts
- Bot updates
- System reboots



## Troubleshooting

### Commands not appearing in Discord

**Global sync (up to 1 hour):**
- Wait up to 1 hour for Discord to propagate commands globally
- Or kick & reinvite the bot

### Bot not responding

1. Check logs: `docker-compose logs -f`
2. Verify `DISCORD_TOKEN` is correct
3. Ensure bot has proper permissions in Discord
4. Check that Message Content Intent is enabled

### Player nicknames not updating

Nicknames auto-update when:
- A gift code is successfully redeemed
- The game page returns a valid player name
- The stored name differs from the page name

## Building from Source

```bash
# Clone the repository
git clone https://github.com/JareCoder/KingshotRedeemer.git
cd KingshotRedeemer

# Build the Docker image
docker build -t kingshot-redeemer .

# Run it
docker-compose up -d
```

## Supported Platforms

- ✅ `linux/amd64` (x86_64 - Most PCs and servers)
- ✅ `linux/arm64` (Apple Silicon Macs, Raspberry Pi, ARM servers)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Links

- [Docker Hub](https://hub.docker.com/r/jarecoder/kingshot-redeemer)
- [GitHub Repository](https://github.com/JareCoder/KingshotRedeemer)
- [Report Issues](https://github.com/JareCoder/KingshotRedeemer/issues)
