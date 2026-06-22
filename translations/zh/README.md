🌐 [English](../../README.md) | [Русский](../ru/README.md)

# @winx_bot — Telegram 任务机器人

团队工作群聊机器人。在消息中 @winx_bot — 它通过 GigaChat 解析文本并返回结构化任务：负责人、优先级、截止日期、链接。

## 功能

- 仅在群组中响应 @提及
- 将一条消息拆分为多个任务（如有需要）
- 根据联邦区自动分配执行人
- 从消息中提取链接（实体 + 正则）
- 根据关键词识别优先级（高 / 中 / 低）
- 从文本中提取截止日期
- 将结果发送至「任务」话题（topic_id=2）

## 技术栈

- Python 3.13
- aiogram 3.28
- GigaChat 0.2 (`GIGACHAT_API_PERS`)
- python-dotenv

## 安装

```bash
git clone https://github.com/umyarr/winx_bot
cd winx_bot
pip install -r requirements.txt
cp .env.example .env
# 填写你的 token
python bot.py
```

## 环境变量

```
TG_TOKEN=来自BotFather的机器人令牌
GIGACHAT_KEY=GigaChat密钥
```

## VPS 部署（systemd）

```bash
systemctl status tg-weeek-bot
systemctl restart tg-weeek-bot
journalctl -u tg-weeek-bot -f
```
