import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Usanidi wa Logging (Ili uone kinachoendelea kwenye logs za Render)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inasoma funguo kutoka kwenye Environment Variables za Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Usanidi wa Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Kazi ya /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Mambo! Mimi ni bot msaidizi. Niulize chochote!')

# Kazi ya kujibu ujumbe kwa kutumia AI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Inatuma ujumbe kwa Gemini
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Hitilafu ya Gemini: {e}")
        await update.message.reply_text("Samahani, nimeshindwa kuchakata ombi lako kwa sasa.")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("Hitilafu: TELEGRAM_TOKEN au GEMINI_API_KEY haijawekwa kwenye Environment Variables!")
    else:
        # Inaanza bot
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        
        # Inasajili handlers
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("Bot inaanza kufanya kazi...")
        app.run_polling()
