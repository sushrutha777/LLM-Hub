
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const navItems = [
  { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
  { icon: '💬', label: 'Playground', path: '/playground' },
  { icon: '⚖️', label: 'Compare Models', path: '/compare' },
  { icon: '📦', label: 'Models', path: '/models' },
  { icon: '📈', label: 'Analytics', path: '/analytics' },
  { icon: '📜', label: 'Logs', path: '/logs' },
  { icon: '❤️', label: 'Health', path: '/health' },
  { icon: '🔑', label: 'API Keys', path: '/keys' },
  { icon: '⚙️', label: 'Settings', path: '/settings' },
  { icon: '👤', label: 'Profile', path: '/profile' },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-header">
        <h2 className="text-gradient">LLMHub</h2>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.label}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
