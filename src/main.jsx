import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { SimulationProvider } from './context/SimulationContext.jsx'
import { SettingsProvider } from './context/SettingsContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <SettingsProvider>
      <SimulationProvider>
        <App />
      </SimulationProvider>
    </SettingsProvider>
  </React.StrictMode>,
)
