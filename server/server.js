import { WebSocketServer } from 'ws';
const server = new WebSocketServer({ port: 8080 });
console.log('WebSocket server started on ws://localhost:8080');

server.on('connection', socket => {
  console.log('New client connected');

  socket.on('message', message => {
    const msg = message.toString();
    console.log(`Received: ${msg}`);

    server.clients.forEach(client => {
      if (client.readyState === 1 && client !== socket) {
        client.send(msg);
      }
    });
  });

  socket.on('close', () => {
    console.log('Client disconnected');
  });
});