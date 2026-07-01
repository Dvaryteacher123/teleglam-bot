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
    caption = "Karibu! Mimi ni AI Bot.\n\nKwenye Group, nitajibu tu ukinipigia tag (mfano: @dvary mambo?)."
    
    keyboard = [
        [InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M")],
        [InlineKeyboardButton("Telegram Channel", url="https://t.me/+nxAx-q0RRLJmOTBk")],
        [InlineKeyboardButton("Cyber Develop", url="https://t.me/+dEZNnJAjUiZjMzc0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tunahakikisha ujumbe unao maandishi
    if not update.message or not update.message.text:
        return

    # Kwenye Private, jibu kila kitu. Kwenye Group, angalia tag (mention)
    is_private = update.effective_chat.type == "private"
    is_mentioned = False
    
    # Angalia kama bot imetajwa kwenye entities
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == "mention":
                mention_text = update.message.text[entity.offset:entity.offset+entity.length]
                # Badilisha 'dvary' na username ya bot yako (bila @)
                if "dvary" in mention_text.lower():
                    is_mentioned = True

    if is_private or is_mentioned:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Ondoa jina la bot kwenye swali ili AI isichanganyikiwe
            clean_text = update.message.text.replace("@dvary", "").strip()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": clean_text}]
            )
            await update.message.reply_text(response.choices[0].message.content, reply_to_message_id=update.message.message_id)
        except Exception as e:
            logging.error(e)
            await update.message.reply_text("Samahani, AI haipatikani kwa sasa.")

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    # Tunasikiliza text zote, logic ya tag ipo ndani ya function
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot inafanya kazi...")
    app.run_polling()
