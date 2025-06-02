# 🤖 Hangman Telegram Bot

Игра "Виселица" в Telegram с возможностью генерации слов от OpenAI по теме и уровню сложности.

## 🚀 Возможности

- Генерация слов от ChatGPT (GPT-3.5)
- Поддержка темы и сложности
- Асинхронный Telegram-бот на `aiogram 3`
- Управление через FSM (машина состояний)

## 🛠 Установка

```bash
git clone https://github.com/00Titan/hangman-telegram-bot.git
cd hangman-telegram-bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt