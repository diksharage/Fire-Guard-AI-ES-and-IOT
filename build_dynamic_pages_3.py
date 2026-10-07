import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

# ---------------------------------------------------------
# 5. IoTDashboard.jsx
# ---------------------------------------------------------
iot_content = """import React, { useContext, useState, useEffect } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Wifi, Server, Activity, Database, Clock } from 'lucide-react';

const IoTDashboard = () => {
  const { temperature, smoke, humidity, riskLevel, aiConfidence, isRunning } = useContext(SimulationContext);
  const [lastUpdate, setLastUpdate] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    if(isRunning) {
      const interval = setInterval(() => {
        setLastUpdate(new Date().toLocaleTimeString());
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [isRunning]);

  const payload = {
    device_id: "FG-ESP8266-01",
    timestamp: new Date().toISOString(),
    sensors: { temperature: parseFloat(temperature.toFixed(1)), smoke: parseFloat(smoke.toFixed(1)), humidity: parseFloat(humidity.toFixed(1)) },
    ai_status: { risk_level: riskLevel, confidence: aiConfidence }
  };

  return (
    <div className="space-y-6 pb-20">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">IoT Cloud Monitoring</h1>
          <p className="text-slate-400">Simulated remote telemetry and cloud connectivity dashboard.</p>
        </div>
        <div className={`px-4 py-2 rounded-full border text-sm font-bold flex items-center gap-2 ${isRunning ? 'bg-green-900/30 text-green-500 border-green-500/50' : 'bg-slate-800 text-slate-500 border-slate-700'}`}>
          <Wifi size={16} /> {isRunning ? 'SIMULATED ONLINE' : 'OFFLINE'}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2"><Server size={16} /> Device Status</h3>
          <div className="space-y-4">
            <div className="flex justify-between border-b border-slate-700 pb-3">
              <span className="text-slate-400">Device Model</span>
              <span className="text-slate-50 font-bold">FireGuard ESP8266 NodeMCU</span>
            </div>
            <div className="flex justify-between border-b border-slate-700 pb-3">
              <span className="text-slate-400">Connection Status</span>
              <span className={`font-bold ${isRunning ? 'text-green-400' : 'text-slate-500'}`}>{isRunning ? 'Connected' : 'Disconnected'}</span>
            </div>
            <div className="flex justify-between border-b border-slate-700 pb-3">
              <span className="text-slate-400">Update Frequency</span>
              <span className="text-slate-50 font-bold">2000 ms</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Last Sync</span>
              <span className="text-primary font-mono font-bold flex items-center gap-1"><Clock size={14}/> {isRunning ? lastUpdate : 'N/A'}</span>
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2"><Database size={16} /> Live JSON Payload</h3>
          <div className="bg-[#0f141f] rounded-lg border border-slate-700 p-4 overflow-x-auto">
            <pre className="text-sm text-green-400 font-mono">
              {isRunning ? JSON.stringify(payload, null, 2) : '// Start simulation to see telemetry data...'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
export default IoTDashboard;
"""
with open(os.path.join(DIR, "pages", "IoTDashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(iot_content)

# ---------------------------------------------------------
# 6. Analytics.jsx
# ---------------------------------------------------------
analytics_content = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Play, Pause, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Analytics = () => {
  const { sensorHistory, isRunning, setIsRunning, clearHistory, circuitReady } = useContext(SimulationContext);
  const navigate = useNavigate();

  return (
    <div className="space-y-6 pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">Sensor Analytics</h1>
          <p className="text-slate-400">Real-time charting of environmental parameters.</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => { if(circuitReady) setIsRunning(!isRunning); else navigate('/circuit'); }} 
            className={`px-4 py-2 rounded font-bold flex items-center gap-2 ${isRunning ? 'bg-amber-900/50 text-amber-500' : 'bg-green-600 text-white'}`}
          >
            {isRunning ? <><Pause size={16}/> Pause Chart</> : <><Play size={16}/> Start Chart</>}
          </button>
          <button onClick={clearHistory} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-red-400 rounded flex items-center gap-2">
            <Trash2 size={16}/> Clear Data
          </button>
        </div>
      </div>

      <div className="glass-card p-6 h-[500px]">
        {sensorHistory.length === 0 ? (
          <div className="w-full h-full flex flex-col items-center justify-center text-slate-500">
            <Activity size={48} className="mb-4 opacity-50" />
            <p>No data recorded yet.</p>
            <p className="text-sm">Start the simulation to plot sensor values.</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sensorHistory} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3342" />
              <XAxis dataKey="time" stroke="#9ca3af" tick={{fontSize: 12}} />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{backgroundColor: '#1C222D', borderColor: '#2a3342', color: '#f5f5f5'}} />
              <Legend />
              <Line type="monotone" dataKey="temperature" stroke="#ef4444" name="Temp (°C)" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line type="monotone" dataKey="smoke" stroke="#94a3b8" name="Smoke (%)" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line type="monotone" dataKey="humidity" stroke="#3b82f6" name="Humidity (%)" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
export default Analytics;
"""
with open(os.path.join(DIR, "pages", "Analytics.jsx"), "w", encoding="utf-8") as f:
    f.write(analytics_content)


# ---------------------------------------------------------
# 7. History.jsx
# ---------------------------------------------------------
history_content = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { History as HistoryIcon, Trash2 } from 'lucide-react';

const History = () => {
  const { sensorHistory, clearHistory } = useContext(SimulationContext);

  return (
    <div className="space-y-6 pb-20">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">Simulation History</h1>
          <p className="text-slate-400">Log of recorded environmental states and AI decisions.</p>
        </div>
        <button onClick={clearHistory} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-red-400 rounded-lg flex items-center gap-2 transition-colors">
          <Trash2 size={16}/> Clear History
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        {sensorHistory.length === 0 ? (
          <div className="p-12 text-center text-slate-500 flex flex-col items-center">
            <HistoryIcon size={48} className="mb-4 opacity-30" />
            <p>No history available.</p>
            <p className="text-sm mt-2">Run the simulation to generate logs.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-800/50 text-slate-400">
                <tr>
                  <th className="p-4">Timestamp</th>
                  <th className="p-4">Temp (°C)</th>
                  <th className="p-4">Smoke (%)</th>
                  <th className="p-4">Humidity (%)</th>
                  <th className="p-4">Confidence</th>
                  <th className="p-4">Classification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50 text-slate-300">
                {[...sensorHistory].reverse().map((entry, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-4 font-mono text-slate-400">{entry.time}</td>
                    <td className="p-4">{entry.temperature.toFixed(1)}</td>
                    <td className="p-4">{entry.smoke.toFixed(0)}</td>
                    <td className="p-4">{entry.humidity.toFixed(0)}</td>
                    <td className="p-4 text-primary font-bold">{entry.aiConfidence}%</td>
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${entry.riskLevel === 2 ? 'bg-red-900/40 text-red-400' : entry.riskLevel === 1 ? 'bg-amber-900/40 text-amber-400' : 'bg-green-900/40 text-green-400'}`}>
                        {entry.riskLevel === 2 ? 'HIGH RISK' : entry.riskLevel === 1 ? 'WARNING' : 'NORMAL'}
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
with open(os.path.join(DIR, "pages", "History.jsx"), "w", encoding="utf-8") as f:
    f.write(history_content)

print("IoTDashboard, Analytics, and History updated.")
