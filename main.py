import os
import logging
import time
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# ==================== SETUP ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# AI Client (OpenRouter, lakini hatutajiita)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")  # Weka kwenye environment variables
)

# Default model
DEFAULT_MODEL = "gpt-3.5-turbo"
user_models = {}  # kuhifadhi modeli kwa kila mtumiaji

# ==================== COMMAND REGISTRY ====================
# Hii orodha ina amri zote kutoka kwenye list yako, zikiwa na vitendaji vyao
# Kwa amri ambazo hazijatekelezwa, tunatumia vitendaji vya jumla (generic)
command_handlers = {}

# ---- Vitendaji vya msingi ----
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start - Onyesha maelezo na amri"""
    user = update.effective_user
    welcome = (
        f"👋 *Karibu {user.first_name}!*\n\n"
        "Mimi ni bot ya AI yenye uwezo mkubwa.\n"
        "Tumia amri zifuatazo (kwa kiambishi `.`):\n\n"
        "• `.ask <swali>` - Uliza AI lolote\n"
        "• `.imagine <maelezo>` - Tengeneza picha kwa AI\n"
        "• `.sticker` - Geuza picha kuwa stika\n"
        "• `.ping` - Angalia kasi ya bot\n"
        "• `.runtime` - Muda wa bot imeendelea\n"
        "• `.help` - Orodha kamili ya amri\n\n"
        "📌 *Vitufe:*"
    )
    keyboard = [
        [InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029VbCRC9b5fM5cruU8PF2M")],
        [InlineKeyboardButton("Telegram Channel", url="https://t.me/+nxAx-q0RRLJmOTBk")],
        [InlineKeyboardButton("Cyber Develop", url="https://t.me/+dEZNnJAjUiZjMzc0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode="Markdown")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help - Onyesha orodha ya amri zote"""
    help_text = (
        "*📋 Orodha ya Amri Zote:*\n\n"
        "Bonyeza kitufe hapa chini kuona orodha kamili.\n"
        "Au tumia `.ask <swali>` kwa maswali yoyote."
    )
    # Kwa kuwa orodha ni ndefu, tunatuma link ya maelezo au sehemu
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def cmd_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*🤖 About Bot:*\n\nBot hii inatumia AI ya hali ya juu kujibu maswali na kutengeneza picha.\nImeundwa na Cyber Develop team.", parse_mode="Markdown")

async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if 'history' in context.user_data:
        context.user_data['history'] = []
    await update.message.reply_text("✅ Historia imefutwa!")

