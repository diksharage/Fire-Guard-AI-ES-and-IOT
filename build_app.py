import os
import json

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

files = {}

files["tailwind.config.js"] = """
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',
        darker: '#020617',
        card: '#1e293b',
        primary: '#f97316', // Orange
        danger: '#ef4444',
        warning: '#eab308',
        safe: '#22c55e'
      }
    },
  },
  plugins: [],
}
"""

files["src/index.css"] = """
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-darker text-slate-200 overflow-x-hidden;
}

.glass-card {
  @apply bg-card/80 backdrop-blur-md border border-slate-700/50 rounded-xl shadow-xl;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #020617; 
}
::-webkit-scrollbar-thumb {
  background: #334155; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #475569; 
}
"""

files["src/main.jsx"] = """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { SimulationProvider } from './context/SimulationContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <SimulationProvider>
      <App />
    </SimulationProvider>
  </React.StrictMode>,
)
"""

files["src/App.jsx"] = """
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import VirtualCircuit from './pages/VirtualCircuit';
import ExperimentLab from './pages/ExperimentLab';
import AIClassifier from './pages/AIClassifier';
import IoTDashboard from './pages/IoTDashboard';
import Analytics from './pages/Analytics';
import History from './pages/History';
import About from './pages/About';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/circuit" element={<VirtualCircuit />} />
          <Route path="/lab" element={<ExperimentLab />} />
          <Route path="/ai" element={<AIClassifier />} />
          <Route path="/iot" element={<IoTDashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
"""

files["src/context/SimulationContext.jsx"] = """
import React, { createContext, useState, useEffect, useRef } from 'react';

export const SimulationContext = createContext();

export const SimulationProvider = ({ children }) => {
  const [temperature, setTemperature] = useState(30.0);
  const [smoke, setSmoke] = useState(100.0);
  
  const [targetTemp, setTargetTemp] = useState(30.0);
  const [targetSmoke, setTargetSmoke] = useState(100.0);

  const [tempRate, setTempRate] = useState(0);
  const [smokeRate, setSmokeRate] = useState(0);

  const [riskLevel, setRiskLevel] = useState(0); // 0=Normal, 1=Warning, 2=High Risk
  const [confidence, setConfidence] = useState(98);

  const [metricsHistory, setMetricsHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [experiments, setExperiments] = useState(JSON.parse(localStorage.getItem('fireguard_experiments') || '[]'));
  
  const [isRunning, setIsRunning] = useState(true);
  const [demoMode, setDemoMode] = useState(false);
  const [demoStage, setDemoStage] = useState(0);
  
  const prevTempRef = useRef(30.0);
  const prevSmokeRef = useRef(100.0);

  // Persistence
  useEffect(() => {
    localStorage.setItem('fireguard_experiments', JSON.stringify(experiments));
  }, [experiments]);

  // Main simulation loop
  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      // Add slight noise
      const tempNoise = (Math.random() - 0.5) * 0.4;
      const smokeNoise = (Math.random() - 0.5) * 5;

      // Move current towards target
      let newTemp = temperature + (targetTemp - temperature) * 0.1 + tempNoise;
      let newSmoke = smoke + (targetSmoke - smoke) * 0.1 + smokeNoise;

      // Bound values
      newTemp = Math.max(10, Math.min(100, newTemp));
      newSmoke = Math.max(0, Math.min(1000, newSmoke));

      // Calculate rates
      const currentTempRate = (newTemp - prevTempRef.current);
      const currentSmokeRate = (newSmoke - prevSmokeRef.current);

      setTempRate(currentTempRate);
      setSmokeRate(currentSmokeRate);

      // AI Logic - Decision Tree
      let newRisk = 0;
      let conf = 95;

      if (newTemp > 50 && newSmoke > 600) {
        newRisk = 2; // High Risk
        conf = 98;
      } else if (newTemp > 55 || newSmoke > 700) {
        newRisk = 2;
        conf = 94;
      } else if (newTemp > 40 || newSmoke > 300 || currentTempRate > 1.5 || currentSmokeRate > 20) {
        newRisk = 1; // Warning
        conf = 88;
      } else {
        newRisk = 0; // Normal
        conf = 96;
      }

      setTemperature(newTemp);
      setSmoke(newSmoke);
      setRiskLevel(newRisk);
      setConfidence(conf);
      
      prevTempRef.current = newTemp;
      prevSmokeRef.current = newSmoke;

      // Update charts
      setMetricsHistory(prev => {
        const newHist = [...prev, {
          time: new Date().toLocaleTimeString(),
          temperature: parseFloat(newTemp.toFixed(1)),
          smoke: Math.round(newSmoke),
          risk: newRisk
        }];
        if (newHist.length > 30) newHist.shift(); // Keep last 30 points
        return newHist;
      });

      // Handle Alerts
      if (newRisk === 2) {
        setAlerts(prev => {
          // Prevent spamming alerts every tick
          const lastAlert = prev[0];
          if (!lastAlert || (Date.now() - lastAlert.timestamp > 10000)) {
            return [{
              id: Date.now(),
              timestamp: Date.now(),
              message: "HIGH FIRE RISK DETECTED!",
              temp: newTemp.toFixed(1),
              smoke: Math.round(newSmoke)
            }, ...prev].slice(0, 50);
          }
          return prev;
        });
      }

    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, temperature, smoke, targetTemp, targetSmoke]);

  // Demo mode sequence
  useEffect(() => {
    if (!demoMode) return;
    
    let timer;
    if (demoStage === 0) {
      setTargetTemp(30); setTargetSmoke(100);
      timer = setTimeout(() => setDemoStage(1), 5000);
    } else if (demoStage === 1) { // Smoke increase
      setTargetSmoke(450);
      timer = setTimeout(() => setDemoStage(2), 8000);
    } else if (demoStage === 2) { // Temp increase (Combined)
      setTargetTemp(65); setTargetSmoke(850);
      timer = setTimeout(() => setDemoStage(3), 8000);
    } else if (demoStage === 3) { // Reset
      setTargetTemp(30); setTargetSmoke(100);
      timer = setTimeout(() => { setDemoMode(false); setDemoStage(0); }, 5000);
    }

    return () => clearTimeout(timer);
  }, [demoMode, demoStage]);

  const resetSimulation = () => {
    setTargetTemp(30);
    setTargetSmoke(100);
    setTemperature(30);
    setSmoke(100);
    setRiskLevel(0);
    setMetricsHistory([]);
    setDemoMode(false);
    setDemoStage(0);
  };

  const addExperimentResult = (name, result) => {
    const newExp = {
      id: Date.now(),
      name,
      date: new Date().toLocaleString(),
      maxTemp: temperature.toFixed(1),
      maxSmoke: Math.round(smoke),
      result,
      status: 'Completed'
    };
    setExperiments(prev => [newExp, ...prev]);
  };

  const clearHistory = () => {
    setExperiments([]);
  };

  return (
    <SimulationContext.Provider value={{
      temperature, smoke, targetTemp, targetSmoke,
      setTargetTemp, setTargetSmoke,
      tempRate, smokeRate,
      riskLevel, confidence,
      metricsHistory, alerts, experiments, addExperimentResult, clearHistory,
      isRunning, setIsRunning,
      resetSimulation,
      demoMode, setDemoMode, demoStage
    }}>
      {children}
    </SimulationContext.Provider>
  );
};
"""

