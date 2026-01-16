// Test connection to the backend
async function testConnection() {
  try {
    // Test the health endpoint
    const response = await fetch('https://aqsaarshi-todo-app-with-chatbot.hf.space/health');
    const healthData = await response.json();
    console.log('Health check response:', healthData);
    
    // Test the root endpoint
    const rootResponse = await fetch('https://aqsaarshi-todo-app-with-chatbot.hf.space/');
    const rootData = await rootResponse.json();
    console.log('Root endpoint response:', rootData);
    
    console.log('Connection to backend successful!');
  } catch (error) {
    console.error('Error connecting to backend:', error.message);
  }
}

testConnection();