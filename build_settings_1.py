import os
import re

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 1. SETTINGS CONTEXT
settings_context_code = """import React, { createContext, useState, useEffect } from 'react';

export const SettingsContext = createContext();

export const SettingsProvider = ({ children }) => {
  const defaultSettings = {
    theme: 'dark', // dark, light, system
    experimentMode: 'easy', // easy, medium, hard
    buzzerSound: true,
    alertSounds: true,
    volume: 0.7,
    simulationSpeed: 'normal',
    autoStart: false,
    sensorAnimations: true,
    circuitAnimations: true,
    requireValidation: true,
    reduceAnimations: false,
    highContrast: false,
    largerText: false,
    dashboardPrefs: {
      showTemperature: true,
      showSmoke: true,
      showHumidity: true,
      showAiConfidence: true,
      showBuzzer: true,
      showIoT: true,
      showTrends: true
    }
  };

  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('fireguard_settings');
    return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
  });

  useEffect(() => {
    localStorage.setItem('fireguard_settings', JSON.stringify(settings));
    
    // Apply theme
    let activeTheme = settings.theme;
    if (activeTheme === 'system') {
      activeTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    if (activeTheme === 'light') {
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
    }
  }, [settings]);

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const updateDashboardPref = (key, value) => {
    setSettings(prev => ({
      ...prev,
      dashboardPrefs: { ...prev.dashboardPrefs, [key]: value }
    }));
  };

  const resetAllSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings(defaultSettings);
    }
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, updateDashboardPref, resetAllSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};
"""
write_file('src/context/SettingsContext.jsx', settings_context_code)

# 2. UPDATE APP.JSX
app_jsx_code = """import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import VirtualCircuit from './pages/VirtualCircuit';
import ExperimentLab from './pages/ExperimentLab';
import AIClassifier from './pages/AIClassifier';
import IoTDashboard from './pages/IoTDashboard';
import Analytics from './pages/Analytics';
import History from './pages/History';
import About from './pages/About';
import Guidelines from './pages/Guidelines';
import Settings from './pages/Settings';
import NotificationsPage from './pages/NotificationsPage';
import { SimulationProvider } from './context/SimulationContext';
import { SettingsProvider } from './context/SettingsContext';

function App() {
  return (
    <SettingsProvider>
      <SimulationProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/guidelines" element={<Guidelines />} />
              <Route path="/circuit" element={<VirtualCircuit />} />
              <Route path="/lab" element={<ExperimentLab />} />
              <Route path="/ai" element={<AIClassifier />} />
              <Route path="/iot" element={<IoTDashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/history" element={<History />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/notifications" element={<NotificationsPage />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </Layout>
        </Router>
      </SimulationProvider>
    </SettingsProvider>
  );
}

export default App;
"""
write_file('src/App.jsx', app_jsx_code)

print("Created Context and Updated App.jsx")