files["src/components/Layout.jsx"] = """
import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Flame, LayoutDashboard, Cpu, FlaskConical, BrainCircuit, Wifi, BarChart3, History, Info, Menu, X, Bell } from 'lucide-react';
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { riskLevel, alerts } = useContext(SimulationContext);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { path: '/circuit', label: 'Virtual Circuit', icon: <Cpu size={20} /> },
    { path: '/lab', label: 'Experiment Lab', icon: <FlaskConical size={20} /> },
    { path: '/ai', label: 'AI Classifier', icon: <BrainCircuit size={20} /> },
    { path: '/iot', label: 'IoT Monitoring', icon: <Wifi size={20} /> },
    { path: '/analytics', label: 'Sensor Analytics', icon: <BarChart3 size={20} /> },
    { path: '/history', label: 'History', icon: <History size={20} /> },
    { path: '/about', label: 'About System', icon: <Info size={20} /> },
  ];

  return (
    <div className="flex h-screen bg-darker overflow-hidden font-sans">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-card border-r border-slate-800 transition-transform duration-300 md:relative md:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center justify-between p-4 border-b border-slate-800">
          <div className="flex items-center gap-2 text-primary font-bold text-xl">
            <Flame className="text-orange-500 animate-pulse" />
            FireGuard AI
          </div>
          <button onClick={() => setSidebarOpen(false)} className="md:hidden text-slate-400 hover:text-white">
            <X size={24} />
          </button>
        </div>
        <div className="p-2 text-xs text-slate-500 uppercase font-semibold tracking-wider">Virtual Laboratory</div>
        <nav className="p-2 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) => 
                `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                  isActive ? 'bg-primary/10 text-primary font-medium' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`
              }
            >
              {item.icon}
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8 bg-card/50 backdrop-blur-sm border-b border-slate-800 shrink-0">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebarOpen(true)} className="md:hidden text-slate-400 hover:text-white">
              <Menu size={24} />
            </button>
            <div className="hidden sm:flex flex-col">
              <h1 className="text-sm font-semibold text-slate-200">Virtual Fire & Smoke Early Warning Laboratory</h1>
              <span className="text-xs text-slate-400">Simulation Environment</span>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${riskLevel === 2 ? 'bg-red-400' : riskLevel === 1 ? 'bg-yellow-400' : 'bg-green-400'}`}></span>
                <span className={`relative inline-flex rounded-full h-3 w-3 ${riskLevel === 2 ? 'bg-red-500' : riskLevel === 1 ? 'bg-yellow-500' : 'bg-green-500'}`}></span>
              </span>
              <span className="text-sm font-medium text-slate-300">
                {riskLevel === 2 ? 'HIGH RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL'}
              </span>
            </div>
            <div className="relative">
              <Bell size={20} className="text-slate-400" />
              {alerts.length > 0 && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] text-white font-bold">
                  {alerts.length > 9 ? '9+' : alerts.length}
                </span>
              )}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};
export default Layout;
"""

