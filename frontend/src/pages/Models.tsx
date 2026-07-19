import React, { useState, useEffect } from 'react';
import { modelsApi } from '../services/api';
import './Models.css';

export const Models: React.FC = () => {
  const [models, setModels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await modelsApi.getModels();
        setModels(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchModels();
  }, []);

  if (loading) return <div className="p-8">Loading model catalog...</div>;
  if (error) return <div className="p-8 text-red-500">Error loading models: {error}</div>;

  return (
    <div className="models-page">
      <header className="page-header">
        <h1>Model Catalog</h1>
        <p className="text-muted">A directory of all AI providers and models natively supported by LLMHub.</p>
      </header>

      <div className="models-grid">
        {models.map((provider) => (
          <div key={provider.id} className="model-card glass-panel">
            <div className="card-header">
              <div className="title-row">
                <h2>{provider.rank}. {provider.name}</h2>
                {provider.free_tier && <span className="badge free">Free Tier</span>}
              </div>
              <span className={`status-dot ${provider.status}`} title={provider.status}></span>
            </div>
            
            <div className="card-body">
              <div className="meta-section">
                <span className="label">Best For:</span>
                <p>{provider.best_for}</p>
              </div>
              
              <div className="meta-section">
                <span className="label">Supported Models:</span>
                <div className="tags">
                  {provider.models.map((m: string) => (
                    <span key={m} className="model-tag">{m}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
