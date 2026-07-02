import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Hii inaangalia kama umeweka namba ya simu
    if not context.args:
        await update.message.reply_text("Tafadhali tumia: /pair [namba_ya_simu]")
        return
    
    phone = context.args[0]
    
    # HAPA ndipo unapoandika Link ya WhatsApp Bot yako
    # Badilisha "URL_YA_WHATSAPP_BOT" na ile link ya WhatsApp bot yako (mfano: https://whatsapp-bot-123.onrender.com)
    node_url = f"https://URL_YA_WHATSAPP_BOT.onrender.com/pair?phone={phone}"
    
    try:
        response = requests.get(node_url).json()
        code = response['pairing_code']
        await update.message.reply_text(f"✅ Hii hapa Pairing Code yako: `{code}`", parse_mode='Markdown')
    except Exception:
        await update.message.reply_text("Error: Siwezi kuunganisha na WhatsApp Server. Hakikisha URL ni sahihi.")

if __name__ == '__main__':
    # Bot inachukua TOKEN kutoka kwenye Environment Variable (TELEGRAM_TOKEN)
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Error: Hujajaza TELEGRAM_TOKEN kwenye Render Environment!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("pair", pair))
        app.run_polling()
