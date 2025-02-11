import React, { useState } from 'react';
import { chat } from '../services/authService';
import '../styles/Chat.css';

function Chat() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    try {
      const data = await chat(message);
      setResponse(data.response);
      
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message"
          className="chat-input"
        />
        <button type="submit" className="chat-button">
          {loading ? <div className="spinner"></div> : 'Send'}
        </button>
      </form>
      <div className="chat-response">
        <h3>Response:</h3>
        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
          </div>
        ) : (
          <p>{response}</p>
        )}
      </div>
    </div>
  );
}

export default Chat;
