🌐 [Русский](translations/ru/README.md) | [中文](translations/zh/README.md)

# @winx_bot — Telegram Task Bot

A bot for team work chats. Mention @winx_bot in a message — it parses the text via GigaChat and returns a structured task: assignee, priority, deadline, links.

Write to the bot in a private chat — it decomposes your task and tells you whether it needs to be split or is already atomic.

## Features

**In group chats (mention @winx_bot):**
- Splits one message into multiple tasks if needed
- Auto-assigns executor by federal district
- Extracts links from messages (entities + regex)
- Detects priority (high / medium / low) from keywords
- Extracts deadlines from text
- Posts results to the «Tasks» topic (topic_id=2)

**In private chat (DM the bot):**
- Accepts any task description
- Determines if it's a "container" (multiple actions) or already atomic
- If needs splitting: returns numbered subtasks in "verb + result" format
- If already atomic: confirms it's good to go as-is
- Responds in a friendly tone ("Друг, предлагаю разбить...")

## Stack

- Python 3.13
- aiogram 3.28
- GigaChat 0.2 (`GIGACHAT_API_PERS`)
- python-dotenv

## Setup

```bash
git clone https://github.com/umyarr/winx_bot
cd winx_bot
pip install -r requirements.txt
cp .env.example .env
# fill in your tokens
python bot.py
```

## Environment variables

```
TG_TOKEN=bot_token_from_BotFather
GIGACHAT_KEY=key_from_GigaChat
```

## Deploy (VPS / systemd)

```bash
systemctl status tg-weeek-bot
systemctl restart tg-weeek-bot
journalctl -u tg-weeek-bot -f
```
