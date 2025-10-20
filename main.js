import promptSync from 'prompt-sync';
import axios from 'axios';

const prompt = promptSync({ sigint: true });

const userId = '001'

async function chat() {
  const date = new Date();
  console.log("CBJ-CHAT. Type 'exit' to quit.");
  while (true) {
    // Input
    process.stdout.write('Send a message: ');
    const userInput = prompt('>> ');

    // Clear the input after entering a messagehi
    process.stdout.moveCursor(0, -1);  
    process.stdout.clearLine(1);       
    process.stdout.cursorTo(0);

    // Exit condition
    if (userInput.toLowerCase() === 'exit') {
      console.log('Exiting chat. Goodbye!');
      break;
    } if (userInput.trim() === '') {
      continue; // Skip empty messages
    }

    // Output
    console.log(`[${date.toDateString()}](${userId}): ${userInput}`);

    // Send message to server
    try {
      const response = await axios.post('http://localhost:3000/', {
        userId,
        timestamp: date.toISOString(),
        message: userInput
      });
    } catch (error) {
      if (error.message === 'socket hang up' || error.code === 'EPIPE') {
        console.warn('Server is currently busy. Please try again.');
      }
      if (error.message === 'connect ECONNREFUSED') {
        console.warn('Network error. Unable to reach the server.');
      }
  }
}}

(async () => {
  await chat();
})()