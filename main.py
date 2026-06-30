import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Inasoma tokens kutoka kwenye Render Environment Variables
# Hakikisha umeziongeza kwenye Render Dashboard -> Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Weka link ya picha yako ya menu hapa (lazima iwe direct image link)
    picha_url = "URL_YA_PICHA_YAKO_HAPA" 
    
    # Link ya channel yako ya WhatsApp
    whatsapp_channel_url = "https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M"
    
    # Kitufe cha kujiunga
    keyboard = [[InlineKeyboardButton("Jiunge na Channel ya WhatsApp", url=whatsapp_channel_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Kutuma picha na ujumbe
    try:
        await update.message.reply_photo(
            photo=picha_url,
            caption="Karibu! Hii ndiyo menyu yetu. Tafadhali jiunge na channel yetu ya WhatsApp kwanza ili uendelee kutumia bot yetu.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await update.message.reply_text("Samahani, picha imeshindwa kupakia. Tafadhali jiunge na channel yetu kwanza: " + whatsapp_channel_url)

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN haijapatikana kwenye environment variables!")
    else:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        print("Bot inaanza...")
        app.run_polling()

