import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /pair [phone_number_with_country_code]")
        return
    
    phone = context.args[0]
    # Hakikisha unabadilisha link hii na ya kwako halisi
    node_url = f"https://your-whatsapp-bot.onrender.com/pair?phone={phone}"
    
    try:
        response = requests.get(node_url).json()
        code = response['pairing_code']
        await update.message.reply_text(f"✅ Your Pairing Code: `{code}`", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("Error: Could not connect to WhatsApp Server.")

if __name__ == '__main__':
    # Hapa ndipo ulikuwa umekosea
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN haijawekwa kwenye Environment Variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("pair", pair))
        app.run_polling()
