import React, { useEffect, useState } from 'react';
import { adminApi, type APIKey } from '../services/api';
import './ApiKeys.css';

export const ApiKeys: React.FC = () => {
  const [keys, setKeys] = useState<APIKey[]>([]);
  const [newName, setNewName] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    setLoading(true);
    try {
      const data = await adminApi.getKeys();
      setKeys(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName) return;
    try {
      const newKey = await adminApi.createKey(newName);
      setKeys([...keys, newKey]);
      setNewName('');
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await adminApi.deleteKey(id);
      setKeys(keys.filter(k => k.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Visual feedback could be added here
  };

  return (
    <div className="apikeys-page">
      <header className="page-header stagger-1">
        <h1>API Keys</h1>
        <p>Manage authentication keys for your applications connecting to LLMHub.</p>
      </header>

      <div className="info-banner stagger-2">
        <span className="info-icon">🔑</span>
        <div className="info-content">
          <h4>Authentication</h4>
          <p>
            API Keys are used to authenticate your applications with LLMHub. 
            Pass the key in the <code>Authorization</code> header of your HTTP requests. 
            Keep your keys secure and do not share them in public repositories.
          </p>
        </div>
      </div>
      
      <div className="apikeys-grid stagger-3">
        <div className="apikeys-main">
          <section className="create-section glass-panel">
            <div className="section-header">
              <h3>Create New Key</h3>
              <p className="section-description">Generate a new key for a specific application or environment.</p>
            </div>
            
            <form onSubmit={handleCreate} className="create-form">
              <input 
                type="text" 
                placeholder="Key Name (e.g. Production Backend)" 
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
              />
              <button type="submit" className="btn-primary" disabled={!newName.trim()}>
                Generate Key
              </button>
            </form>
          </section>

          <section className="keys-list glass-panel stagger-4">
            <div className="section-header">
              <h3>Active Keys</h3>
              <p className="section-description">Keys currently authorized to make requests to the gateway.</p>
            </div>
            
            {loading ? (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Loading keys...</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Key</th>
                      <th style={{width: '100px'}}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {keys.map(k => (
                      <tr key={k.id}>
                        <td className="key-name">{k.name}</td>
                        <td>
                          <div className="key-value-container">
                            <code className="key-string">{k.key}</code>
                            <button 
                              className="btn-icon copy-btn" 
                              onClick={() => copyToClipboard(k.key)}
                              title="Copy to clipboard"
                            >
                              📋
                            </button>
                          </div>
                        </td>
                        <td>
                          <button onClick={() => handleDelete(k.id)} className="btn-danger">
                            Revoke
                          </button>
                        </td>
                      </tr>
                    ))}
                    {keys.length === 0 && (
                      <tr>
                        <td colSpan={3} className="empty-state">
                          <span className="emoji">🛡️</span>
                          <p>No API keys found. Create one above to get started!</p>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>

        <aside className="apikeys-sidebar stagger-5">
          <div className="glass-panel quick-start-panel">
            <h3>Quick Start</h3>
            <p className="section-description">How to use your API key in a request.</p>
            
            <div className="code-snippet-container">
              <span className="snippet-label">cURL Example</span>
              <div className="code-snippet">
                <button 
                  className="copy-btn" 
                  onClick={() => copyToClipboard('curl -X POST http://localhost:8000/v1/chat/completions \\\n  -H "Authorization: YOUR_API_KEY" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello!"}]}\'')}
                >
                  Copy
                </button>
                <pre>
{`curl -X POST http://localhost:8000/v1/chat/completions \\
  -H "Authorization: YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'`}
                </pre>
              </div>
            </div>
            
            <div className="docs-link mt-4">
              <a href="#" className="text-info">View full API documentation →</a>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};
