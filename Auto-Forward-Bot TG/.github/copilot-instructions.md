# Auto-Forward-Bot TG

## Stack
- **Runtime**: Python 3.6+
- **Library**: Pyrogram (Telegram client library)
- **Deployment**: Heroku, Docker, VPS

## Project Structure
```
bot.py                 # Main bot logic
config.py              # Configuration & secrets
translation.py         # Multi-language support
requirements.txt       # Python dependencies
Procfile              # Heroku deployment config
runtime.txt           # Python version spec
```

## Key Patterns
- **Automatic Forwarding**: Watches source channel(s), auto-forwards to destination(s)
- **API Credentials**: Requires Telegram API_ID & API_HASH from my.telegram.org
- **Bot Token**: @BotFather token for Telegram bot API
- **Channel Mapping**: Format `source_id:dest_id` (e.g., `-10023352648:-100655379`)
- **Simple Logic**: Minimal dependencies, lightweight footprint

## Common Commands
```bash
pip install -r requirements.txt    # Install dependencies
python bot.py                       # Run locally
heroku create && git push heroku    # Deploy to Heroku
```

## Configuration
- **Env vars**: `API_ID`, `API_HASH`, `TG_BOT_TOKEN`, channel mappings
- **my.telegram.org**: Get API_ID and API_HASH (required for Pyrogram)
- **@BotFather**: Create bot token via Telegram

## Important Files
- `bot.py` — Main forwarding logic
- `config.py` — Credentials & channel configuration
- `translation.py` — Localization support
- `requirements.txt` — Pyrogram + dependencies
- `Procfile` — Heroku worker config

## Notes
- API_ID and API_HASH are personal; never commit to repo
- Bot must be added to both source and destination channels with permissions
- Test with test channels before running on production channels
