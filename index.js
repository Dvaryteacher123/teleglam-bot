const { Client, LocalAuth } = require('whatsapp-web.js');
const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');
require('dotenv').config();

// Sanidi Telegram (Inatumia Token kutoka Render Env)
const tg = new TelegramBot(process.env.TELEGRAM_TOKEN, { polling: true });

// Sanidi WhatsApp (Inatumia LocalAuth kuhifadhi session)
const wa = new Client({
    authStrategy: new LocalAuth({ dataPath: './session' }),
    puppeteer: { args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

// Telegram: Amri ya kupata Pairing Code
tg.onText(/\/pair (.+)/, async (msg, match) => {
    const phone = match[1];
    try {
        tg.sendMessage(msg.chat.id, "Naandaa code ya pairing, subiri...");
        const code = await wa.requestPairingCode(phone);
        tg.sendMessage(msg.chat.id, `✅ Code yako ni: *${code}*\n\nNenda WhatsApp: Link Devices > Link with phone number.`);
    } catch (e) {
        tg.sendMessage(msg.chat.id, "⚠️ Imeshindikana: " + e.message);
    }
});

// WhatsApp: Logic ya AI (OpenRouter)
wa.on('message', async (msg) => {
    if (msg.fromMe) return;

    // Menu ya haraka
    if (msg.body.toLowerCase() === 'menu') {
        msg.reply("Karibu Dvary-Music!\nAndika 'AI: [swali]' ili kuongea na mtaalamu wetu.");
    }

    // AI logic ikianza na "AI: "
    if (msg.body.startsWith('AI:')) {
        const swali = msg.body.replace('AI:', '').trim();
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
                "Content-Type": "application/json",
                "HTTP-Referer": "https://dvary-music.com",
                "X-Title": "Dvary AI"
            },
            body: JSON.stringify({
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": swali}]
            })
        });
        const data = await response.json();
        if (data.choices) {
            msg.reply(data.choices[0].message.content);
        }
    }
});

wa.initialize();
console.log("Bot imewashwa na inasubiri maelekezo...");

