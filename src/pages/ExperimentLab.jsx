import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Sliders, Play, Pause, RotateCcw, AlertTriangle, ShieldAlert, Volume2, VolumeX } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ExperimentLab = () => {
  const { 
    isSoundEnabled, setIsSoundEnabled,
    temperature, setTemperature, 
    smoke, setSmoke, 
    humidity, setHumidity,
    riskLevel, isRunning, setIsRunning,
    circuitReady,
    buzzerStatus, greenLedStatus, yellowLedStatus, redLedStatus 
  } = useContext(SimulationContext);
  
  const navigate = useNavigate();

  const handleReset = () => {
    setIsRunning(false);
    setTemperature(25);
    setSmoke(10);
    setHumidity(45);
  };

  const setScenario = (type) => {
    if(type === 'normal') { setTemperature(25); setSmoke(10); }
    if(type === 'warning') { setTemperature(38); setSmoke(45); }
    if(type === 'danger') { setTemperature(55); setSmoke(85); }
  };

  return (
    <div className="space-y-6 pb-20">
      
      {/* Guided Progress Indicator */}
      <div className="hidden md:flex justify-between items-center bg-slate-800/50 p-3 rounded-xl border border-slate-700 text-sm font-semibold text-slate-400">
        <div className="flex items-center gap-2 text-green-500"><span className="w-5 h-5 rounded-full bg-green-500/20 flex items-center justify-center">1</span> Circuit Ready ✓</div>
        <div className="h-px bg-slate-700 flex-1 mx-4"></div>
        <div className={`flex items-center gap-2 ${isRunning ? 'text-green-500' : 'text-slate-200'}`}><span className={`w-5 h-5 rounded-full flex items-center justify-center ${isRunning ? 'bg-green-500/20' : 'bg-primary text-slate-900'}`}>2</span> Start Experiment</div>
        <div className="h-px bg-slate-700 flex-1 mx-4"></div>
        <div className={`flex items-center gap-2 ${isRunning ? 'text-primary' : ''}`}><span className={`w-5 h-5 rounded-full flex items-center justify-center ${isRunning ? 'bg-primary text-slate-900' : 'bg-slate-700'}`}>3</span> Set Environment</div>
        <div className="h-px bg-slate-700 flex-1 mx-4"></div>
        <div className="flex items-center gap-2"><span className="w-5 h-5 rounded-full bg-slate-700 flex items-center justify-center">4</span> Observe Response</div>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">Experiment Lab</h1>
          <p className="text-slate-400">Control the environmental parameters and observe the hardware response.</p>
        </div>
        
        <div className="flex gap-3 w-full md:w-auto">
          <button 
            onClick={() => { if(circuitReady) setIsRunning(!isRunning); else navigate('/circuit'); }}
            className={`flex-1 md:flex-none px-8 py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors text-lg shadow-lg ${!circuitReady ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : isRunning ? 'bg-amber-900/50 text-amber-500 border border-amber-700' : 'bg-primary hover:bg-primary-bright text-slate-900'}`}
          >
            {!circuitReady ? <><AlertTriangle size={20}/> Valid Circuit Required</> : isRunning ? <><Pause size={20}/> Pause Experiment</> : <><Play size={20}/> START EXPERIMENT</>}
          </button>
          {isRunning && (
            <button onClick={handleReset} className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors shadow-lg" title="Reset Experiment">
              <RotateCcw size={20} />
            </button>
          )}
          <button 
            onClick={() => setIsSoundEnabled(!isSoundEnabled)} 
            className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors shadow-lg" 
            title={isSoundEnabled ? "Mute Buzzer" : "Unmute Buzzer"}
          >
            {isSoundEnabled ? <Volume2 size={20} className="text-green-400" /> : <VolumeX size={20} className="text-slate-500" />}
          </button>
        </div>
      </div>

      {!circuitReady && (
        <div className="bg-red-900/20 border border-red-700/50 p-4 rounded-xl flex gap-3 text-red-400">
          <AlertTriangle className="shrink-0" />
          <div>
            <h4 className="font-bold mb-1">Cannot Start Simulation</h4>
            <p className="text-sm text-red-300/80 mb-3">You must build and validate the virtual circuit before running experiments.</p>
            <button onClick={() => navigate('/circuit')} className="px-4 py-2 bg-red-900/50 hover:bg-red-800 text-white rounded text-sm transition">Go to Virtual Circuit</button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Environment Controls */}
        <div className={`glass-card p-6 space-y-6 ${!isRunning && circuitReady ? 'opacity-50 pointer-events-none' : ''}`}>
          <div className="flex items-center justify-between border-b border-slate-700 pb-2">
            <div className="flex items-center gap-2 text-primary font-bold">
              <Sliders size={20} /> ENVIRONMENT SIMULATION
            </div>
          </div>
          
          <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700 space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">1-Click Demonstration Scenarios</h4>
            <div className="grid grid-cols-3 gap-2">
              <button onClick={() => setScenario('normal')} className="px-2 py-2 bg-green-900/30 hover:bg-green-900/50 border border-green-700/50 text-green-400 rounded text-sm font-bold transition">Normal</button>
              <button onClick={() => setScenario('warning')} className="px-2 py-2 bg-amber-900/30 hover:bg-amber-900/50 border border-amber-700/50 text-amber-400 rounded text-sm font-bold transition">Warning</button>
              <button onClick={() => setScenario('danger')} className="px-2 py-2 bg-red-900/30 hover:bg-red-900/50 border border-red-700/50 text-red-400 rounded text-sm font-bold transition">High Fire Risk</button>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Temperature (°C)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-3 py-1 rounded shadow-inner text-lg font-bold">{temperature.toFixed(1)}</span>
            </div>
            <input type="range" min="10" max="80" step="0.5" value={temperature} onChange={(e) => setTemperature(parseFloat(e.target.value))} className="w-full accent-primary h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>10°C</span><span>80°C</span></div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Smoke / Gas Level (%)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-3 py-1 rounded shadow-inner text-lg font-bold">{smoke.toFixed(0)}</span>
            </div>
            <input type="range" min="0" max="100" value={smoke} onChange={(e) => setSmoke(parseFloat(e.target.value))} className="w-full accent-slate-400 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>0%</span><span>100%</span></div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Humidity (%)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-3 py-1 rounded shadow-inner text-lg font-bold">{humidity.toFixed(0)}</span>
            </div>
            <input type="range" min="10" max="90" value={humidity} onChange={(e) => setHumidity(parseFloat(e.target.value))} className="w-full accent-blue-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>10%</span><span>90%</span></div>
          </div>
          
          <div className="mt-8 bg-blue-900/10 border border-blue-900/30 p-4 rounded-xl flex gap-3">
            <ShieldAlert className="text-blue-500/70 shrink-0 size-5" />
            <p className="text-blue-200/60 text-xs leading-relaxed">
              These scenarios are for demonstration only. Changing these values instantly updates the central AI model and simulates physical hardware responses.
            </p>
          </div>
        </div>

        {/* Hardware Response */}
        <div className="space-y-6">
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-slate-50 mb-4 border-b border-slate-700 pb-2">Virtual Hardware Response</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 transition-all duration-300 ${greenLedStatus ? 'bg-green-500 border-green-300 shadow-[0_0_20px_rgba(34,197,94,0.6)]' : 'bg-green-950 border-green-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Green LED</div>
                <div className="text-xs text-slate-500 font-mono">{greenLedStatus ? 'ON (D5 HIGH)' : 'OFF (D5 LOW)'}</div>
              </div>
              
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 transition-all duration-300 ${yellowLedStatus ? 'bg-amber-500 border-amber-300 shadow-[0_0_20px_rgba(245,158,11,0.6)]' : 'bg-amber-950 border-amber-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Yellow LED</div>
                <div className="text-xs text-slate-500 font-mono">{yellowLedStatus ? 'ON (D6 HIGH)' : 'OFF (D6 LOW)'}</div>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 transition-all duration-300 ${redLedStatus ? 'bg-red-500 border-red-300 shadow-[0_0_20px_rgba(239,68,68,0.6)] animate-pulse' : 'bg-red-950 border-red-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Red LED</div>
                <div className="text-xs text-slate-500 font-mono">{redLedStatus ? 'ON (D7 HIGH)' : 'OFF (D7 LOW)'}</div>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${buzzerStatus ? 'bg-slate-800 border-red-500 text-red-500 animate-ping' : 'bg-slate-900 border-slate-700 text-slate-600'}`}>
                  <Volume2 size={24} />
                </div>
                <div className="text-sm font-bold text-slate-300">Buzzer</div>
                <div className="text-xs text-slate-500 font-mono">{buzzerStatus ? 'ON (D4 HIGH)' : 'OFF (D4 LOW)'}</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-slate-50 mb-2">AI Classification Result</h3>
            <div className={`p-4 rounded-lg font-bold text-center text-2xl tracking-widest transition-colors duration-300 ${riskLevel === 2 ? 'bg-red-900/30 text-red-500 border border-red-500/50' : riskLevel === 1 ? 'bg-amber-900/30 text-amber-500 border border-amber-500/50' : 'bg-green-900/30 text-green-500 border border-green-500/50'}`}>
              {riskLevel === 2 ? 'HIGH FIRE RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL'}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
export default ExperimentLab;
