import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { SettingsContext } from '../context/SettingsContext';
import { Thermometer, Wind, Droplets, BrainCircuit, Activity, Volume2, ShieldAlert } from 'lucide-react';

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
    <div className="space-y-6 pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">FireGuard AI Dashboard</h1>
          <p className="text-slate-400">Virtual Fire & Smoke Early Warning Laboratory</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 text-sm">
            Mode: <strong className="text-blue-400 uppercase">{settings?.experimentMode || 'EASY'}</strong>
          </div>
          <div className="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 text-sm">
            Simulation: <strong className={isRunning ? 'text-green-500' : 'text-slate-500'}>{isRunning ? 'RUNNING' : 'PAUSED'}</strong>
          </div>
        </div>
      </div>

      {/* Main Status Card */}
      <div className={`glass-card p-8 flex flex-col items-center justify-center text-center transition-colors ${risk.bg} ${risk.border} border-2`}>
        <h2 className="text-lg font-semibold text-slate-400 mb-2 uppercase tracking-widest">Current Risk Level</h2>
        <div className={`text-5xl font-black mb-4 ${risk.color}`}>{risk.text}</div>
        <p className="text-slate-300 text-lg">
          {riskLevel === 2 ? 'Immediate attention required' : riskLevel === 1 ? 'Abnormal environmental conditions detected' : 'Environment appears safe'}
        </p>
      </div>

      {/* Sensor Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {prefs.showTemperature !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Thermometer /> <span className="font-semibold">Temperature</span></div>
          <div className="text-4xl font-bold text-slate-50">{temperature.toFixed(1)}<span className="text-xl text-slate-500 ml-1">°C</span></div>
        </div>
        )}
        
        {prefs.showSmoke !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Wind /> <span className="font-semibold">Smoke Level</span></div>
          <div className="text-4xl font-bold text-slate-50">{smoke.toFixed(0)}<span className="text-xl text-slate-500 ml-1">%</span></div>
        </div>
        )}
        
        {prefs.showHumidity !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Droplets /> <span className="font-semibold">Humidity</span></div>
          <div className="text-4xl font-bold text-slate-50">{humidity.toFixed(0)}<span className="text-xl text-slate-500 ml-1">%</span></div>
        </div>
        )}
        
        {prefs.showAiConfidence !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><BrainCircuit /> <span className="font-semibold">AI Confidence</span></div>
          <div className="text-4xl font-bold text-slate-50">{aiConfidence}%</div>
        </div>
        )}
        
        {prefs.showBuzzer !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Volume2 /> <span className="font-semibold">Buzzer Status</span></div>
          <div className={`text-3xl font-bold ${buzzerStatus ? 'text-red-500' : 'text-slate-500'}`}>
            {buzzerStatus ? 'ALARMING' : 'SILENT'}
          </div>
        </div>
        )}
        
        {prefs.showIoT !== false && (
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 text-slate-400 mb-3"><Activity /> <span className="font-semibold">IoT Connection</span></div>
          <div className="text-3xl font-bold text-green-500">CONNECTED</div>
        </div>
        )}
      </div>

      {/* Recent Activity Section */}
      <div className="glass-card p-6 mt-6">
        <div className="flex items-center gap-2 mb-4 text-slate-300">
          <ShieldAlert size={20} />
          <h2 className="text-lg font-bold">Recent Experiment Activity</h2>
        </div>
        <div className="space-y-3">
          {(!notifications || notifications.length === 0) ? (
            <div className="text-slate-500 text-sm p-4 text-center border border-slate-800 rounded bg-slate-900/50">
              No recent activity recorded.
            </div>
          ) : (
            notifications.slice(0, 5).map(note => (
              <div key={note.id} className={`flex justify-between items-center p-3 rounded bg-slate-900/50 border-l-4 ${note.type === 'danger' ? 'border-red-500' : note.type === 'warning' ? 'border-yellow-500' : 'border-blue-500'}`}>
                <div className="flex flex-col">
                  <span className={`${note.type === 'danger' ? 'text-red-400' : note.type === 'warning' ? 'text-yellow-400' : 'text-blue-400'} font-semibold text-sm`}>
                    {note.title}
                  </span>
                  <span className="text-slate-300 text-sm">{note.message}</span>
                </div>
                <span className="text-slate-500 text-xs whitespace-nowrap ml-4">
                  {new Date(note.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
