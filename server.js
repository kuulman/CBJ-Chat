import express from 'express';

const app = express();
const PORT = 3000;

app.use(express.json());

const messages = [];

app.get('/', (req, res) => {
    res.send('CBJ Chat Server is running');
    res.json({ messages });
});

app.post('/', (req, res) => {
    const { userId, timestamp, message } = req.body;
    console.log(`[${timestamp}](${userId}): ${message}`);

    messages.push({ userId, timestamp, message });

    res.status(200).json({ status: 'success', message: 'Message received' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});