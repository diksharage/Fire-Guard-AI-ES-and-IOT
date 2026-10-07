import React, { useContext } from 'react';
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
