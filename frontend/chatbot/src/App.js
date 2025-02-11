import React, { useState } from 'react';
import Signup from './components/Signup';
import Login from './components/Login';
import Chat from './components/Chat';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleSignup = () => {
    setShowSignup(false);
  };

  return (
    <div className="App">
      <h1>RAG System</h1>
      {!isLoggedIn ? (
        <>
          {showSignup ? (
            <Signup onSignup={handleSignup} />
          ) : (
            <Login onLogin={handleLogin} />
          )}
          <button onClick={() => setShowSignup(!showSignup)}>
            {showSignup ? 'Already have an account? Login' : 'Need an account? Sign Up'}
          </button>
        </>
      ) : (
        <Chat />
      )}
    </div>
  );
}

export default App;