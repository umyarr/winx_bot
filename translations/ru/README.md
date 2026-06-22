🌐 [English](../../README.md) | [中文](../zh/README.md)

# @winx_bot — Telegram Task Bot

Бот для рабочего чата команды. Упомяни @winx_bot в сообщении — он разберёт текст через GigaChat и вернёт структурированную задачу: исполнитель, приоритет, дедлайн, ссылки.

## Что умеет

- Реагирует только на @упоминание в группе
- Разбивает одно сообщение на несколько задач (если их несколько)
- Назначает исполнителя автоматически по федеральному округу
- Извлекает ссылки из сообщений (entities + regex)
- Определяет приоритет (high / medium / low) по ключевым словам
- Извлекает дедлайн из текста
- Отвечает в тему «Задачи от викса» (topic_id=2)

## Стек

- Python 3.13
- aiogram 3.28
- GigaChat 0.2 (`GIGACHAT_API_PERS`)
- python-dotenv

## Установка

```bash
git clone https://github.com/umyarr/winx_bot
cd winx_bot
pip install -r requirements.txt
cp .env.example .env
# заполни .env своими токенами
python bot.py
```

## Переменные окружения

```
TG_TOKEN=токен_бота_от_BotFather
GIGACHAT_KEY=ключ_от_GigaChat
```

## Деплой на VPS (systemd)

```bash
systemctl status tg-weeek-bot
systemctl restart tg-weeek-bot
journalctl -u tg-weeek-bot -f
```
