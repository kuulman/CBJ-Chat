import { json } from 'express';
import { WebSocketServer } from 'ws';
const server = new WebSocketServer({ port: 8080 });
console.log('WebSocket server started on ws://localhost:8080');
const connectedUsers = new Map()

server.on('connection', socket => {
  socket.on('message', message => {
    const data = JSON.parse(message)

    if (data.type === 'init') {
      const { secret_id } = data
      connectedUsers.set(secret_id, socket)
      socket.secret_id = secret_id
      console.log(secret_id)
      return 
    }

    if (data.type === 'message') {
      const { to, msg } = data
      if (connectedUsers.has(to)) {
        connectedUsers.get(to).send(JSON.stringify({
          from: socket.secret_id,
          to: to,
          message: msg
        }))
      }
    }
  });

  socket.on('close', () => {
    connectedUsers.delete(socket.secret_id)
    console.log('Client disconnected');
  });
});