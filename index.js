const { Client, LocalAuth } = require('whatsapp-web.js');
const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');
require('dotenv').config();

const tg = new TelegramBot(process.env.TELEGRAM_TOKEN, { polling: true });

// Tumeondoa puppeteer configuration ngumu ili itumie defaults za mfumo
const wa = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    }
});

// Telegram inajibu sasa bila kusubiri WhatsApp iwake
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

wa.on('ready', () => console.log('WhatsApp Bot iko tayari!'));
wa.initialize().catch(err => console.log("WhatsApp imefeli kuanza, lakini Telegram bado inafanya kazi."));

