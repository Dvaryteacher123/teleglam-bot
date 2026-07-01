import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Sanidi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Sanidi OpenRouter (Claude 3.5 Sonnet ni bora kwa coding)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! I am your AI App Generator.\n\n"
        "Send me a description of an app or website you want, and I will write the code for you.\n"
        "Example: /code Create a simple calculator app using HTML and JS."
    )

async def generate_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Please provide a description. Example: /code Create a login page.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Tunatumia Claude 3.5 Sonnet kupitia OpenRouter kwa code bora
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[{"role": "user", "content": f"Write complete, working code for: {prompt}. Return only the code."}]
        )
        
        code_content = response.choices[0].message.content
        
        # Hifadhi code kwenye faili ya muda
        file_name = "generated_app.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(code_content)
        
        # Mtumie mtumiaji faili hiyo
        await update.message.reply_document(document=open(file_name, "rb"), caption="Here is your generated code!")
        
    except Exception as e:
        await update.message.reply_text("Failed to generate code. Check your API Key or Credits.")
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", generate_code))
    
    print("Bot is running...")
    app.run_polling()

