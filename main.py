import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Angalia kama mtumiaji ameweka namba ya simu
    if not context.args:
        await update.message.reply_text("Tafadhali tumia: /pair [namba_ya_simu]\nMfano: /pair 2557XXXXXXXX")
        return
    
    phone = context.args[0]
    
    # Hapa ndipo link ya WhatsApp Bot yako ilipo
    # Tumia link ileile ya https://teleglam-bot.onrender.com uliyonipa
    node_url = f"https://teleglam-bot.onrender.com/pair?phone={phone}"
    
    try:
        # Telegram Bot inatuma ombi kwenye WhatsApp Bot
        response = requests.get(node_url).json()
        code = response['pairing_code']
        await update.message.reply_text(f"✅ Hii hapa Pairing Code yako: `{code}`", parse_mode='Markdown')
    except Exception:
        await update.message.reply_text("Error: Siwezi kuunganisha na WhatsApp Server. Hakikisha URL ni sahihi.")

if __name__ == '__main__':
    # Token inachukuliwa kutoka kwenye Environment Variables za Render
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Error: Hujajaza TELEGRAM_TOKEN kwenye Render!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("pair", pair))
        print("Telegram Bot inafanya kazi...")
        app.run_polling()

