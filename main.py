import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Sanidi logging ili uone hitilafu zikijitokeza
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Sanidi OpenRouter (Hakikisha API key imewekwa kwenye Render Environment Variables)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Link ya picha yako
    photo_url = "https://res.cloudinary.com/dvbftux6w/image/upload/v1782940328/yt8vqnuybzly1jhgv9nq.png"
    
    # Maandishi ya juu
    caption = "Karibu! Mimi ni AI Bot. Tumia vitufe hapo chini kutembelea channel zetu:"
    
    # Kutengeneza vitufe vya channel
    keyboard = [
        [InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M")],
        [InlineKeyboardButton("Telegram Channel", url="https://t.me/+nxAx-q0RRLJmOTBk")],
        [InlineKeyboardButton("Cyber Develop", url="https://t.me/+dEZNnJAjUiZjMzc0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Inatuma picha na vitufe chini yake
    await update.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Mawasiliano na AI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )
    
    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

if __name__ == '__main__':
    # Token inachukuliwa kutoka Render Environment Variables
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    app.run_polling()

