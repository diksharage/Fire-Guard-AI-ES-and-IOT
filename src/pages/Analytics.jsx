import React, { useContext } from 'react';
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
