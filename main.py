import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Sanidi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    photo_url = "https://res.cloudinary.com/dvbftux6w/image/upload/v1782940328/yt8vqnuybzly1jhgv9nq.png"
    caption = f"Karibu! Mimi ni AI Bot.\n\nKuna watumiaji {len(users)}.\n\n- Chat nami (Tag @BotUsername kwenye group).\n- /picha [maelezo] : Kutengeneza picha."
    
    keyboard = [
        [InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M")],
        [InlineKeyboardButton("Telegram Channel", url="https://t.me/+nxAx-q0RRLJmOTBk")],
        [InlineKeyboardButton("Cyber Develop", url="https://t.me/+dEZNnJAjUiZjMzc0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Hakikisha bot inajibu kwenye private au kama imetajwa (tagged)
    if update.effective_chat.type == "private" or (update.message.mention_entities and "bot" in update.message.text.lower()):
        users.add(update.effective_user.id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": update.message.text}]
            )
            await update.message.reply_text(response.choices[0].message.content, reply_to_message_id=update.message.message_id)
        except Exception:
            await update.message.reply_text("Kuna tatizo la AI. Hakikisha API key ni sahihi.")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Tumia: /picha [maelezo]")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
    
    try:
        response = client.images.generate(
            model="stabilityai/sdxl",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        await update.message.reply_photo(photo=response.data[0].url, caption=f"Picha ya: {prompt}")
    except Exception:
        await update.message.reply_text("Imeshindwa kutengeneza picha.")

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("picha", generate_image))
    # Hii itasikiliza ujumbe wote, na ndani ya function tumeweka logic ya "tag"
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot inafanya kazi...")
    app.run_polling()

