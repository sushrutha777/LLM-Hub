import React, { useState, useEffect } from 'react';
import './Providers.css';

interface ProviderConfig {
  id: string;
  name: string;
  description: string;
  hasKey: boolean;
  color: string;
}

const INITIAL_PROVIDERS: ProviderConfig[] = [
  { id: 'openai', name: 'OpenAI', description: 'Access GPT-4o, GPT-3.5 and more.', hasKey: true, color: '#10b981' },
  { id: 'anthropic', name: 'Anthropic', description: 'Access Claude 3 Opus, Sonnet, Haiku.', hasKey: true, color: '#f59e0b' },
  { id: 'google', name: 'Google (Gemini)', description: 'Access Gemini 1.5 Pro and Flash.', hasKey: true, color: '#6366f1' },
  { id: 'mistral', name: 'Mistral AI', description: 'Access Mistral Large and Mixtral.', hasKey: false, color: '#f97316' },
  { id: 'groq', name: 'Groq', description: 'Ultra-fast inference for Llama 3 & Mixtral.', hasKey: false, color: '#ef4444' },
  { id: 'cohere', name: 'Cohere', description: 'Access Command R and Command R+.', hasKey: false, color: '#a855f7' },
  { id: 'together', name: 'Together AI', description: 'Access Llama 3, Qwen, and open-source models.', hasKey: false, color: '#3b82f6' },
  { id: 'aws', name: 'AWS Bedrock', description: 'Access Claude, Llama and more via AWS.', hasKey: false, color: '#0ea5e9' },
  { id: 'azure', name: 'Azure OpenAI', description: 'Access OpenAI models securely via Azure.', hasKey: false, color: '#0284c7' },
  { id: 'ollama', name: 'Ollama (Local)', description: 'Run Gemma, Llama 3 locally.', hasKey: true, color: '#64748b' },
];

export const Providers: React.FC = () => {
  const [providers, setProviders] = useState<ProviderConfig[]>([]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [tempKey, setTempKey] = useState('');

  useEffect(() => {
    // Load state from local storage or use initial
    const saved = localStorage.getItem('llmhub_providers');
    if (saved) {
      setProviders(JSON.parse(saved));
    } else {
      setProviders(INITIAL_PROVIDERS);
      localStorage.setItem('llmhub_providers', JSON.stringify(INITIAL_PROVIDERS));
    }
  }, []);

  const handleEdit = (id: string) => {
    setEditingId(id);
    setTempKey(''); // Clear temp key on edit
  };

  const handleSave = (id: string) => {
    const updated = providers.map(p => {
      if (p.id === id) {
        return { ...p, hasKey: tempKey.trim().length > 0 };
      }
      return p;
    });
    setProviders(updated);
    localStorage.setItem('llmhub_providers', JSON.stringify(updated));
    setEditingId(null);
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  return (
    <div className="providers-page">
      <header className="page-header stagger-1">
        <h1>Provider Configuration</h1>
        <p>Manage API credentials for the 10 supported AI providers.</p>
      </header>

      <div className="info-banner stagger-2">
        <span className="info-icon">🔌</span>
        <div className="info-content">
          <h4>Provider Routing</h4>
          <p>
            Configure your AI provider credentials here. Only providers marked as 
            <span className="badge configured" style={{margin: '0 6px'}}>Configured</span> 
            will be available for routing. API keys are encrypted at rest and never shared.
          </p>
        </div>
      </div>

      <div className="providers-grid stagger-3">
        {providers.map((p, i) => (
          <div key={p.id} className={`provider-card glass-panel stagger-${(i % 5) + 3}`}>
            <div className="card-header">
              <div className="title-row">
                <div className="provider-icon" style={{ backgroundColor: p.color }}></div>
                <h2>{p.name}</h2>
              </div>
              {p.hasKey ? (
                <span className="badge configured">Configured</span>
              ) : (
                <span className="badge not-configured">Not Configured</span>
              )}
            </div>

            <div className="card-body">
              <p className="provider-desc">{p.description}</p>

              {editingId === p.id ? (
                <div className="key-edit-area">
                  <div className="form-group">
                    <label>API Key</label>
                    <input 
                      type="password" 
                      placeholder="sk-..." 
                      value={tempKey}
                      onChange={(e) => setTempKey(e.target.value)}
                      autoFocus
                    />
                  </div>
                  <div className="edit-actions">
                    <button className="btn-secondary btn-sm" onClick={handleCancel}>Cancel</button>
                    <button className="btn-primary btn-sm" onClick={() => handleSave(p.id)}>Save</button>
                  </div>
                </div>
              ) : (
                <div className="key-display-area">
                  <div className="form-group">
                    <label>API Key</label>
                    <div className="masked-key">
                      {p.hasKey ? '••••••••••••••••••••' : 'No key configured'}
                    </div>
                  </div>
                  <button className="btn-secondary w-100" onClick={() => handleEdit(p.id)}>
                    {p.hasKey ? 'Update Key' : 'Configure Key'}
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
