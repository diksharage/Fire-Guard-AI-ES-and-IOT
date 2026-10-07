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
              <span className="text-sm font-bold text-primary">{targetTemp}°C</span>
            </div>
            <input 
              type="range" min="10" max="100" step="1" 
              value={targetTemp} 
              onChange={(e) => setTargetTemp(Number(e.target.value))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary"
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
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg font-medium transition ${isRunning ? 'bg-slate-700 hover:bg-slate-600 text-slate-50' : 'bg-green-600 hover:bg-green-500 text-slate-50'}`}
            >
              {isRunning ? <><Square size={18} /> Pause Sim</> : <><Play size={18} /> Resume Sim</>}
            </button>
            <button 
              onClick={resetSimulation}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-slate-700 hover:bg-slate-600 text-slate-50 rounded-lg font-medium transition"
            >
              <RotateCcw size={18} /> Reset
            </button>
            <button 
              onClick={() => setDemoMode(!demoMode)}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg font-medium transition ${demoMode ? 'bg-primary text-slate-50 animate-pulse' : 'bg-slate-800 text-primary border border-primary/50'}`}
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
