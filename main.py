import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Inasoma token kutoka kwenye Environment Variables zilizopo kwenye Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Usalama: Hakikisha token zipo kabla ya kuanza
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Tafadhali weka TELEGRAM_TOKEN na GEMINI_API_KEY kwenye Environment Variables!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update, context):
    await update.message.reply_text('Bot inafanya kazi vyema!')

async def handle_message(update, context):
    response = model.generate_content(update.message.text)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot inaanza...")
    app.run_polling()

