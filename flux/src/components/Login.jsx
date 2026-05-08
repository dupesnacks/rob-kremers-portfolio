import React, { useState } from 'react';
import '../styles/Login.css';

export default function Login({ onLoginSuccess }) {
  const [token, setToken] = useState('');
  const [showPasteForm, setShowPasteForm] = useState(false);
  const [error, setError] = useState('');

  const handleTokenSubmit = (e) => {
    e.preventDefault();
    if (!token.trim()) {
      setError('Token cannot be empty');
      return;
    }
    
    localStorage.setItem('volvo_access_token', token.trim());
    onLoginSuccess();
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>⚡ Flux</h1>
        <p className="tagline">Volvo Vehicle Control</p>

        {!showPasteForm ? (
          <div className="login-methods">
            <button className="primary-btn" onClick={() => setShowPasteForm(true)}>
              🔑 Get Started
            </button>
          </div>
        ) : (
          <form onSubmit={handleTokenSubmit} className="token-form">
            <textarea
              value={token}
              onChange={(e) => {
                setToken(e.target.value);
                setError('');
              }}
              placeholder="Paste your Volvo API token here..."
              className="token-input"
            />
            {error && <div className="error-text">{error}</div>}
            
            <div className="form-buttons">
              <button type="submit" className="submit-btn">
                ✓ Authenticate
              </button>
              <button 
                type="button" 
                className="back-btn"
                onClick={() => {
                  setShowPasteForm(false);
                  setToken('');
                  setError('');
                }}
              >
                ← Back
              </button>
            </div>
          </form>
        )}

        <div className="help-text">
          <h3>How to get your token (30 seconds):</h3>
          <ol>
            <li>
              Go to <a href="https://developer.volvocars.com/apis/docs/test-access-tokens/" target="_blank" rel="noreferrer">
                Test Access Tokens
              </a>
            </li>
            <li>
              Log in with your Volvo ID (same as My Car app)
            </li>
            <li>
              Select <strong>"Connected Vehicle"</strong> API
            </li>
            <li>
              Click <strong>"Generate"</strong> button
            </li>
            <li>
              Copy the token that appears
            </li>
            <li>
              Paste it above & hit "Authenticate"
            </li>
          </ol>
          <p className="tip">💡 Token lasts 1 hour. You'll need to regenerate it if it expires.</p>
        </div>
      </div>
    </div>
  );
}
