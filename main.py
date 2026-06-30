import os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Sanidi OpenAI (OpenRouter)
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Link ya channel yako
CHANNEL_URL = "https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Picha ya menyu (Weka link halisi hapa)
    picha_url = "https://i.ibb.co/picha-yako/menu.jpg" 
    
    keyboard = [[InlineKeyboardButton("Join My Channels", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=picha_url,
        caption="Karibu! Tafadhali jiunge na channel yetu ya WhatsApp kwanza hapo chini, kisha nitumie swali lolote ili tuanze kuchati na AI.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Bot inatuma ujumbe kwa AI
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text("Samahani, kuna tatizo la kiufundi. Jaribu tena baadae.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot inafanya kazi!")
    app.run_polling()
