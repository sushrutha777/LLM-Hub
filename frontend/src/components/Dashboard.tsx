
import './Dashboard.css';

const metrics = [
  { title: 'Total Requests', value: '12,567', trend: '+14%', positive: true },
  { title: 'Avg Latency', value: '340 ms', trend: '-22ms', positive: true },
  { title: 'Cache Hit Rate', value: '71%', trend: '+5%', positive: true },
];

const models = [
  { name: 'Gemma', usage: '54%', color: '#6366f1' },
  { name: 'Qwen', usage: '26%', color: '#10b981' },
  { name: 'GPT-4o', usage: '12%', color: '#f59e0b' },
  { name: 'Gemini-1.5', usage: '8%', color: '#ef4444' },
];

export const Dashboard: React.FC = () => {
  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard Overview</h1>
        <p className="text-muted">Monitor your LLM infrastructure in real-time.</p>
      </header>

      <section className="metrics-grid">
        {metrics.map((m) => (
          <div key={m.title} className="metric-card glass-panel">
            <h3>{m.title}</h3>
            <div className="metric-value">
              <h2>{m.value}</h2>
              <span className={`trend ${m.positive ? 'positive' : 'negative'}`}>
                {m.trend}
              </span>
            </div>
          </div>
        ))}
      </section>

      <section className="chart-section glass-panel">
        <div className="section-header">
          <h3>Request Volume (Last 24h)</h3>
        </div>
        <div className="mock-chart">
          {[40, 70, 45, 90, 65, 80, 55, 100, 75, 85, 60, 95].map((height, i) => (
            <div key={i} className="bar-wrapper">
              <div className="bar" style={{ height: `${height}%` }}></div>
            </div>
          ))}
        </div>
      </section>

      <div className="bottom-grid">
        <section className="models-section glass-panel">
          <h3>Active Models</h3>
          <ul className="model-list">
            {models.map((model) => (
              <li key={model.name}>
                <div className="model-info">
                  <span className="dot" style={{ backgroundColor: model.color }}></span>
                  <span>{model.name}</span>
                </div>
                <strong>{model.usage}</strong>
              </li>
            ))}
          </ul>
        </section>

        <section className="providers-section glass-panel">
          <h3>Top Providers</h3>
          <div className="provider-stats">
            <div className="provider-stat">
              <span className="provider-name">Ollama (Local)</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '80%', backgroundColor: '#6366f1' }}></div>
              </div>
            </div>
            <div className="provider-stat">
              <span className="provider-name">OpenAI</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '12%', backgroundColor: '#10b981' }}></div>
              </div>
            </div>
            <div className="provider-stat">
              <span className="provider-name">Google Gemini</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '8%', backgroundColor: '#f59e0b' }}></div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};
