import React from 'react'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Dashboard />
      </div>
    </div>
  )
}

export default App
