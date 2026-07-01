const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('.'));

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
if (!OPENROUTER_API_KEY) {
    console.error('❌ OPENROUTER_API_KEY haijapatikana kwenye environment!');
    process.exit(1);
}

app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    if (!message) {
        return res.status(400).json({ error: 'Ujumbe unahitajika.' });
    }

    try {
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
                'HTTP-Referer': 'https://your-app.onrender.com',
                'X-Title': 'DVARY Termux Master'
            },
            body: JSON.stringify({
                model: 'google/gemini-2.0-flash-lite-preview-02-05:free',
                messages: [
                    {
                        role: 'system',
                        content: `Wewe ni msaidizi wa Termux Master Pro. Unajua kila kitu kuhusu Termux, commands, hacking tools, bot creation, na mbinu za usalama. Jibu kwa Kiswahili kilichochanganyika na Kiingereza (Swahili + English). Toa maelezo ya hatua kwa hatua, na uonyeshe commands kwa code blocks. Usijibu maswali yasiyohusiana na Termux au programming. Weka maelezo mafupi na yenye maana.`
                    },
                    { role: 'user', content: message }
                ],
                max_tokens: 700,
                temperature: 0.7
            })
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error?.message || 'OpenRouter error (HTTP ' + response.status + ')');
        }

        const data = await response.json();
        const reply = data.choices?.[0]?.message?.content || 'Samahani, sikupata jibu.';
        res.json({ reply });
    } catch (error) {
        console.error('AI error:', error);
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => {
    console.log(`✅ Server inaendesha kwenye port ${port}`);
});
