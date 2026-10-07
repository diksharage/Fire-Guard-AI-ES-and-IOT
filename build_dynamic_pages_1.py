import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

# ---------------------------------------------------------
# 1. SimulationContext.jsx
# ---------------------------------------------------------
ctx_content = """import React, { createContext, useState, useEffect } from 'react';

export const SimulationContext = createContext();

export const SimulationProvider = ({ children }) => {
  // Environmental States
  const [temperature, setTemperature] = useState(25);
  const [smoke, setSmoke] = useState(15);
  const [humidity, setHumidity] = useState(45);
  
  // AI States
  const [riskLevel, setRiskLevel] = useState(0); // 0=NORMAL, 1=WARNING, 2=HIGH RISK
  const [aiConfidence, setAiConfidence] = useState(95);
  const [alerts, setAlerts] = useState([]);
  
  // History
  const [sensorHistory, setSensorHistory] = useState(() => {
    const saved = localStorage.getItem('fireguard_history');
    return saved ? JSON.parse(saved) : [];
  });
  
  // Circuit States
  const [circuitWires, setCircuitWires] = useState([]);
  const [circuitValidation, setCircuitValidation] = useState({ status: 'idle', missing: [], valid: false, correct: 0, total: 17 });
  const [circuitReady, setCircuitReady] = useState(false);
  
  // App States
  const [isRunning, setIsRunning] = useState(false);
  
  // Derived Hardware States
  const buzzerStatus = isRunning && circuitReady && riskLevel === 2;
  const greenLedStatus = isRunning && circuitReady && riskLevel === 0;
  const yellowLedStatus = isRunning && circuitReady && riskLevel === 1;
  const redLedStatus = isRunning && circuitReady && riskLevel === 2;

  // AI Classification Logic
  useEffect(() => {
    let newRisk = 0;
    let confidence = 85 + Math.random() * 10;
    
    // Demonstration parameters
    if (smoke >= 65 && temperature >= 45) {
      newRisk = 2; // HIGH RISK
      confidence = 92 + Math.random() * 6;
    } else if (smoke >= 40 || temperature >= 35) {
      newRisk = 1; // WARNING
      confidence = 88 + Math.random() * 8;
    } else {
      newRisk = 0; // NORMAL
      confidence = 95 + Math.random() * 4;
    }
    
    // Add Alert if risk increases
    if (newRisk > riskLevel) {
      const timestamp = new Date().toLocaleTimeString();
      let msg = newRisk === 2 ? 'High fire-risk condition detected in simulation.' : 'Smoke/Temp increased. Risk status changed to WARNING.';
      setAlerts(prev => [{ id: Date.now(), time: timestamp, message: msg, type: newRisk }, ...prev].slice(0, 10));
    }
    
    setRiskLevel(newRisk);
    setAiConfidence(Math.round(confidence));
  }, [temperature, smoke, humidity]);

  // History Logging
  useEffect(() => {
    localStorage.setItem('fireguard_history', JSON.stringify(sensorHistory));
  }, [sensorHistory]);

  useEffect(() => {
    let interval;
    if (isRunning && circuitReady) {
      interval = setInterval(() => {
        setSensorHistory(prev => {
          const newEntry = {
            time: new Date().toLocaleTimeString([], { hour12: false }),
            temperature,
            smoke,
            humidity,
            riskLevel,
            aiConfidence
          };
          return [...prev, newEntry].slice(-50); // Keep last 50 points
        });
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isRunning, circuitReady, temperature, smoke, humidity, riskLevel, aiConfidence]);

  const clearHistory = () => {
    setSensorHistory([]);
    setAlerts([]);
    localStorage.removeItem('fireguard_history');
  };

  const dismissAlert = (id) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  return (
    <SimulationContext.Provider value={{
      temperature, setTemperature,
      smoke, setSmoke,
      humidity, setHumidity,
      riskLevel,
      aiConfidence,
      alerts, dismissAlert,
      sensorHistory, clearHistory,
      circuitWires, setCircuitWires,
      circuitValidation, setCircuitValidation,
      circuitReady, setCircuitReady,
      isRunning, setIsRunning,
      buzzerStatus, greenLedStatus, yellowLedStatus, redLedStatus
    }}>
      {children}
    </SimulationContext.Provider>
  );
};
"""
with open(os.path.join(DIR, "context", "SimulationContext.jsx"), "w", encoding="utf-8") as f:
    f.write(ctx_content)


