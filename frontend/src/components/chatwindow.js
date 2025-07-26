import React, { useState } from 'react';
import axios from 'axios';
import Message from './message';
import '../App.css';

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message
    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post('http://localhost:5000/api/query', { 
        query: input 
      });
      setMessages(prev => [...prev, { 
        text: res.data.answer, 
        sender: 'bot' 
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        text: "Sorry, I'm having trouble connecting to the chatbot service.", 
        sender: 'bot' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
        {isLoading && (
          <Message text="Thinking" sender="bot" />
        )}
      </div>
      <form onSubmit={handleSend} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me about products, orders, or stock..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;