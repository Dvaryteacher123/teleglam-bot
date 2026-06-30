import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Usanidi wa Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Weka API Key yako ya OpenRouter hapa au kwenye Environment Variables
# Hakikisha kwenye Render Environment Variables umeita: OPENROUTER_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Mambo! Mimi ni bot msaidizi. Niulize chochote!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Tunatumia modeli ya bei nafuu na ya haraka kupitia OpenRouter
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct", 
            messages=[{"role": "user", "content": user_text}]
        )
        response = completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Hitilafu ya OpenRouter: {e}")
        await update.message.reply_text("Samahani, nimeshindwa kuwasiliana na AI kwa sasa.")

if __name__ == '__main__':
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot inaanza kufanya kazi...")
    app.run_polling()
