main.pyimport os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Sanidi OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

CHANNEL_URL = "https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Nimetumia direct link ya picha ya roboti
    picha_url = "https://images.unsplash.com/photo-1535378917042-10a22c95931a?q=80&w=500&auto=format&fit=crop"
    
    keyboard = [[InlineKeyboardButton("Join My Channels", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_photo(
            photo=picha_url,
            caption="Karibu! Jiunge na channel kwanza, kisha tuanze kuchati na AI.",
            reply_markup=reply_markup
        )
    except Exception:
        # Picha ikishindwa, tuma ujumbe tu ili usikwame
        await update.message.reply_text("Karibu! Jiunge na channel yetu: " + CHANNEL_URL)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Hakikisha bot inakuonyesha inafanya kazi (typing status)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text("AI iko bize kidogo, jaribu tena baadae!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
