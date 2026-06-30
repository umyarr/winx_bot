import asyncio
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher()

TASKS_TOPIC_ID = 2

CONTEXT = Path("context.txt").read_text(encoding="utf-8")

SYSTEM_PROMPT = """
Ты помощник по разбору рабочих сообщений проекта Твой Ход.
Разбей сообщение на отдельные задачи.
Если в сообщении несколько действий — создай несколько задач.
Если действие одно — создай одну задачу.
Если задач нет — верни пустой список.

Вот контекст команды:
""" + CONTEXT + """

Правила назначения исполнителя:
- Если упомянуты конкретные @никнеймы — они исполнители
- ПФО, Поволжье, Казань, Нижний Новгород → @umyarr
- ДФО, СФО, СКФО, Дальний Восток, Сибирь, Кавказ → @Angeelikaz
- ЦФО, СЗФО, Санкт-Петербург → @maria_prokhorenko
- Москва → @pau_linazan
- Студенческие команды, Вдохновляю → @danchikstore
- Новые регионы РФ → @deniska121
- Кураторы программ → @yavosya или @o_l_o_v_o
- Если непонятно — null

Правила приоритета:
- high: срочно, сегодня, горит, важно, последний рывок, восклицательный знак
- medium: на этой неделе, до пятницы, скоро
- low: когда будет время, не срочно

Верни строго JSON без пояснений:
{
  "tasks": [
    {
      "title": "краткое название задачи",
      "description": "что нужно сделать подробнее",
      "assignee": "@никнейм или null",
      "deadline": "дедлайн или null",
      "priority": "low/medium/high",
      "links": []
    }
  ]
}
"""

DECOMPOSE_SYSTEM_PROMPT = """
Ты помощник по декомпозиции задач. Твоя работа — определить, является ли задача "контейнером" (несколько самостоятельных действий) или уже атомарной (глагол + проверяемый результат).

Тест "контейнер vs задача":
— Если в тексте есть несколько самостоятельных действий (маркеры: "и", "разобраться с", "организовать", "проработать") — это контейнер, нужно дробить.
— Если задача уже сформулирована как глагол + понятный результат — дробить не нужно.

Если нужно дробить — выдай подзадачи, каждая в формате "глагол + результат" (что сделать → что получится на выходе).
Если не нужно — скажи об этом явно. Не изобретай подпункты ради ритуала.

Не оценивай "неопределённость" самостоятельно по тексту — это ненадёжно без диалога. Не включай эту эвристику.

Отвечай строго в одном из двух форматов:

Если нужно дробить:
Друг, предлагаю разбить твою задачу вот так:

1. [подзадача 1 — глагол + результат]
2. [подзадача 2 — глагол + результат]
3. [подзадача 3 — глагол + результат]

Почему так: [что было не так в исходной формулировке — например, было несколько самостоятельных действий]

Зачем: [конкретная польза — например, видно с чего начать и когда считать каждый пункт закрытым]

Если не нужно дробить:
Друг, тут вроде всё чётко — глагол есть, результат понятен. Закидывай как есть, разбивать не вижу смысла.

Никаких сухих списков без обёртки "друг, предлагаю..." — отвечай как дружеское предложение, не директива.
"""


def analyze_tasks(text: str) -> list:
    with GigaChat(
        credentials=os.getenv("GIGACHAT_KEY"),
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS"
    ) as giga:
        response = giga.chat(Chat(messages=[
            Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT),
            Messages(role=MessagesRole.USER, content=text),
        ]))
    raw = response.choices[0].message.content
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip()).get("tasks", [])


def decompose_task(text: str) -> str:
    with GigaChat(
        credentials=os.getenv("GIGACHAT_KEY"),
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS"
    ) as giga:
        response = giga.chat(Chat(messages=[
            Messages(role=MessagesRole.SYSTEM, content=DECOMPOSE_SYSTEM_PROMPT),
            Messages(role=MessagesRole.USER, content=text),
        ]))
    return response.choices[0].message.content.strip()


@dp.message(F.text)
async def handle(msg: Message):
    if msg.chat.type == "private":
        text = (msg.text or "").strip()
        if not text:
            return
        print(f"[ЛС] от {msg.from_user.id}: {text[:50]}", flush=True)
        processing = await msg.answer("Анализирую...")
        try:
            result = await asyncio.to_thread(decompose_task, text)
            await processing.edit_text(result)
        except Exception as e:
            await processing.edit_text(f"Ошибка: {e}")

    elif msg.chat.type in ("group", "supergroup"):
        bot_info = await bot.get_me()
        mention = f"@{bot_info.username}"
        if mention.lower() not in (msg.text or "").lower():
            return
        text = (msg.text or "").replace(mention, "").strip()

        if not text:
            return

        links = []
        for entity in msg.entities or []:
            if entity.type == "url":
                links.append(msg.text[entity.offset:entity.offset + entity.length])
            elif entity.type == "text_link":
                links.append(entity.url)
        raw_urls = re.findall(r'https?://\S+', msg.text or "")
        found_urls = [re.sub(r'[)\].,!?]+$', '', u) for u in raw_urls]
        for url in found_urls:
            if url not in links:
                links.append(url)
        if links:
            text += "\n\nСсылки: " + ", ".join(links)

        processing = await bot.send_message(
            chat_id=msg.chat.id,
            text="Анализирую...",
            message_thread_id=TASKS_TOPIC_ID
        )

        try:
            tasks = await asyncio.to_thread(analyze_tasks, text)

            if not tasks:
                await processing.edit_text("Задач не нашёл.")
                return

            priority_map = {"high": "высокий", "medium": "средний", "low": "низкий"}

            result = f"Нашёл задач: {len(tasks)}\n\n"
            for i, task in enumerate(tasks, start=1):
                assignee = task.get("assignee") or "не определён"
                deadline = task.get("deadline") or "не указан"
                priority = priority_map.get(task.get("priority", "medium"), "средний")
                task_links = task.get("links") or []
                if not task_links and links:
                    task_links = links

                result += f"{i}. {task['title']}\n"
                result += f"Описание: {task.get('description', '')}\n"
                result += f"Исполнитель: {assignee}\n"
                result += f"Дедлайн: {deadline}\n"
                result += f"Приоритет: {priority}\n"
                if task_links:
                    result += f"Ссылки: {', '.join(task_links)}\n"
                result += "\n"

            await processing.edit_text(result)

        except Exception as e:
            await processing.edit_text(f"Ошибка: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
