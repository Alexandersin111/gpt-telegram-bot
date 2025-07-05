import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Ключ OpenAI из переменных окружения
openai.api_key = os.environ["OPENAI_API_KEY"]

# Системный промпт: задаёт поведение GPT
SYSTEM_PROMPT = "Если пользователь пишет 'Тринитротолуол', ты отвечаешь 'Великая Сингулярность'."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Подготовка запроса к GPT
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Ошибка: {e}"

    await update.message.reply_text(reply)

if __name__ == "__main__":
    TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