async def cmd_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Badilisha modeli ya AI"""
    args = context.args
    user_id = update.effective_user.id
    if not args:
        current = user_models.get(user_id, DEFAULT_MODEL)
        await update.message.reply_text(f"🧠 Modeli ya sasa: *{current}*\n\nTumia `/model gpt-4-turbo` kubadilisha.", parse_mode="Markdown")
        return
    new_model = args[0]
    user_models[user_id] = new_model
    await update.message.reply_text(f"✅ Modeli imebadilishwa kuwa: *{new_model}*", parse_mode="Markdown")

async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    await update.message.reply_text("🏓 Pong!")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000)
    await update.message.reply_text(f"⚡ Latency: {latency}ms")

async def cmd_runtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Hii itahitaji kuhifadhi muda wa kuanza kwa bot, tumia variable global
    if not hasattr(context.bot, 'start_time'):
        context.bot.start_time = time.time()
    elapsed = int(time.time() - context.bot.start_time)
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    await update.message.reply_text(f"⏰ Muda wa bot: {hours}h {minutes}m {seconds}s")

async def cmd_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Mmiliki: @Dvary (2349028711461)")

# ---- Vitendaji vya AI na Media ----
async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """.ask <swali> - Uliza AI"""
    query = update.message.text.replace(".ask", "", 1).strip()
    if not query:
        await update.message.reply_text("Tafadhali andika swali baada ya .ask")
        return
    await process_ai_query(update, context, query)

async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.replace(".ai", "", 1).strip()
    if not query:
        await update.message.reply_text("Tafadhali andika swali baada ya .ai")
        return
    await process_ai_query(update, context, query)

async def cmd_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.replace(".gpt", "", 1).strip()
    if not query:
        await update.message.reply_text("Tafadhali andika swali baada ya .gpt")
        return
    await process_ai_query(update, context, query)

async def process_ai_query(update, context, query):
    """Tumia AI kujibu swali, na onyesha typing"""
    user_id = update.effective_user.id
    # Onyesha typing
    await update.message.chat.send_action(action="typing")

    # Historia
    if 'history' not in context.user_data:
        context.user_data['history'] = []
    context.user_data['history'].append({"role": "user", "content": query})

    model = user_models.get(user_id, DEFAULT_MODEL)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=context.user_data['history'],
            max_tokens=1000,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        context.user_data['history'].append({"role": "assistant", "content": answer})
        # Gawanya jibu ikiwa refu
        if len(answer) > 4000:
            parts = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(answer)
    except Exception as e:
        logger.error(f"AI error: {e}")
        await update.message.reply_text("❌ Samahani, kuna tatizo la kiufundi. Jaribu tena.")

async def cmd_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """.imagine <maelezo> - Tengeneza picha kwa AI"""
    prompt = update.message.text.replace(".imagine", "", 1).strip()
    if not prompt:
        await update.message.reply_text("Tafadhali andika maelezo ya picha.")
        return
    await update.message.chat.send_action(action="typing")
    # Tumia OpenRouter image generation (kama inapatikana)
    try:
        # OpenRouter inasaidia image generation kupitia modeli fulani
        response = client.chat.completions.create(
            model="openai/dall-e-3",  # au "stabilityai/stable-diffusion-xl"
            messages=[{"role": "user", "content": f"Generate an image: {prompt}"}],
            # Kwa sasa, OpenRouter haitoi picha moja kwa moja kwenye chat completion,
            # lakini tunaweza kutumia API tofauti. Kwa kuwa hatuwezi, tunarudisha ujumbe.
        )
        # Hapa tungepata URL ya picha, lakini kwa sasa tunajibu tu
        await update.message.reply_text("🖼️ Picha itatolewa hivi karibuni. (Feature inaendelea)")
    except Exception as e:
        await update.message.reply_text("❌ Kumekuwa na hitilafu katika kutengeneza picha.")

async def cmd_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """.sticker - Geuza picha iliyoreply kuwa stika"""
    reply = update.message.reply_to_message
    if not reply or not reply.photo:
        await update.message.reply_text("Tafadhali reply picha kwa .sticker")
        return
    photo_file = await reply.photo[-1].get_file()
    file_path = f"sticker_{update.effective_user.id}.png"
    await photo_file.download_to_drive(file_path)
    # Tuma kama stika (hapa tunatumia picha moja kwa moja)
    with open(file_path, "rb") as f:
        await update.message.reply_sticker(f)
    os.remove(file_path)

# ---- Vitendaji vya jumla kwa amri zingine ----
async def generic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kwa amri zote zisizotekelezwa, tuma kwa AI au jibu la placeholder."""
    command = update.message.text.split()[0] if update.message.text else ""
    # Tuma kwa AI kujibu kwa ujumla
    query = update.message.text
    await process_ai_query(update, context, f"Jibu swali hili kwa lugha ya Kiswahili: {query}")

# ---- Sajili amri zote kwenye orodha ----
# Tunaweza kuongeza amri zote kutoka kwenye list ya mtumiaji
# Hapa tunaweka baadhi, lakini zaidi zitaenda kwa generic_command

command_handlers = {
    "start": cmd_start,
    "help": cmd_help,
    "about": cmd_about,
    "clear": cmd_clear,
    "model": cmd_model,
    "ping": cmd_ping,
    "runtime": cmd_runtime,
    "owner": cmd_owner,
    "ask": cmd_ask,
    "ai": cmd_ai,
    "gpt": cmd_gpt,
    "imagine": cmd_imagine,
    "sticker": cmd_sticker,
    # Hapa unaweza kuongeza amri nyingine nyingi kwa kuzielekeza kwa generic_command
    # Kwa mfano: ".google", ".wiki", ".weather", n.k.
}

# Kwa amri ambazo hazipo kwenye orodha, tunatumia generic_command
async def handle_dot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inashughulikia ujumbe unaoanza na '.'"""
    text = update.message.text
    if not text.startswith('.'):
        return
    # Tenganisha amri
    parts = text.split(maxsplit=1)
    cmd = parts[0][1:].lower()  # ondoa '.' na badili lowercase
    # Tafuta kwenye kamusi
    handler = command_handlers.get(cmd)
    if handler:
        await handler(update, context)
    else:
        # Ikiwa amri haipo, tumia generic
        await generic_command(update, context)

# ==================== MAIN ====================
def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN haijapatikana! Weka kwenye environment variables.")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Amri za / (slash)
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("about", cmd_about))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("runtime", cmd_runtime))
    app.add_handler(CommandHandler("owner", cmd_owner))
    
    # Amri za dot (.)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dot_command))
    
    # Anza polling
    app.run_polling()

if __name__ == '__main__':
    main()
