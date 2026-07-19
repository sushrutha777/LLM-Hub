import React, { useState, useEffect } from 'react';
import { modelsApi } from '../services/api';
import './Models.css';

export const Models: React.FC = () => {
  const [models, setModels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // We fetch real data, but if it fails or is incomplete, we could fallback
  // For now, let's just use what the API provides, which should ideally return all 10
  // Or we can augment it visually if needed.
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

  return (
    <div className="models-page">
      <header className="page-header stagger-1">
        <h1>Model Catalog</h1>
        <p>Browse all supported AI providers and their models.</p>
      </header>

      <div className="info-banner stagger-2">
        <span className="info-icon">💡</span>
        <div className="info-content">
          <h4>How Routing Works</h4>
          <p>
            When an application requests a model (e.g. <code>gpt-4o</code>), LLMHub automatically
            routes it to the correct provider. You can view all supported models below.
            Only providers with configured API keys will successfully process requests.
          </p>
        </div>
      </div>

      {loading && (
        <div className="loading-state stagger-3">
          <div className="spinner"></div>
          <p>Loading catalog...</p>
        </div>
      )}

      {error && (
        <div className="error-state stagger-3">
          <p className="text-danger">Error loading models: {error}</p>
          <button className="btn-secondary" onClick={() => window.location.reload()}>Retry</button>
        </div>
      )}

      {!loading && !error && (
        <div className="models-grid">
          {models.map((provider, i) => (
            <div key={provider.id} className={`model-card glass-panel stagger-${(i % 5) + 3}`}>
              <div className="card-header">
                <div className="title-row">
                  <h2>{provider.name}</h2>
                  {provider.free_tier && <span className="badge free">Free Tier</span>}
                </div>
                {/* Visual indicator of active status */}
                <span className={`status-dot ${provider.status}`} title={provider.status}></span>
              </div>
              
              <div className="card-body">
                <div className="meta-section">
                  <span className="label">Best For</span>
                  <p>{provider.best_for}</p>
                </div>
                
                <div className="meta-section">
                  <span className="label">Supported Models</span>
                  <div className="tags">
                    {provider.models && provider.models.length > 0 ? (
                      provider.models.map((m: string) => (
                        <span key={m} className="model-tag">{m}</span>
                      ))
                    ) : (
                      <span className="text-muted">No specific models listed</span>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="card-footer">
                <button className="btn-secondary btn-sm" onClick={() => window.location.href = '/playground'}>
                  Test in Playground
                </button>
              </div>
            </div>
          ))}
          {models.length === 0 && (
            <div className="empty-state">
              <span className="emoji">📭</span>
              <p>No providers configured in the catalog.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
