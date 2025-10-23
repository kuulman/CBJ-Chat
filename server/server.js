import { WebSocketServer } from 'ws';
const server = new WebSocketServer({ port: 8080 });
console.log('WebSocket server started on ws://localhost:8080');

server.on('connection', socket => {
  console.log('New client connected');

  socket.on('message', message => {
    console.log(`Received: ${message}`);
    // Echo the message back to the client
    socket.send(`Server received: ${message}`);
  });

  socket.on('close', () => {
    console.log('Client disconnected');
  });
});