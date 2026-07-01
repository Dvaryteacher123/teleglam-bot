import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Sanidi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Sanidi OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

# Set ya kuhifadhi User IDs (Ili kujua idadi ya watu)
users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ongeza mtumiaji kwenye list
    users.add(update.effective_user.id)
    
    photo_url = "https://res.cloudinary.com/dvbftux6w/image/upload/v1782940328/yt8vqnuybzly1jhgv9nq.png"
    caption = f"Karibu! Mimi ni AI Bot.\n\nKuna watumiaji {len(users)} wanaotumia bot hii.\n\nTumia vitufe hapo chini kutembelea channel zetu:"
    
    keyboard = [
        [InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M")],
        [InlineKeyboardButton("Telegram Channel", url="https://t.me/+nxAx-q0RRLJmOTBk")],
        [InlineKeyboardButton("Cyber Develop", url="https://t.me/+dEZNnJAjUiZjMzc0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ongeza mtumiaji kama alikuwa hajasajiliwa
    users.add(update.effective_user.id)
    
    # Inaonyesha "typing..."
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    user_text = update.message.text
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Samahani, kuna tatizo la API key. Tafadhali hakikisha OPENROUTER_API_KEY imewekwa vizuri.")
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot inafanya kazi...")
    app.run_polling()

