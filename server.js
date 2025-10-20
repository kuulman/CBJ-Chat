import express from 'express';

const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.send('CBJ Chat Server is running');
});

app.post('/', (req, res) => {
    const { userId, message } = req.body;
    console.log(`Received message from ${userId}: ${message}`);
    res.status(200).json({ status: 'success', message: 'Message received' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});