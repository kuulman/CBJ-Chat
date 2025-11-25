import { WebSocketServer } from 'ws';
import { createClient } from '@supabase/supabase-js'
import dotenv from 'dotenv';
dotenv.config({ path: '../.env' })

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

const server = new WebSocketServer({ port: 8080 });
console.log('WebSocket server started on ws://localhost:8080');
const connectedUsers = new Map() // Save currently user online


server.on('connection', socket => {
  socket.on('message', async message => {
    const data = JSON.parse(message)

    /* When client online, they will send init for identification */
    if (data.type === 'init') {
      const { secret_id } = data
      connectedUsers.set(secret_id, socket)
      socket.secret_id = secret_id
      console.log(secret_id)
      return
    }

    /* For client send a message */
    if (data.type === 'message') {
      // Get room id
      const rawRoomID = [socket.secret_id, data.to].map(String).sort().join('@') // Create room id by sorting user IDs
      const room = Buffer.from(rawRoomID, 'utf-8').toString('base64') // Encode room id to base64

      const { to, msg } = data
      const { data: roomData, error } = await supabase
        .from('rooms')
        .select('*')
        .eq('room_id', room)
      if (error) {
        console.error('Error: ', error)
        return
      }
      
      if (!roomData || roomData.length === 0) {
        const { data: newRoom, error: newRoomError } = await supabase
          .from('rooms')
          .insert({
            room_id: room,
            type: 'private',
            members: [socket.secret_id, to],
          })
        if (newRoomError) {
          console.error('Error creating room:', newRoomError)
          return
        }
      }

      console.log(`${room}: ${msg}`)

      if (connectedUsers.has(to)) {
        connectedUsers.get(to).send(JSON.stringify({
          room: room,
          from: socket.secret_id,
          to: to,
          message: msg
        }))
      }
    }
  });

  /* Delete when client off */
  socket.on('close', () => {
    connectedUsers.delete(socket.secret_id)
    console.log('Client disconnected');
  });
});