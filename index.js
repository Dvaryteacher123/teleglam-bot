const { default: makeWASocket, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

let sock;

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState('session_auth');
    sock = makeWASocket({ auth: state });
    sock.ev.on('creds.update', saveCreds);
}

// API Endpoint ya kupata pairing code
app.get('/pair', async (req, res) => {
    const phone = req.query.phone;
    if (!phone) return res.status(400).json({ error: "No phone number" });
    
    const code = await sock.requestPairingCode(phone);
    res.json({ pairing_code: code });
});

app.listen(PORT, () => {
    startBot();
    console.log(`WhatsApp API running on port ${PORT}`);
});
