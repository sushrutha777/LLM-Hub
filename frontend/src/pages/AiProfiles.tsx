import React, { useEffect, useState } from 'react';
import { profilesApi, type AIProfile } from '../services/api';
import './AiProfiles.css';

const PROVIDER_MODELS: Record<string, string[]> = {
  google: ['gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-1.5-pro', 'gemini-1.5-flash'],
  openai: ['gpt-4.1', 'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo'],
  anthropic: ['claude-3-5-sonnet', 'claude-3-opus', 'claude-3-haiku'],
  groq: ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'],
  cohere: ['command-r', 'command-r-plus'],
  mistral: ['mistral-large-latest', 'open-mixtral-8x22b'],
  together: ['meta-llama/Llama-3-70b-chat-hf', 'Qwen/Qwen2-72B-Instruct'],
  aws: ['anthropic.claude-3-sonnet-20240229-v1:0', 'meta.llama3-70b-instruct-v1:0'],
  azure: ['azure-gpt-4o', 'azure-gpt-35-turbo'],
  ollama: ['gemma:7b', 'llama3:8b']
};

const PROVIDER_NAMES: Record<string, string> = {
  google: 'Google (Gemini)',
  openai: 'OpenAI',
  anthropic: 'Anthropic',
  groq: 'Groq',
  cohere: 'Cohere',
  mistral: 'Mistral AI',
  together: 'Together AI',
  aws: 'AWS Bedrock',
  azure: 'Azure OpenAI',
  ollama: 'Ollama (Local)'
};

