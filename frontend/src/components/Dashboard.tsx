
import './Dashboard.css';

const metrics = [
  { 
    title: 'Total Requests', 
    subtitle: 'API calls processed through the gateway',
    value: '12,567', 
    trend: '+14%', 
    positive: true 
  },
  { 
    title: 'Avg Latency', 
    subtitle: 'Mean response time across all providers',
    value: '340 ms', 
    trend: '-22ms', 
    positive: true 
  },
  { 
    title: 'Cache Hit Rate', 
    subtitle: 'Percentage of requests served from Redis cache',
    value: '71%', 
    trend: '+5%', 
    positive: true 
  },
  { 
    title: 'Active Providers', 
    subtitle: 'Providers with configured API keys',
    value: '5 / 10', 
    trend: '', 
    positive: true 
  },
];

const models = [
  { name: 'Gemini 1.5 Flash', provider: 'Google', usage: '38%', color: '#6366f1' },
  { name: 'GPT-4o', provider: 'OpenAI', usage: '26%', color: '#10b981' },
  { name: 'Claude 3.5 Sonnet', provider: 'Anthropic', usage: '18%', color: '#f59e0b' },
  { name: 'Mixtral 8x7B', provider: 'Groq', usage: '12%', color: '#ef4444' },
  { name: 'Command R', provider: 'Cohere', usage: '6%', color: '#a855f7' },
];

const providers = [
  { name: 'Google Gemini', percentage: 38, color: '#6366f1' },
  { name: 'OpenAI', percentage: 26, color: '#10b981' },
  { name: 'Anthropic', percentage: 18, color: '#f59e0b' },
  { name: 'Groq', percentage: 12, color: '#ef4444' },
  { name: 'Cohere', percentage: 6, color: '#a855f7' },
];

export const Dashboard: React.FC = () => {
  return (
    <main className="dashboard">
      {/* Welcome Banner */}
      <section className="welcome-banner glass-panel stagger-1">
        <div className="welcome-content">
          <h1>Welcome to <span className="text-gradient">LLMHub</span></h1>
          <p className="text-muted">
            Your centralized AI gateway. Monitor request volumes, track latency across providers,
            manage API keys, and route traffic to 10+ AI providers — all from this admin console.
          </p>
        </div>
        <div className="welcome-stats">
          <div className="quick-stat">
            <span className="quick-stat-value">10</span>
            <span className="quick-stat-label">Providers</span>
          </div>
          <div className="quick-stat">
            <span className="quick-stat-value">99.8%</span>
            <span className="quick-stat-label">Uptime</span>
          </div>
        </div>
      </section>

      {/* Metric Cards */}
      <section className="metrics-grid">
        {metrics.map((m, i) => (
          <div key={m.title} className={`metric-card glass-panel stagger-${i + 2}`}>
            <h3>{m.title}</h3>
            <p className="metric-subtitle">{m.subtitle}</p>
            <div className="metric-value">
              <h2>{m.value}</h2>
              {m.trend && (
                <span className={`trend ${m.positive ? 'positive' : 'negative'}`}>
                  {m.trend}
                </span>
              )}
            </div>
          </div>
        ))}
      </section>

      {/* Chart Section */}
      <section className="chart-section glass-panel stagger-6">
        <div className="section-header">
          <div>
            <h3>Request Volume (Last 24h)</h3>
            <p className="section-description">Number of API requests processed each hour through the gateway.</p>
          </div>
        </div>
        <div className="mock-chart">
          {[40, 70, 45, 90, 65, 80, 55, 100, 75, 85, 60, 95].map((height, i) => (
            <div key={i} className="bar-wrapper">
              <div className="bar" style={{ height: `${height}%` }}></div>
            </div>
          ))}
        </div>
      </section>

      {/* Bottom Grid */}
      <div className="bottom-grid">
        <section className="models-section glass-panel stagger-7">
          <h3>Top Models by Usage</h3>
          <p className="section-description">Most frequently requested models across all applications.</p>
          <ul className="model-list">
            {models.map((model) => (
              <li key={model.name}>
                <div className="model-info">
                  <span className="dot" style={{ backgroundColor: model.color }}></span>
                  <div>
                    <span className="model-name">{model.name}</span>
                    <span className="model-provider">{model.provider}</span>
                  </div>
                </div>
                <strong>{model.usage}</strong>
              </li>
            ))}
          </ul>
        </section>

        <section className="providers-section glass-panel stagger-8">
          <h3>Traffic by Provider</h3>
          <p className="section-description">Percentage of total requests routed to each AI provider.</p>
          <div className="provider-stats">
            {providers.map((p) => (
              <div key={p.name} className="provider-stat">
                <div className="provider-row">
                  <span className="provider-name">{p.name}</span>
                  <span className="provider-pct">{p.percentage}%</span>
                </div>
                <div className="progress-bar">
                  <div className="progress" style={{ width: `${p.percentage}%`, backgroundColor: p.color }}></div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
};