files["src/components/Controls.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Play, Square, RotateCcw, Zap } from 'lucide-react';

const Controls = () => {
  const { 
    targetTemp, setTargetTemp, targetSmoke, setTargetSmoke,
    isRunning, setIsRunning, resetSimulation,
    demoMode, setDemoMode
  } = useContext(SimulationContext);

  return (
    <div className="glass-card p-6 mt-6">
      <div className="flex flex-col md:flex-row gap-8">
        
        {/* Sliders */}
        <div className="flex-1 space-y-6">
          <h3 className="text-lg font-semibold text-slate-200 border-b border-slate-700 pb-2">Environment Controls</h3>
          
          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium text-slate-400">Target Temperature (°C)</label>
              <span className="text-sm font-bold text-orange-400">{targetTemp}°C</span>
            </div>
            <input 
              type="range" min="10" max="100" step="1" 
              value={targetTemp} 
              onChange={(e) => setTargetTemp(Number(e.target.value))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-orange-500"
              disabled={demoMode}
            />
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium text-slate-400">Target Smoke Level (ppm)</label>
              <span className="text-sm font-bold text-slate-300">{targetSmoke}</span>
            </div>
            <input 
              type="range" min="0" max="1000" step="10" 
              value={targetSmoke} 
              onChange={(e) => setTargetSmoke(Number(e.target.value))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-400"
              disabled={demoMode}
            />
          </div>
        </div>

        {/* Presets & Actions */}
        <div className="flex-1 space-y-4">
          <h3 className="text-lg font-semibold text-slate-200 border-b border-slate-700 pb-2">Presets & Actions</h3>
          
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => { setTargetTemp(30); setTargetSmoke(100); }} disabled={demoMode} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm rounded-lg border border-slate-600 transition">Normal Environment</button>
            <button onClick={() => { setTargetTemp(32); setTargetSmoke(450); }} disabled={demoMode} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm rounded-lg border border-slate-600 transition">Smoke Detected</button>
            <button onClick={() => { setTargetTemp(60); setTargetSmoke(120); }} disabled={demoMode} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm rounded-lg border border-slate-600 transition">High Temperature</button>
            <button onClick={() => { setTargetTemp(70); setTargetSmoke(850); }} disabled={demoMode} className="px-4 py-2 bg-red-900/30 hover:bg-red-800/50 text-sm text-red-200 rounded-lg border border-red-700/50 transition">Combined Fire Risk</button>
          </div>

          <div className="flex gap-3 pt-2">
            <button 
              onClick={() => setIsRunning(!isRunning)}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg font-medium transition ${isRunning ? 'bg-slate-700 hover:bg-slate-600 text-white' : 'bg-green-600 hover:bg-green-500 text-white'}`}
            >
              {isRunning ? <><Square size={18} /> Pause Sim</> : <><Play size={18} /> Resume Sim</>}
            </button>
            <button 
              onClick={resetSimulation}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition"
            >
              <RotateCcw size={18} /> Reset
            </button>
            <button 
              onClick={() => setDemoMode(!demoMode)}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg font-medium transition ${demoMode ? 'bg-primary text-white animate-pulse' : 'bg-slate-800 text-primary border border-primary/50'}`}
            >
              <Zap size={18} /> {demoMode ? 'Stop Demo' : 'Demo Mode'}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
export default Controls;
"""

files["src/pages/Dashboard.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Thermometer, Wind, AlertTriangle, ShieldCheck, Activity, Brain, Volume2, VolumeX, Flame } from 'lucide-react';
import Controls from '../components/Controls';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const { temperature, smoke, riskLevel, confidence, metricsHistory } = useContext(SimulationContext);

  const getRiskDisplay = () => {
    if (riskLevel === 2) return { text: 'HIGH FIRE RISK', color: 'text-red-500', bg: 'bg-red-500/10', border: 'border-red-500/50', icon: <Flame size={48} className="text-red-500 animate-pulse" />, msg: 'Immediate attention required. Evacuate area.' };
    if (riskLevel === 1) return { text: 'WARNING', color: 'text-yellow-500', bg: 'bg-yellow-500/10', border: 'border-yellow-500/50', icon: <AlertTriangle size={48} className="text-yellow-500" />, msg: 'Abnormal environmental conditions detected.' };
    return { text: 'NORMAL', color: 'text-green-500', bg: 'bg-green-500/10', border: 'border-green-500/50', icon: <ShieldCheck size={48} className="text-green-500" />, msg: 'Environment appears safe.' };
  };

  const risk = getRiskDisplay();

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard Overview</h1>
          <p className="text-slate-400">Real-time status of the virtual simulation.</p>
        </div>
        <div className="px-4 py-2 bg-slate-800 rounded-full text-sm font-medium border border-slate-700 flex items-center gap-2">
          <Activity size={16} className="text-primary" /> System Status: ONLINE
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Sensor Cards */}
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 bg-orange-500/20 text-orange-500 rounded-xl"><Thermometer size={28} /></div>
          <div>
            <p className="text-sm text-slate-400 font-medium">Temperature</p>
            <p className="text-2xl font-bold text-slate-100">{temperature.toFixed(1)} <span className="text-sm text-slate-500">°C</span></p>
          </div>
        </div>
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 bg-slate-500/20 text-slate-400 rounded-xl"><Wind size={28} /></div>
          <div>
            <p className="text-sm text-slate-400 font-medium">Smoke Level</p>
            <p className="text-2xl font-bold text-slate-100">{Math.round(smoke)} <span className="text-sm text-slate-500">ppm</span></p>
          </div>
        </div>
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 bg-blue-500/20 text-blue-400 rounded-xl"><Brain size={28} /></div>
          <div>
            <p className="text-sm text-slate-400 font-medium">AI Confidence</p>
            <p className="text-2xl font-bold text-slate-100">{confidence}%</p>
          </div>
        </div>
        <div className="glass-card p-5 flex items-center gap-4">
          <div className={`p-3 rounded-xl ${riskLevel === 2 ? 'bg-red-500/20 text-red-500 animate-pulse' : 'bg-slate-800 text-slate-500'}`}>
            {riskLevel === 2 ? <Volume2 size={28} /> : <VolumeX size={28} />}
          </div>
          <div>
            <p className="text-sm text-slate-400 font-medium">Virtual Buzzer</p>
            <p className="text-2xl font-bold text-slate-100">{riskLevel === 2 ? 'ON' : 'OFF'}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Status */}
        <div className={`glass-card p-8 flex flex-col items-center justify-center text-center transition-colors duration-500 border-2 ${risk.border} ${risk.bg}`}>
          {risk.icon}
          <h2 className={`text-4xl font-black mt-4 tracking-wider ${risk.color}`}>{risk.text}</h2>
          <p className="text-slate-300 mt-2 text-lg">{risk.msg}</p>
        </div>

        {/* Live Mini Chart */}
        <div className="glass-card p-5 lg:col-span-2">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Live Sensor Trends</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metricsHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickFormatter={(tick) => ''} />
                <YAxis yAxisId="left" stroke="#f97316" fontSize={12} domain={[0, 100]} />
                <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" fontSize={12} domain={[0, 1000]} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
                <Line yAxisId="left" type="monotone" dataKey="temperature" stroke="#f97316" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line yAxisId="right" type="monotone" dataKey="smoke" stroke="#94a3b8" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <Controls />
    </div>
  );
};
export default Dashboard;
"""

files["src/pages/VirtualCircuit.jsx"] = """
import { useContext, useState } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import Controls from '../components/Controls';
import { Cpu, Wind, Thermometer, Info } from 'lucide-react';

const VirtualCircuit = () => {
  const { temperature, smoke, riskLevel } = useContext(SimulationContext);
  const [activeComponent, setActiveComponent] = useState(null);

  const infoMap = {
    esp: { name: "ESP8266 NodeMCU", desc: "Microcontroller + Wi-Fi. Processes sensor data and sends to cloud.", pins: "A0, D2, D4, D5, D6, D7" },
    mq2: { name: "MQ-2 Sensor", desc: "Smoke and combustible gas detection.", pins: "VCC, GND, A0 (Analog Out)" },
    dht11: { name: "DHT11 Sensor", desc: "Temperature measurement.", pins: "VCC, DATA (D2), GND" },
    leds: { name: "LED Indicators", desc: "Visual risk-level indication. Green=Normal, Yellow=Warning, Red=High Risk.", pins: "D5, D6, D7" },
    buzzer: { name: "Piezo Buzzer", desc: "Local audible warning during High Fire Risk.", pins: "D4, GND" }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Virtual Circuit Laboratory</h1>
        <p className="text-slate-400">Interactive hardware simulation of the ESP8266-based system.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card p-6 min-h-[500px] relative flex flex-col items-center justify-center bg-[#0a0f1c]">
          {/* Virtual Wiring Canvas (Simulated with SVG) */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-50" style={{ zIndex: 0 }}>
            {/* Wires */}
            <path d="M 250 200 C 350 200, 350 300, 450 300" stroke="#f59e0b" strokeWidth="3" fill="none" /> {/* MQ2 to ESP */}
            <path d="M 250 400 C 350 400, 350 320, 450 320" stroke="#3b82f6" strokeWidth="3" fill="none" /> {/* DHT to ESP */}
            <path d="M 650 280 C 750 280, 750 200, 800 200" stroke="#22c55e" strokeWidth="3" fill="none" /> {/* ESP to LEDs */}
            <path d="M 650 340 C 750 340, 750 400, 800 400" stroke="#ef4444" strokeWidth="3" fill="none" /> {/* ESP to Buzzer */}
          </svg>

          <div className="relative z-10 w-full max-w-4xl grid grid-cols-3 gap-8 items-center">
            
            {/* Input Sensors (Left) */}
            <div className="flex flex-col gap-12 items-center">
              <div 
                className={`relative bg-slate-800 p-4 rounded-lg border-2 cursor-pointer transition ${activeComponent === 'mq2' ? 'border-primary' : 'border-slate-600'} w-40 text-center shadow-lg`}
                onMouseEnter={() => setActiveComponent('mq2')} onMouseLeave={() => setActiveComponent(null)}
              >
                <Wind className="mx-auto mb-2 text-slate-400" size={32} />
                <div className="font-bold text-slate-200">MQ-2</div>
                <div className="text-xs text-slate-400 mt-1">Analog Out: {Math.round(smoke)}</div>
                {/* Smoke visual effect */}
                {smoke > 300 && <div className="absolute -top-4 -right-4 w-12 h-12 bg-slate-400/20 rounded-full blur-xl animate-pulse"></div>}
              </div>

              <div 
                className={`bg-slate-800 p-4 rounded-lg border-2 cursor-pointer transition ${activeComponent === 'dht11' ? 'border-primary' : 'border-slate-600'} w-40 text-center shadow-lg`}
                onMouseEnter={() => setActiveComponent('dht11')} onMouseLeave={() => setActiveComponent(null)}
              >
                <Thermometer className="mx-auto mb-2 text-orange-500" size={32} />
                <div className="font-bold text-slate-200">DHT11</div>
                <div className="text-xs text-slate-400 mt-1">Data: {temperature.toFixed(1)}°C</div>
              </div>
            </div>

            {/* Microcontroller (Center) */}
            <div className="flex flex-col items-center">
              <div 
                className={`bg-slate-900 p-6 rounded-xl border-4 cursor-pointer transition ${activeComponent === 'esp' ? 'border-primary' : 'border-slate-700'} w-56 text-center shadow-2xl relative`}
                onMouseEnter={() => setActiveComponent('esp')} onMouseLeave={() => setActiveComponent(null)}
              >
                <Cpu className="mx-auto mb-3 text-primary" size={48} />
                <div className="font-bold text-white text-lg">ESP8266</div>
                <div className="text-xs text-slate-400 mt-2">NodeMCU v3</div>
                
                {/* Simulated Pins */}
                <div className="absolute top-0 bottom-0 left-[-8px] flex flex-col justify-around py-4">
                  {[...Array(6)].map((_,i) => <div key={i} className="w-2 h-2 bg-yellow-600 rounded-sm"></div>)}
                </div>
                <div className="absolute top-0 bottom-0 right-[-8px] flex flex-col justify-around py-4">
                  {[...Array(6)].map((_,i) => <div key={i} className="w-2 h-2 bg-yellow-600 rounded-sm"></div>)}
                </div>
                
                {/* WiFi TX/RX blink */}
                <div className="absolute top-4 right-4 w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
              </div>
            </div>

            {/* Outputs (Right) */}
            <div className="flex flex-col gap-12 items-center">
              <div 
                className={`bg-slate-800 p-4 rounded-lg border-2 cursor-pointer transition flex gap-4 ${activeComponent === 'leds' ? 'border-primary' : 'border-slate-600'} shadow-lg`}
                onMouseEnter={() => setActiveComponent('leds')} onMouseLeave={() => setActiveComponent(null)}
              >
                <div className={`w-8 h-8 rounded-full ${riskLevel === 0 ? 'bg-green-500 shadow-[0_0_15px_#22c55e]' : 'bg-green-900/50'}`}></div>
                <div className={`w-8 h-8 rounded-full ${riskLevel === 1 ? 'bg-yellow-500 shadow-[0_0_15px_#eab308]' : 'bg-yellow-900/50'}`}></div>
                <div className={`w-8 h-8 rounded-full ${riskLevel === 2 ? 'bg-red-500 shadow-[0_0_15px_#ef4444]' : 'bg-red-900/50'}`}></div>
              </div>

              <div 
                className={`bg-slate-800 p-4 rounded-full border-2 cursor-pointer transition w-24 h-24 flex items-center justify-center ${activeComponent === 'buzzer' ? 'border-primary' : 'border-slate-600'} shadow-lg relative`}
                onMouseEnter={() => setActiveComponent('buzzer')} onMouseLeave={() => setActiveComponent(null)}
              >
                <div className={`w-16 h-16 rounded-full border-4 border-slate-900 flex items-center justify-center ${riskLevel === 2 ? 'bg-slate-700 animate-bounce' : 'bg-slate-700'}`}>
                  {riskLevel === 2 && (
                     <div className="absolute inset-0 rounded-full border border-white/20 animate-ping"></div>
                  )}
                </div>
                <span className="absolute bottom-2 text-[10px] font-bold text-slate-400">BUZZER</span>
              </div>
            </div>

          </div>
        </div>

        <div className="glass-card p-6 flex flex-col">
          <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <Info size={20} className="text-primary"/> Component Inspector
          </h3>
          {activeComponent ? (
            <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700 h-full">
              <h4 className="text-xl font-bold text-white mb-2">{infoMap[activeComponent].name}</h4>
              <p className="text-slate-300 text-sm mb-4">{infoMap[activeComponent].desc}</p>
              <div className="mt-auto">
                <span className="text-xs text-slate-500 uppercase font-semibold">Connections:</span>
                <p className="text-sm font-mono text-slate-400 mt-1 bg-black/30 p-2 rounded">{infoMap[activeComponent].pins}</p>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-center p-4">
              <Cpu size={48} className="mb-4 opacity-50" />
              <p>Hover over a circuit component to view its details and connections.</p>
            </div>
          )}
        </div>
      </div>
      
      <Controls />
    </div>
  );
};
export default VirtualCircuit;
"""

files["src/pages/AIClassifier.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { BrainCircuit, GitMerge, CheckCircle2 } from 'lucide-react';

const AIClassifier = () => {
  const { temperature, smoke, tempRate, smokeRate, riskLevel, confidence } = useContext(SimulationContext);

  const getDecisionPath = () => {
    if (riskLevel === 2) {
      if (temperature > 50 && smoke > 600) return [true, true, null, null]; // Path 1: Both high
      return [true, false, true, null]; // Path 2: One very high
    } else if (riskLevel === 1) {
      return [false, null, null, true]; // Path 3: Warning conditions met
    }
    return [false, null, null, false]; // Path 4: Normal
  };

  const path = getDecisionPath();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">AI Fire-Risk Classification</h1>
        <p className="text-slate-400">Explainable AI: See exactly how the Decision Tree evaluates sensor data.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="glass-card p-6 flex flex-col gap-6">
          <h3 className="text-lg font-semibold border-b border-slate-700 pb-2">Real-time Inputs</h3>
          
          <div className="space-y-4">
            <div className="bg-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Temperature</span>
              <span className="font-bold font-mono text-orange-400">{temperature.toFixed(1)}°C</span>
            </div>
            <div className="bg-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Smoke Level</span>
              <span className="font-bold font-mono text-slate-200">{Math.round(smoke)} ppm</span>
            </div>
            <div className="bg-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Temp Rate (Δ/s)</span>
              <span className="font-bold font-mono text-orange-400">{tempRate > 0 ? '+' : ''}{tempRate.toFixed(2)}</span>
            </div>
            <div className="bg-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Smoke Rate (Δ/s)</span>
              <span className="font-bold font-mono text-slate-200">{smokeRate > 0 ? '+' : ''}{smokeRate.toFixed(1)}</span>
            </div>
          </div>

          <div className="mt-auto pt-6 border-t border-slate-700">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-400">Model Output</span>
              <span className={`font-bold px-3 py-1 rounded text-sm ${riskLevel === 2 ? 'bg-red-500/20 text-red-500' : riskLevel === 1 ? 'bg-yellow-500/20 text-yellow-500' : 'bg-green-500/20 text-green-500'}`}>
                {riskLevel === 2 ? 'HIGH RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL'}
              </span>
            </div>
            <div className="flex justify-between items-center mt-3">
              <span className="text-sm text-slate-400">Confidence Score</span>
              <span className="font-bold text-white">{confidence}%</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 glass-card p-6 overflow-x-auto">
          <h3 className="text-lg font-semibold border-b border-slate-700 pb-2 mb-6">Decision Tree Visualization</h3>
          
          <div className="min-w-[600px] flex flex-col items-center gap-6 font-mono text-sm relative pb-8">
            {/* Root Node */}
            <div className="bg-blue-900/50 border-2 border-blue-500 text-blue-100 p-3 rounded-xl shadow-lg w-64 text-center z-10 relative">
              Temp {'>'} 50 OR Smoke {'>'} 600?
            </div>

            <div className="flex w-full justify-center gap-32 relative">
              {/* Lines from Root */}
              <svg className="absolute w-full h-12 -top-6 pointer-events-none" style={{ zIndex: 0 }}>
                <path d="M 50% 0 L 50% 10 L 25% 10 L 25% 24" stroke={path[0] === true ? "#f97316" : "#475569"} strokeWidth={path[0] === true ? "3" : "2"} fill="none" />
                <path d="M 50% 0 L 50% 10 L 75% 10 L 75% 24" stroke={path[0] === false ? "#22c55e" : "#475569"} strokeWidth={path[0] === false ? "3" : "2"} fill="none" />
              </svg>

              {/* Left Branch (YES) */}
              <div className="flex flex-col items-center gap-6 w-1/2">
                <span className="bg-slate-800 px-2 rounded -mt-3 z-10 text-xs">YES</span>
                <div className={`p-3 rounded-xl shadow-lg w-56 text-center z-10 transition-colors ${path[0] === true ? 'bg-blue-900/50 border-2 border-blue-500 text-blue-100' : 'bg-slate-800 border-2 border-slate-700 text-slate-500'}`}>
                  Temp {'>'} 50 AND Smoke {'>'} 600?
                </div>

                <div className="flex w-full justify-center gap-16 relative">
                  <svg className="absolute w-full h-12 -top-6 pointer-events-none" style={{ zIndex: 0 }}>
                    <path d="M 50% 0 L 50% 10 L 20% 10 L 20% 24" stroke={path[1] === true ? "#ef4444" : "#475569"} strokeWidth={path[1] === true ? "3" : "2"} fill="none" />
                    <path d="M 50% 0 L 50% 10 L 80% 10 L 80% 24" stroke={path[1] === false ? "#f97316" : "#475569"} strokeWidth={path[1] === false ? "3" : "2"} fill="none" />
                  </svg>
                  
                  {/* Both high */}
                  <div className="flex flex-col items-center mt-2">
                    <span className="bg-slate-800 px-2 rounded -mt-5 z-10 text-xs mb-4">YES</span>
                    <div className={`p-2 rounded font-bold w-24 text-center ${path[1] === true ? 'bg-red-500 text-white shadow-[0_0_15px_#ef4444]' : 'bg-slate-800 text-slate-600'}`}>HIGH RISK</div>
                  </div>
                  
                  {/* One high */}
                  <div className="flex flex-col items-center mt-2">
                    <span className="bg-slate-800 px-2 rounded -mt-5 z-10 text-xs mb-4">NO</span>
                    <div className={`p-2 rounded font-bold w-24 text-center ${path[1] === false ? 'bg-red-500 text-white shadow-[0_0_15px_#ef4444]' : 'bg-slate-800 text-slate-600'}`}>HIGH RISK</div>
                  </div>
                </div>
              </div>

              {/* Right Branch (NO) */}
              <div className="flex flex-col items-center gap-6 w-1/2">
                <span className="bg-slate-800 px-2 rounded -mt-3 z-10 text-xs">NO</span>
                <div className={`p-3 rounded-xl shadow-lg w-64 text-center z-10 transition-colors ${path[0] === false ? 'bg-blue-900/50 border-2 border-blue-500 text-blue-100' : 'bg-slate-800 border-2 border-slate-700 text-slate-500'}`}>
                  Temp {'>'} 40 OR Smoke {'>'} 400 OR<br/>Rates High?
                </div>

                <div className="flex w-full justify-center gap-16 relative">
                  <svg className="absolute w-full h-12 -top-6 pointer-events-none" style={{ zIndex: 0 }}>
                    <path d="M 50% 0 L 50% 10 L 20% 10 L 20% 24" stroke={path[3] === true ? "#eab308" : "#475569"} strokeWidth={path[3] === true ? "3" : "2"} fill="none" />
                    <path d="M 50% 0 L 50% 10 L 80% 10 L 80% 24" stroke={path[3] === false ? "#22c55e" : "#475569"} strokeWidth={path[3] === false ? "3" : "2"} fill="none" />
                  </svg>
                  
                  {/* Warning */}
                  <div className="flex flex-col items-center mt-2">
                    <span className="bg-slate-800 px-2 rounded -mt-5 z-10 text-xs mb-4">YES</span>
                    <div className={`p-2 rounded font-bold w-24 text-center ${path[3] === true ? 'bg-yellow-500 text-black shadow-[0_0_15px_#eab308]' : 'bg-slate-800 text-slate-600'}`}>WARNING</div>
                  </div>
                  
                  {/* Normal */}
                  <div className="flex flex-col items-center mt-2">
                    <span className="bg-slate-800 px-2 rounded -mt-5 z-10 text-xs mb-4">NO</span>
                    <div className={`p-2 rounded font-bold w-24 text-center ${path[3] === false ? 'bg-green-500 text-white shadow-[0_0_15px_#22c55e]' : 'bg-slate-800 text-slate-600'}`}>NORMAL</div>
                  </div>
                </div>
              </div>

            </div>
          </div>
          
          <div className="mt-8 bg-slate-800/50 p-4 rounded-lg border border-slate-700">
            <h4 className="font-bold text-primary mb-2 flex items-center gap-2"><BrainCircuit size={18} /> Why did the AI make this prediction?</h4>
            <ul className="list-disc list-inside text-slate-300 space-y-1 text-sm">
              {riskLevel === 0 && (
                <>
                  <li>Temperature is within normal simulated range.</li>
                  <li>Smoke level is low.</li>
                  <li>No rapid environmental changes detected in recent history.</li>
                </>
              )}
              {riskLevel === 1 && (
                <>
                  <li>Conditions differ from normal baseline.</li>
                  <li>Either temperature or smoke is moderately elevated.</li>
                  <li>Or sensor trends indicate rapidly changing conditions.</li>
                </>
              )}
              {riskLevel === 2 && (
                <>
                  <li>Temperature is significantly elevated.</li>
                  <li>Smoke level is dangerously high.</li>
                  <li>The combined factors cross the critical safety threshold.</li>
                </>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
export default AIClassifier;
"""

files["src/pages/ExperimentLab.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Play, Check, ChevronRight, TestTube2 } from 'lucide-react';

const ExperimentLab = () => {
  const { setTargetTemp, setTargetSmoke, riskLevel, addExperimentResult, experiments } = useContext(SimulationContext);

  const predefinedExperiments = [
    {
      id: 1,
      name: "Normal Environment",
      objective: "Observe the system under normal environmental conditions.",
      targetT: 30,
      targetS: 100,
      expectedRisk: 0,
      expectedText: "NORMAL"
    },
    {
      id: 2,
      name: "Smoke Detection",
      objective: "Increase the smoke level and observe the system response.",
      targetT: 32,
      targetS: 450,
      expectedRisk: 1,
      expectedText: "WARNING"
    },
    {
      id: 3,
      name: "Temperature Anomaly",
      objective: "Increase temperature and observe how the classifier responds.",
      targetT: 65,
      targetS: 120,
      expectedRisk: 1,
      expectedText: "WARNING / HIGH RISK"
    },
    {
      id: 4,
      name: "Combined Fire Risk",
      objective: "Increase both temperature and smoke to simulate fire.",
      targetT: 75,
      targetS: 850,
      expectedRisk: 2,
      expectedText: "HIGH FIRE RISK"
    }
  ];

  const runExperiment = (exp) => {
    setTargetTemp(exp.targetT);
    setTargetSmoke(exp.targetS);
  };

  const recordResult = (exp) => {
    addExperimentResult(exp.name, riskLevel === 2 ? 'HIGH RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL');
  };

  const completedCount = new Set(experiments.map(e => e.name)).size;
  const accuracy = completedCount > 0 ? "100%" : "0%";

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white">Experiment Lab</h1>
          <p className="text-slate-400">Run predefined simulation scenarios and record results.</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-slate-400">Experiments Completed</div>
          <div className="text-xl font-bold text-primary">{Math.min(completedCount, 4)} / 4</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {predefinedExperiments.map((exp) => (
          <div key={exp.id} className="glass-card p-6 flex flex-col">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <TestTube2 className="text-primary" size={24} /> 
                Experiment {exp.id}: {exp.name}
              </h3>
            </div>
            
            <p className="text-slate-300 text-sm mb-4">{exp.objective}</p>
            
            <div className="bg-slate-800/50 rounded-lg p-4 mb-6 text-sm">
              <div className="grid grid-cols-2 gap-4 mb-2">
                <div><span className="text-slate-500">Target Temp:</span> <span className="font-mono text-orange-400">{exp.targetT}°C</span></div>
                <div><span className="text-slate-500">Target Smoke:</span> <span className="font-mono text-slate-300">{exp.targetS} ppm</span></div>
              </div>
              <div className="pt-2 border-t border-slate-700">
                <span className="text-slate-500">Expected Result:</span> <span className="font-bold ml-2 text-white">{exp.expectedText}</span>
              </div>
            </div>

            <div className="mt-auto flex gap-3">
              <button 
                onClick={() => runExperiment(exp)}
                className="flex-1 flex items-center justify-center gap-2 py-2 bg-primary hover:bg-orange-500 text-white rounded-lg font-medium transition"
              >
                <Play size={18} /> Start
              </button>
              <button 
                onClick={() => recordResult(exp)}
                className="flex-1 flex items-center justify-center gap-2 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition"
              >
                <Check size={18} /> Record Result
              </button>
            </div>
          </div>
        ))}
      </div>
      
      <div className="glass-card p-6 mt-6 flex justify-between items-center">
        <div>
          <h3 className="text-lg font-bold text-white">Educational Score</h3>
          <p className="text-sm text-slate-400">Based on recorded experiment results.</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-black text-green-500">{accuracy}</div>
          <div className="text-xs text-slate-400 uppercase tracking-widest">Accuracy</div>
        </div>
      </div>
    </div>
  );
};
export default ExperimentLab;
"""

files["src/pages/IoTDashboard.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Wifi, Cloud, Smartphone, Database, AlertCircle, ArrowRight } from 'lucide-react';

const IoTDashboard = () => {
  const { temperature, smoke, riskLevel, alerts } = useContext(SimulationContext);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">IoT & Cloud Monitoring</h1>
        <p className="text-slate-400">Simulated remote dashboard receiving data from the ESP8266.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-4 flex flex-col items-center text-center justify-center border-t-4 border-t-green-500">
          <Wifi size={32} className="text-green-500 mb-2" />
          <h4 className="font-bold text-white">Wi-Fi Status</h4>
          <p className="text-sm text-green-400">CONNECTED</p>
        </div>
        <div className="glass-card p-4 flex flex-col items-center text-center justify-center border-t-4 border-t-blue-500">
          <Cloud size={32} className="text-blue-500 mb-2" />
          <h4 className="font-bold text-white">Cloud Server</h4>
          <p className="text-sm text-blue-400">ONLINE</p>
        </div>
        <div className="glass-card p-4 flex flex-col items-center text-center justify-center border-t-4 border-t-purple-500">
          <Database size={32} className="text-purple-500 mb-2" />
          <h4 className="font-bold text-white">Data Logging</h4>
          <p className="text-sm text-purple-400">ACTIVE</p>
        </div>
        <div className="glass-card p-4 flex flex-col items-center text-center justify-center border-t-4 border-t-primary">
          <Smartphone size={32} className="text-primary mb-2" />
          <h4 className="font-bold text-white">Push Alerts</h4>
          <p className="text-sm text-orange-400">ENABLED</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold text-white mb-6 border-b border-slate-700 pb-2">Remote Telemetry Stream</h3>
          
          <div className="font-mono text-sm bg-black/50 p-4 rounded-lg overflow-hidden relative">
            <div className="absolute top-2 right-2 flex gap-1">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
            </div>
            <div className="text-slate-500 mb-2">{`// Last received payload`}</div>
            <div className="text-green-400">
              {`{`}
              <div className="pl-4">
                <span className="text-blue-300">"device_id"</span>: <span className="text-orange-300">"esp8266_lab_01"</span>,<br/>
                <span className="text-blue-300">"timestamp"</span>: <span className="text-orange-300">"{new Date().toISOString()}"</span>,<br/>
                <span className="text-blue-300">"sensors"</span>: {`{`}<br/>
                <div className="pl-4">
                  <span className="text-blue-300">"temp_c"</span>: <span className="text-purple-300">{temperature.toFixed(2)}</span>,<br/>
                  <span className="text-blue-300">"smoke_ppm"</span>: <span className="text-purple-300">{smoke.toFixed(1)}</span><br/>
                </div>
                {`}`},<br/>
                <span className="text-blue-300">"ai_classification"</span>: <span className="text-purple-300">{riskLevel}</span>,<br/>
                <span className="text-blue-300">"actuators"</span>: {`{`}<br/>
                <div className="pl-4">
                  <span className="text-blue-300">"buzzer"</span>: <span className="text-orange-300">{riskLevel === 2 ? "true" : "false"}</span><br/>
                </div>
                {`}`}
              </div>
              {`}`}
            </div>
          </div>
        </div>

        <div className="glass-card p-6 flex flex-col">
          <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-700 pb-2 flex items-center gap-2">
            <AlertCircle className="text-red-500" /> Remote Alert System
          </h3>
          
          <div className="flex-1 overflow-y-auto max-h-80 pr-2 space-y-3">
            {alerts.length === 0 ? (
              <div className="h-full flex items-center justify-center text-slate-500">
                No alerts generated yet. Trigger a HIGH RISK state.
              </div>
            ) : (
              alerts.map((alert) => (
                <div key={alert.id} className="bg-red-900/20 border border-red-500/30 p-4 rounded-lg flex flex-col gap-2">
                  <div className="flex justify-between items-start">
                    <span className="font-bold text-red-500 text-sm flex items-center gap-1">🚨 SIMULATED FIRE ALERT</span>
                    <span className="text-xs text-slate-400">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-slate-200 text-sm">{alert.message}</p>
                  <div className="text-xs text-slate-400 flex gap-4 mt-1">
                    <span>Temp: {alert.temp}°C</span>
                    <span>Smoke: {alert.smoke} ppm</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
export default IoTDashboard;
"""

files["src/pages/Analytics.jsx"] = """
import { useContext, useMemo } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const Analytics = () => {
  const { metricsHistory, experiments } = useContext(SimulationContext);

  const stats = useMemo(() => {
    if (metricsHistory.length === 0) return { avgTemp: 0, maxTemp: 0, avgSmoke: 0, maxSmoke: 0 };
    let totalT = 0, maxT = 0, totalS = 0, maxS = 0;
    metricsHistory.forEach(m => {
      totalT += m.temperature;
      totalS += m.smoke;
      if (m.temperature > maxT) maxT = m.temperature;
      if (m.smoke > maxS) maxS = m.smoke;
    });
    return {
      avgTemp: (totalT / metricsHistory.length).toFixed(1),
      maxTemp: maxT.toFixed(1),
      avgSmoke: Math.round(totalS / metricsHistory.length),
      maxSmoke: Math.round(maxS)
    };
  }, [metricsHistory]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Sensor Analytics</h1>
        <p className="text-slate-400">Historical data analysis and trends.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card p-4">
          <p className="text-sm text-slate-400">Avg Temperature</p>
          <p className="text-2xl font-bold text-orange-400">{stats.avgTemp}°C</p>
        </div>
        <div className="glass-card p-4">
          <p className="text-sm text-slate-400">Max Temperature</p>
          <p className="text-2xl font-bold text-red-500">{stats.maxTemp}°C</p>
        </div>
        <div className="glass-card p-4">
          <p className="text-sm text-slate-400">Avg Smoke</p>
          <p className="text-2xl font-bold text-slate-300">{stats.avgSmoke} ppm</p>
        </div>
        <div className="glass-card p-4">
          <p className="text-sm text-slate-400">Max Smoke</p>
          <p className="text-2xl font-bold text-slate-100">{stats.maxSmoke} ppm</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-5 h-80">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Temperature Trend</h3>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={metricsHistory}>
              <defs>
                <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickFormatter={() => ''} />
              <YAxis stroke="#94a3b8" fontSize={12} domain={[10, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
              <Area type="monotone" dataKey="temperature" stroke="#f97316" fillOpacity={1} fill="url(#colorTemp)" isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-card p-5 h-80">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Smoke Level Trend</h3>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={metricsHistory}>
              <defs>
                <linearGradient id="colorSmoke" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#94a3b8" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickFormatter={() => ''} />
              <YAxis stroke="#94a3b8" fontSize={12} domain={[0, 1000]} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
              <Area type="monotone" dataKey="smoke" stroke="#94a3b8" fillOpacity={1} fill="url(#colorSmoke)" isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
export default Analytics;
"""

files["src/pages/History.jsx"] = """
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Trash2, History as HistIcon } from 'lucide-react';

const History = () => {
  const { experiments, clearHistory } = useContext(SimulationContext);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white">Experiment History</h1>
          <p className="text-slate-400">Log of locally stored experiment runs.</p>
        </div>
        <button 
          onClick={clearHistory}
          className="flex items-center gap-2 px-4 py-2 bg-red-900/30 hover:bg-red-800/50 text-red-300 rounded-lg border border-red-700/50 transition"
        >
          <Trash2 size={16} /> Clear History
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        {experiments.length === 0 ? (
          <div className="p-12 flex flex-col items-center justify-center text-slate-500">
            <HistIcon size={48} className="mb-4 opacity-50" />
            <p>No experiment history found. Run some experiments in the Lab.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-800/50 border-b border-slate-700 text-sm text-slate-400">
                  <th className="p-4 font-semibold">Date / Time</th>
                  <th className="p-4 font-semibold">Experiment Name</th>
                  <th className="p-4 font-semibold">Max Temp</th>
                  <th className="p-4 font-semibold">Max Smoke</th>
                  <th className="p-4 font-semibold">AI Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {experiments.map((exp) => (
                  <tr key={exp.id} className="hover:bg-slate-800/30 transition text-sm">
                    <td className="p-4 text-slate-300">{exp.date}</td>
                    <td className="p-4 font-medium text-white">{exp.name}</td>
                    <td className="p-4 font-mono text-orange-400">{exp.maxTemp}°C</td>
                    <td className="p-4 font-mono text-slate-300">{exp.maxSmoke} ppm</td>
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${exp.result === 'HIGH RISK' ? 'bg-red-500/20 text-red-500' : exp.result === 'WARNING' ? 'bg-yellow-500/20 text-yellow-500' : 'bg-green-500/20 text-green-500'}`}>
                        {exp.result}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
export default History;
"""

files["src/pages/About.jsx"] = """
import React from 'react';
import { FileText, Cpu, Server, ShieldAlert } from 'lucide-react';

const About = () => {
  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">About FireGuard AI</h1>
        <p className="text-slate-400 text-lg">Virtual Fire & Smoke Early Warning Laboratory</p>
      </div>

      <div className="glass-card p-8 space-y-6 text-slate-300 leading-relaxed">
        
        <section>
          <h2 className="text-xl font-bold text-white mb-3 flex items-center gap-2"><ShieldAlert className="text-primary"/> The Problem & Solution</h2>
          <p className="mb-3">
            Small fires can escalate quickly into dangerous situations when abnormal smoke or temperature goes undetected early on. Traditional smoke detectors often trigger late or lack intelligent analysis to distinguish between minor issues and severe threats.
          </p>
          <p>
            <strong>Solution:</strong> This virtual laboratory simulates an ESP8266-based IoT early warning system. By combining physical sensor inputs (MQ-2, DHT11) with an AI Decision Tree classifier, the system continuously analyzes environmental conditions and rates of change to predict fire risks instantly.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white mb-3 flex items-center gap-2"><Cpu className="text-primary"/> Simulated Hardware Components</h2>
          <ul className="list-disc list-inside space-y-2 ml-2">
            <li><strong>ESP8266 NodeMCU:</strong> The core microcontroller providing processing and Wi-Fi connectivity.</li>
            <li><strong>MQ-2 Gas Sensor:</strong> Detects smoke and combustible gases via analog input.</li>
            <li><strong>DHT11 Sensor:</strong> Measures ambient temperature via digital input.</li>
            <li><strong>LED Indicators:</strong> Visual state representation (Green = Normal, Yellow = Warning, Red = High Risk).</li>
            <li><strong>Piezo Buzzer:</strong> Provides local audible alerts during emergencies.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white mb-3 flex items-center gap-2"><Server className="text-primary"/> Virtual vs. Real Hardware</h2>
          <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
            <p className="mb-2"><strong className="text-primary">VIRTUAL MODE (Current):</strong> The browser generates simulated sensor values. The Decision Tree runs in JavaScript, and the dashboard updates purely through software state.</p>
            <p><strong className="text-blue-400">REAL HARDWARE MODE:</strong> The exact same architecture can be applied to physical hardware. The real MQ-2 and DHT11 feed data to a physical ESP8266, which transmits JSON payloads over Wi-Fi to a backend server to drive this dashboard.</p>
          </div>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white mb-3 flex items-center gap-2"><FileText className="text-primary"/> System Architecture</h2>
          <div className="bg-slate-900 p-6 rounded-lg font-mono text-sm text-center">
            <div className="text-slate-400">Environment</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-white font-bold border border-slate-700 inline-block px-4 py-2 rounded">MQ-2 + DHT11 Sensors</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-blue-400 font-bold border border-blue-900 bg-blue-900/20 inline-block px-4 py-2 rounded">ESP8266 Microcontroller</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-purple-400 font-bold border border-purple-900 bg-purple-900/20 inline-block px-4 py-2 rounded">AI Risk Classification (Decision Tree)</div>
            <div className="text-primary my-1">↓</div>
            <div className="grid grid-cols-2 gap-4 mt-2 max-w-md mx-auto">
              <div className="text-red-400 border border-red-900 bg-red-900/20 p-2 rounded">Local: LED + Buzzer</div>
              <div className="text-green-400 border border-green-900 bg-green-900/20 p-2 rounded">Cloud: IoT Dashboard & Alerts</div>
            </div>
          </div>
        </section>
        
        <div className="text-xs text-slate-500 text-center mt-8 pt-4 border-t border-slate-800">
          This is an educational simulation created for demonstration purposes. 
          Thresholds and logic are designed to illustrate the concept of AI-based early warning systems and should not be used for actual life-safety applications without professional calibration.
        </div>
      </div>
    </div>
  );
};
export default About;
"""

import subprocess
import sys

for path, content in files.items():
    write_file(path, content)

print("Files generated successfully.")
