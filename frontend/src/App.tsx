import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import { ApiKeys } from './pages/ApiKeys'
import { AiProfiles } from './pages/AiProfiles'
import { Playground } from './pages/Playground'
import { Models } from './pages/Models'
import { Providers } from './pages/Providers'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/keys" element={<ApiKeys />} />
            <Route path="/profiles" element={<AiProfiles />} />
            <Route path="/playground" element={<Playground />} />
            <Route path="/models" element={<Models />} />
            <Route path="/providers" element={<Providers />} />
            <Route path="*" element={
              <div style={{padding: '60px 32px', textAlign: 'center'}} className="stagger-1">
                <span style={{fontSize: '48px', display: 'block', marginBottom: '16px'}}>🚧</span>
                <h2>Coming Soon</h2>
                <p className="text-muted" style={{marginTop: '8px'}}>This feature is currently under development.</p>
                <button className="btn-secondary" style={{marginTop: '24px'}} onClick={() => window.history.back()}>
                  Go Back
                </button>
              </div>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
