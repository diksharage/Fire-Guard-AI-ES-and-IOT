import React, { useContext, useState, useEffect } from 'react';
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
