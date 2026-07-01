const { Client, LocalAuth } = require('whatsapp-web.js');
const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');
require('dotenv').config();

const tg = new TelegramBot(process.env.TELEGRAM_TOKEN, { polling: true });

const wa = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    }
});

// Amri ya Telegram ya kupata Pairing Code
tg.onText(/\/pair (.+)/, async (msg, match) => {
    const phone = match[1];
    tg.sendMessage(msg.chat.id, "Naandaa code ya pairing...");
    try {
        const code = await wa.requestPairingCode(phone);
        tg.sendMessage(msg.chat.id, `✅ Code yako ni: *${code}*\nIingize haraka kwenye WhatsApp (Linked Devices).`);
    } catch (e) {
        tg.sendMessage(msg.chat.id, "⚠️ Hitilafu: " + e.message);
    }
});

// Telegram AI Chat
tg.on('message', async (msg) => {
    if (msg.text && !msg.text.startsWith('/')) {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": msg.text}]
            })
        });
        const data = await response.json();
        if (data.choices) tg.sendMessage(msg.chat.id, data.choices[0].message.content);
    }
});

// WhatsApp AI Chat
wa.on('message', async (msg) => {
    if (msg.fromMe || !msg.body.startsWith('AI:')) return;
    const swali = msg.body.replace('AI:', '').trim();
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`, "Content-Type": "application/json" },
        body: JSON.stringify({ "model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": swali}] })
    });
    const data = await response.json();
    if (data.choices) msg.reply(data.choices[0].message.content);
});

wa.initialize();

