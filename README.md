# @winx_bot — Telegram Task Bot

Бот для рабочего чата команды «Твой Ход». Реагирует на @упоминание, анализирует сообщение через GigaChat и формирует задачу: исполнитель, приоритет, дедлайн, ссылки.

---

## Что умеет

- Реагирует только на @упоминание в группе
- Разбивает одно сообщение на несколько задач (если их несколько)
- Назначает исполнителя автоматически по федеральному округу
- Извлекает ссылки из сообщений (entities + regex)
- Определяет приоритет (high / medium / low) по ключевым словам
- Извлекает дедлайн из текста
- Отвечает в тему «Задачи от викса» (topic_id=2)

---

## Стек.

- Python 3.13
- aiogram 3.28
- GigaChat 0.2 (scope: `GIGACHAT_API_PERS`)
- python-dotenv

---

## Структура

```
tg-weeek-bot/
├── bot.py          ← основной код
├── context.txt     ← контекст команды (роли, округа)
├── .env            ← секреты (не в git)
├── .env.example    ← шаблон переменных
└── .gitignore
```

---

## Установка

```bash
git clone https://github.com/umyarr/tg-weeek-bot
cd tg-weeek-bot
pip install -r requirements.txt
cp .env.example .env
# заполни .env своими токенами
python bot.py
```

---

## Переменные окружения (.env)

```
TG_TOKEN=токен_бота_от_BotFather
GIGACHAT_KEY=ключ_от_GigaChat
```

---

## Деплой на VPS (systemd)

Бот запущен как systemd-сервис на Питерском VPS (`212.116.115.131`).

```bash
# Статус
systemctl status tg-weeek-bot

# Перезапуск
systemctl restart tg-weeek-bot

# Логи в реальном времени
journalctl -u tg-weeek-bot -f
```

---

## Расход токенов GigaChat

- ~1500–2000 токенов на запрос
- Лимит: 1 млн токенов (личный аккаунт GIGACHAT_API_PERS)

---

## Что планируется

- [ ] Кнопки «Создать в Weeek» / «Пропустить» под каждой задачей
- [ ] Weeek API интеграция
- [ ] Логирование ошибок в отдельный чат
