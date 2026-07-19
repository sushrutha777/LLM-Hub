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

  return (
    <div className="apikeys-page">
      <header className="page-header">
        <h1>API Keys</h1>
        <p className="text-muted">Manage your API keys for authenticating with LLMHub.</p>
      </header>
      
      <section className="create-section glass-panel">
        <h3>Create New Key</h3>
        <form onSubmit={handleCreate} className="create-form">
          <input 
            type="text" 
            placeholder="Key Name (e.g. Production Backend)" 
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
          <button type="submit" className="btn-primary">Generate Key</button>
        </form>
      </section>

      <section className="keys-list glass-panel">
        <h3>Active Keys</h3>
        {loading ? <p>Loading...</p> : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Key</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {keys.map(k => (
                <tr key={k.id}>
                  <td>{k.name}</td>
                  <td className="key-string">{k.key}</td>
                  <td>
                    <button onClick={() => handleDelete(k.id)} className="btn-danger">Revoke</button>
                  </td>
                </tr>
              ))}
              {keys.length === 0 && (
                <tr>
                  <td colSpan={3} className="empty-state">No API keys found. Create one above!</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
};