export const AiProfiles: React.FC = () => {
  const [profiles, setProfiles] = useState<AIProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Form states
  const [newId, setNewId] = useState('');
  const [newName, setNewName] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newProvider, setNewProvider] = useState('google');
  const [newModel, setNewModel] = useState('gemini-1.5-pro');
  
  // Edit states
  const [editingProfile, setEditingProfile] = useState<AIProfile | null>(null);
  const [editName, setEditName] = useState('');
  const [editDesc, setEditDesc] = useState('');
  const [editProvider, setEditProvider] = useState('');
  const [editModel, setEditModel] = useState('');
  const [editActive, setEditActive] = useState(true);

  useEffect(() => {
    loadProfiles();
  }, []);

  // Update target model option list when provider selection changes
  useEffect(() => {
    if (PROVIDER_MODELS[newProvider]) {
      setNewModel(PROVIDER_MODELS[newProvider][0]);
    }
  }, [newProvider]);

  useEffect(() => {
    if (editProvider && PROVIDER_MODELS[editProvider]) {
      // Only reset editModel if it's not present in the new provider's list
      if (!PROVIDER_MODELS[editProvider].includes(editModel)) {
        setEditModel(PROVIDER_MODELS[editProvider][0]);
      }
    }
  }, [editProvider]);

  const loadProfiles = async () => {
    setLoading(true);
    try {
      const data = await profilesApi.getProfiles();
      setProfiles(data);
    } catch (e: any) {
      setError(e.message || 'Failed to load profiles');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newId || !newName) return;
    
    // Clean key ID
    const sanitizedId = newId.trim().toLowerCase().replace(/[^a-z0-9-_]/g, '-');
    
    try {
      const newProfile = await profilesApi.createProfile({
        id: sanitizedId,
        name: newName,
        description: newDesc,
        provider_id: newProvider,
        model_id: newModel,
        is_active: true
      });
      setProfiles([...profiles, newProfile]);
      
      // Reset form
      setNewId('');
      setNewName('');
      setNewDesc('');
      setNewProvider('google');
      setNewModel('gemini-1.5-pro');
    } catch (e: any) {
      alert(`Error creating profile: ${e.message}`);
    }
  };

  const handleStartEdit = (profile: AIProfile) => {
    setEditingProfile(profile);
    setEditName(profile.name);
    setEditDesc(profile.description);
    setEditProvider(profile.provider_id);
    setEditModel(profile.model_id);
    setEditActive(profile.is_active);
  };

  const handleSaveEdit = async () => {
    if (!editingProfile) return;
    try {
      const updated = await profilesApi.updateProfile(editingProfile.id, {
        name: editName,
        description: editDesc,
        provider_id: editProvider,
        model_id: editModel,
        is_active: editActive
      });
      
      setProfiles(profiles.map(p => p.id === updated.id ? updated : p));
      setEditingProfile(null);
    } catch (e: any) {
      alert(`Error updating profile: ${e.message}`);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm(`Are you sure you want to delete profile '${id}'?`)) return;
    try {
      await profilesApi.deleteProfile(id);
      setProfiles(profiles.filter(p => p.id !== id));
    } catch (e: any) {
      alert(`Error deleting profile: ${e.message}`);
    }
  };

  const toggleProfileStatus = async (profile: AIProfile) => {
    try {
      const updated = await profilesApi.updateProfile(profile.id, {
        is_active: !profile.is_active
      });
      setProfiles(profiles.map(p => p.id === updated.id ? updated : p));
    } catch (e: any) {
      alert(`Error toggling profile status: ${e.message}`);
    }
  };

  return (
    <div className="profiles-page">
      <header className="page-header stagger-1">
        <h1>AI Profiles (Logical Models)</h1>
        <p>Define stable, application-agnostic model names and map them to physical LLM backends.</p>
      </header>

      <div className="info-banner stagger-2">
        <span className="info-icon">🤖</span>
        <div className="info-content">
          <h4>Dynamic Model Routing</h4>
          <p>
            Instead of hardcoding concrete models like <code>gpt-4o</code> in client code, point your apps to logical profiles like <code>rag-chat</code>.
            As an administrator, you can hot-swap the backend provider or model at any time with zero downtime or code redeployments.
          </p>
        </div>
      </div>

      <div className="profiles-grid stagger-3">
        <div className="profiles-main">
          {/* Create Section */}
          <section className="create-section glass-panel">
            <div className="section-header">
              <h3>Create AI Profile</h3>
              <p className="section-description">Define a new logical model mapping.</p>
            </div>
            
            <form onSubmit={handleCreate} className="profile-form">
              <div className="form-row">
                <div className="form-group flex-1">
                  <label>Profile Identifier (API Name)</label>
                  <input 
                    type="text" 
                    placeholder="e.g. invoice-extractor" 
                    value={newId}
                    onChange={e => setNewId(e.target.value)}
                    required
                  />
                  <small className="form-help">Use only letters, numbers, hyphens, and underscores.</small>
                </div>
                
                <div className="form-group flex-1">
                  <label>Display Name</label>
                  <input 
                    type="text" 
                    placeholder="e.g. Invoice Extractor" 
                    value={newName}
                    onChange={e => setNewName(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group flex-1">
                  <label>Target Provider</label>
                  <select value={newProvider} onChange={e => setNewProvider(e.target.value)}>
                    {Object.keys(PROVIDER_NAMES).map(p => (
                      <option key={p} value={p}>{PROVIDER_NAMES[p]}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group flex-1">
                  <label>Target Model</label>
                  <select value={newModel} onChange={e => setNewModel(e.target.value)}>
                    {(PROVIDER_MODELS[newProvider] || []).map(m => (
                      <option key={m} value={m}>{m}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea 
                  placeholder="Describe the purpose of this profile..." 
                  value={newDesc}
                  onChange={e => setNewDesc(e.target.value)}
                  rows={2}
                />
              </div>

              <button type="submit" className="btn-primary mt-2">
                Create Profile
              </button>
            </form>
          </section>

          {/* List Section */}
          <section className="profiles-list-section glass-panel stagger-4">
            <div className="section-header">
              <h3>Configured Profiles</h3>
              <p className="section-description">Manage your active logical profiles.</p>
            </div>

            {loading ? (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Loading AI Profiles...</p>
              </div>
            ) : error ? (
              <div className="error-state">
                <p className="text-danger">{error}</p>
                <button className="btn-secondary" onClick={loadProfiles}>Retry</button>
              </div>
            ) : (
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Profile ID</th>
                      <th>Name / Desc</th>
                      <th>Target Backend</th>
                      <th>Status</th>
                      <th style={{ width: '150px' }}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {profiles.map(p => (
                      <tr key={p.id}>
                        <td>
                          <code className="profile-id-badge">{p.id}</code>
                        </td>
                        <td>
                          <div className="profile-info-cell">
                            <strong>{p.name}</strong>
                            {p.description && <span className="profile-desc-text">{p.description}</span>}
                          </div>
                        </td>
                        <td>
                          <div className="backend-target">
                            <span className="provider-tag">{PROVIDER_NAMES[p.provider_id] || p.provider_id}</span>
                            <span className="arrow">→</span>
                            <code className="model-tag-small">{p.model_id}</code>
                          </div>
                        </td>
                        <td>
                          <button 
                            className={`badge ${p.is_active ? 'active' : 'warning'}`}
                            onClick={() => toggleProfileStatus(p)}
                            title="Click to toggle status"
                            style={{ cursor: 'pointer', border: 'none' }}
                          >
                            {p.is_active ? 'Active' : 'Inactive'}
                          </button>
                        </td>
                        <td>
                          <div className="action-buttons">
                            <button className="btn-secondary btn-sm" onClick={() => handleStartEdit(p)}>
                              Edit
                            </button>
                            <button className="btn-danger" onClick={() => handleDelete(p.id)}>
                              Revoke
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {profiles.length === 0 && (
                      <tr>
                        <td colSpan={5} className="empty-state">
                          <span className="emoji">⚙️</span>
                          <p>No AI Profiles configured. Create one above to get started!</p>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>

        {/* Sidebar / Quick Start */}
        <aside className="profiles-sidebar stagger-5">
          <div className="glass-panel instruction-panel">
            <h3>API Integration</h3>
            <p className="section-description">How to use AI Profiles in your code.</p>
            
            <div className="instruction-step">
              <span className="step-num">1</span>
              <p>Reference the stable Profile ID as the <code>model</code> parameter in your API request payload.</p>
            </div>
            
            <div className="code-snippet-container">
              <span className="snippet-label">Python Request</span>
              <div className="code-snippet">
                <pre>
{`import openai

client = openai.OpenAI(
    api_key="your-llmhub-key",
    base_url="http://localhost:8000/v1"
)

# Use stable logical model name
completion = client.chat.completions.create(
    model="rag-chat",
    messages=[{"role": "user", "content": "Hi!"}]
)`}
                </pre>
              </div>
            </div>

            <div className="instruction-step mt-4">
              <span className="step-num">2</span>
              <p>LLMHub dynamically intercepts the request and routes it to the target backend (e.g. Gemini 2.5 Pro) with zero latency.</p>
            </div>
          </div>
        </aside>
      </div>

      {/* Edit Modal / Backdrop */}
      {editingProfile && (
        <div className="modal-backdrop">
          <div className="modal-content glass-panel">
            <div className="modal-header">
              <h2>Edit AI Profile: {editingProfile.id}</h2>
              <button className="btn-icon" onClick={() => setEditingProfile(null)}>×</button>
            </div>
            
            <div className="modal-body">
              <div className="form-group">
                <label>Display Name</label>
                <input 
                  type="text" 
                  value={editName}
                  onChange={e => setEditName(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea 
                  value={editDesc}
                  onChange={e => setEditDesc(e.target.value)}
                  rows={2}
                />
              </div>

              <div className="form-row">
                <div className="form-group flex-1">
                  <label>Target Provider</label>
                  <select value={editProvider} onChange={e => setEditProvider(e.target.value)}>
                    {Object.keys(PROVIDER_NAMES).map(p => (
                      <option key={p} value={p}>{PROVIDER_NAMES[p]}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group flex-1">
                  <label>Target Model</label>
                  <select value={editModel} onChange={e => setEditModel(e.target.value)}>
                    {(PROVIDER_MODELS[editProvider] || []).map(m => (
                      <option key={m} value={m}>{m}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group check-group">
                <label className="checkbox-label">
                  <input 
                    type="checkbox" 
                    checked={editActive}
                    onChange={e => setEditActive(e.target.checked)}
                  />
                  <span>Active & Routing Enabled</span>
                </label>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setEditingProfile(null)}>Cancel</button>
              <button className="btn-primary" onClick={handleSaveEdit}>Save Changes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
