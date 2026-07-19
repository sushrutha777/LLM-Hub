
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import { ApiKeys } from './pages/ApiKeys'
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
            <Route path="*" element={<div style={{padding: 32}}><h2>Coming Soon</h2><p className="text-muted">This feature is under development.</p></div>} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
