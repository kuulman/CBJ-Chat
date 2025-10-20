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

    // Clear the input after entering a message
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
    console.log(`[${date.toDateString()}]: ${userInput}`);

    // Send message to server
    try {
      const response = await axios.post('http://localhost:3000/', {
        userId,
        message: userInput
      });
      console.log('Server response:', response.data);
    } catch (error) {
      console.error('Error sending message:', error.message);
    }
  }
}

(async () => {
  await chat();
})();