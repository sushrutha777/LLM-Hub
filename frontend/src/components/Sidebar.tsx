import React from 'react';
import './Sidebar.css';

const navItems = [
  { icon: '🏠', label: 'Dashboard', active: true },
  { icon: '💬', label: 'Playground' },
  { icon: '⚖️', label: 'Compare Models' },
  { icon: '📦', label: 'Models' },
  { icon: '📈', label: 'Analytics' },
  { icon: '📜', label: 'Logs' },
  { icon: '❤️', label: 'Health' },
  { icon: '🔑', label: 'API Keys' },
  { icon: '⚙️', label: 'Settings' },
  { icon: '👤', label: 'Profile' },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-header">
        <h2 className="text-gradient">LLMHub</h2>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <a
            key={item.label}
            href="#"
            className={`nav-item ${item.active ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
};
