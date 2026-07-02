import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mtumiaji anaandika /pair 2557XXXXXXXX
    if not context.args:
        await update.message.reply_text("Usage: /pair [phone_number_with_country_code]")
        return
    
    phone = context.args[0]
    # URL ya Node.js server yako kule Render
    node_url = f"https://your-whatsapp-bot.onrender.com/pair?phone={phone}"
    
    try:
        response = requests.get(node_url).json()
        code = response['pairing_code']
        await update.message.reply_text(f"✅ Your Pairing Code: `{code}`", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("Error: Could not connect to WhatsApp Server.")

if __name__ == '__main__':
    app = ApplicationBuilder().token("YOUR_TELEGRAM_TOKEN").build()
    app.add_handler(CommandHandler("pair", pair))
    app.run_polling()