# ---------------------------------------------------------
# 2. Dashboard.jsx
# ---------------------------------------------------------
dashboard_content = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Thermometer, Wind, Droplets, Brain, Activity, Volume2, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { temperature, smoke, humidity, riskLevel, aiConfidence, buzzerStatus, isRunning, circuitReady, alerts, dismissAlert } = useContext(SimulationContext);

  const getRiskDisplay = () => {
    if (riskLevel === 2) return { text: 'HIGH FIRE RISK', color: 'text-red-500', bg: 'bg-red-900/20', border: 'border-red-500/50' };
    if (riskLevel === 1) return { text: 'WARNING', color: 'text-amber-500', bg: 'bg-amber-900/20', border: 'border-amber-500/50' };
    return { text: 'NORMAL', color: 'text-green-500', bg: 'bg-green-900/20', border: 'border-green-500/50' };
  };

  const risk = getRiskDisplay();

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">FireGuard AI Dashboard</h1>
          <p className="text-slate-400">Virtual Fire & Smoke Early Warning Laboratory</p>
        </div>
        <div className="flex gap-3">
          <div className="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 text-sm">
            System Status: <strong className="text-primary">ONLINE</strong>
          </div>
          <div className="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 text-sm">
            Simulation: <strong className={isRunning ? 'text-green-500' : 'text-slate-500'}>{isRunning ? 'RUNNING' : 'PAUSED'}</strong>
          </div>
        </div>
      </div>

      {alerts.length > 0 && (
        <div className="space-y-3">
          {alerts.slice(0, 2).map(alert => (
            <div key={alert.id} className={`p-4 rounded-xl border flex justify-between items-center ${alert.type === 2 ? 'bg-red-900/30 border-red-700' : 'bg-amber-900/30 border-amber-700'}`}>
              <div>
                <div className={`font-bold flex items-center gap-2 ${alert.type === 2 ? 'text-red-400' : 'text-amber-400'}`}>
                  {alert.type === 2 ? '🚨 FireGuard Alert' : '⚠ FireGuard Alert'} 
                  <span className="text-xs font-normal text-slate-300">[{alert.time}]</span>
                </div>
                <div className="text-sm text-slate-200 mt-1">{alert.message}</div>
              </div>
              <button onClick={() => dismissAlert(alert.id)} className="text-slate-400 hover:text-slate-50 text-sm bg-slate-800/50 px-3 py-1 rounded">Dismiss</button>
            </div>
          ))}
        </div>
      )}

      {/* Main Status Card */}
      <div className={`glass-card p-8 flex flex-col items-center justify-center text-center transition-colors ${risk.bg} ${risk.border} border-2`}>
        <h2 className="text-lg font-semibold text-slate-400 mb-2 uppercase tracking-widest">Current Risk Level</h2>
        <div className={`text-5xl font-black mb-4 ${risk.color}`}>{risk.text}</div>
        <p className="text-slate-300 text-lg">
          {riskLevel === 2 ? 'Immediate attention required' : riskLevel === 1 ? 'Abnormal environmental conditions detected' : 'Environment appears safe'}
        </p>
      </div>

      {/* Sensor Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Thermometer /> <span className="font-semibold">Temperature</span></div>
          <div className="text-4xl font-bold text-slate-50">{temperature.toFixed(1)}<span className="text-xl text-slate-500 ml-1">°C</span></div>
        </div>
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Wind /> <span className="font-semibold">Smoke Level</span></div>
          <div className="text-4xl font-bold text-slate-50">{smoke.toFixed(0)}<span className="text-xl text-slate-500 ml-1">%</span></div>
        </div>
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Droplets /> <span className="font-semibold">Humidity</span></div>
          <div className="text-4xl font-bold text-slate-50">{humidity.toFixed(0)}<span className="text-xl text-slate-500 ml-1">%</span></div>
        </div>
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Brain /> <span className="font-semibold">AI Confidence</span></div>
          <div className="text-4xl font-bold text-primary">{aiConfidence}<span className="text-xl text-slate-500 ml-1">%</span></div>
        </div>
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Volume2 /> <span className="font-semibold">Buzzer</span></div>
          <div className={`text-3xl font-bold ${buzzerStatus ? 'text-red-500 animate-pulse' : 'text-slate-500'}`}>{buzzerStatus ? 'ON (ALARM)' : 'OFF'}</div>
        </div>
        <div className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Activity /> <span className="font-semibold">IoT Connection</span></div>
          <div className={`text-2xl font-bold ${isRunning ? 'text-green-500' : 'text-amber-500'}`}>{isRunning ? 'CONNECTED' : 'STANDBY'}</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/lab" className="glass-card p-6 flex justify-between items-center hover:bg-slate-800 transition-colors group">
          <div>
            <h3 className="text-lg font-bold text-slate-50 mb-1">Experiment Lab</h3>
            <p className="text-sm text-slate-400">Control temperature & smoke simulation parameters</p>
          </div>
          <ArrowRight className="text-slate-500 group-hover:text-primary transition-colors" />
        </Link>
        <Link to="/analytics" className="glass-card p-6 flex justify-between items-center hover:bg-slate-800 transition-colors group">
          <div>
            <h3 className="text-lg font-bold text-slate-50 mb-1">Sensor Analytics</h3>
            <p className="text-sm text-slate-400">View real-time sensor graphs</p>
          </div>
          <ArrowRight className="text-slate-500 group-hover:text-primary transition-colors" />
        </Link>
      </div>

    </div>
  );
};
export default Dashboard;
"""
with open(os.path.join(DIR, "pages", "Dashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(dashboard_content)

print("Context and Dashboard updated.")
