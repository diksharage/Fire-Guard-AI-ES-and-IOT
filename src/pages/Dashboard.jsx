import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { SettingsContext } from '../context/SettingsContext';
import { Thermometer, Wind, Droplets, Brain, Activity, Volume2, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { temperature, smoke, humidity, riskLevel, aiConfidence, buzzerStatus, isRunning, circuitReady, notifications } = useContext(SimulationContext);
  const { settings } = useContext(SettingsContext);
  const prefs = settings?.dashboardPrefs || {};

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

      {notifications && notifications.length > 0 && (
        <div className="glass-card p-4 mb-6 border border-red-900/30">
          {notifications.slice(0, 2).map(alert => (
            <div key={alert.id} className={`flex justify-between items-center p-3 rounded bg-slate-900 border-l-4 mb-2 last:mb-0 ${alert.type === 'danger' ? 'border-red-500' : 'border-yellow-500'}`}>
              <div className="flex flex-col">
                <span className={`${alert.type === 'danger' ? 'text-red-400' : 'text-yellow-400'} font-semibold`}>{alert.title}</span>
                <span className="text-slate-300 text-sm">{alert.message}</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-slate-500 text-xs">{new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
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
