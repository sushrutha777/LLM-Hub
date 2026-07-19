
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const navSections = [
  {
    label: 'MAIN',
    items: [
      { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
      { icon: '💬', label: 'Playground', path: '/playground' },
      { icon: '⚖️', label: 'Compare Models', path: '/compare' },
    ],
  },
  {
    label: 'MANAGEMENT',
    items: [
      { icon: '📦', label: 'Models', path: '/models' },
      { icon: '🔌', label: 'Providers', path: '/providers' },
      { icon: '🤖', label: 'AI Profiles', path: '/profiles' },
      { icon: '🔑', label: 'API Keys', path: '/keys' },
    ],
  },
  {
    label: 'SYSTEM',
    items: [
      { icon: '📈', label: 'Analytics', path: '/analytics' },
      { icon: '📜', label: 'Logs', path: '/logs' },
      { icon: '❤️', label: 'Health', path: '/health' },
      { icon: '⚙️', label: 'Settings', path: '/settings' },
    ],
  },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-header">
        <h2 className="text-gradient">LLMHub</h2>
        <span className="sidebar-subtitle">Admin Console</span>
      </div>
      <nav className="sidebar-nav">
        {navSections.map((section) => (
          <div key={section.label} className="nav-section">
            <span className="nav-section-label">{section.label}</span>
            {section.items.map((item) => (
              <NavLink
                key={item.label}
                to={item.path}
                className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="version-badge">
          <span className="version-dot"></span>
          LLMHub v1.0
        </div>
      </div>
    </aside>
  );
};
