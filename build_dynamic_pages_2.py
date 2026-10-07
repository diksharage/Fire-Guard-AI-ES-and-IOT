import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

# ---------------------------------------------------------
# 3. ExperimentLab.jsx
# ---------------------------------------------------------
lab_content = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Sliders, Play, Pause, RotateCcw, AlertTriangle, ShieldAlert } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ExperimentLab = () => {
  const { 
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

  return (
    <div className="space-y-6 pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50 mb-2">Experiment Lab</h1>
          <p className="text-slate-400">Control the environmental parameters and observe the hardware response.</p>
        </div>
        
        <div className="flex gap-3 w-full md:w-auto">
          <button 
            onClick={() => { if(circuitReady) setIsRunning(!isRunning); else navigate('/circuit'); }}
            className={`flex-1 md:flex-none px-6 py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors ${!circuitReady ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : isRunning ? 'bg-amber-900/50 text-amber-500 border border-amber-700' : 'bg-green-600 hover:bg-green-500 text-white'}`}
          >
            {!circuitReady ? <><AlertTriangle size={18}/> Valid Circuit Required</> : isRunning ? <><Pause size={18}/> Pause Experiment</> : <><Play size={18}/> Start Experiment</>}
          </button>
          {isRunning && (
            <button onClick={handleReset} className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors">
              <RotateCcw size={18} />
            </button>
          )}
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
        <div className={`glass-card p-6 space-y-8 ${!isRunning && circuitReady ? 'opacity-50 pointer-events-none' : ''}`}>
          <div className="flex items-center gap-2 text-primary font-bold mb-2">
            <Sliders size={20} /> SIMULATION CONTROLS
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Temperature (°C)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-2 py-0.5 rounded">{temperature.toFixed(1)}</span>
            </div>
            <input type="range" min="10" max="80" step="0.5" value={temperature} onChange={(e) => setTemperature(parseFloat(e.target.value))} className="w-full accent-primary" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>10°C</span><span>80°C</span></div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Smoke / Gas Level (%)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-2 py-0.5 rounded">{smoke.toFixed(0)}</span>
            </div>
            <input type="range" min="0" max="100" value={smoke} onChange={(e) => setSmoke(parseFloat(e.target.value))} className="w-full accent-slate-400" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>0%</span><span>100%</span></div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300 font-semibold">Humidity (%)</span>
              <span className="text-slate-50 font-mono bg-slate-800 px-2 py-0.5 rounded">{humidity.toFixed(0)}</span>
            </div>
            <input type="range" min="10" max="90" value={humidity} onChange={(e) => setHumidity(parseFloat(e.target.value))} className="w-full accent-blue-500" />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono"><span>10%</span><span>90%</span></div>
          </div>
          
          <div className="mt-8 bg-blue-900/10 border border-blue-900/30 p-4 rounded-xl flex gap-3">
            <ShieldAlert className="text-blue-500/70 shrink-0 size-5" />
            <p className="text-blue-200/60 text-xs leading-relaxed">
              These sliders simulate physical environmental changes that the DHT11 and MQ-2 sensors would detect. Changing these values instantly updates the central AI model.
            </p>
          </div>
        </div>

        {/* Hardware Response */}
        <div className="space-y-6">
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-slate-50 mb-4 border-b border-slate-700 pb-2">Virtual Hardware Response</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 ${greenLedStatus ? 'bg-green-500 border-green-300 shadow-[0_0_20px_rgba(34,197,94,0.6)]' : 'bg-green-950 border-green-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Green LED</div>
                <div className="text-xs text-slate-500 font-mono">{greenLedStatus ? 'ON (D5 HIGH)' : 'OFF (D5 LOW)'}</div>
              </div>
              
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 ${yellowLedStatus ? 'bg-amber-500 border-amber-300 shadow-[0_0_20px_rgba(245,158,11,0.6)]' : 'bg-amber-950 border-amber-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Yellow LED</div>
                <div className="text-xs text-slate-500 font-mono">{yellowLedStatus ? 'ON (D6 HIGH)' : 'OFF (D6 LOW)'}</div>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full shadow-inner border-2 ${redLedStatus ? 'bg-red-500 border-red-300 shadow-[0_0_20px_rgba(239,68,68,0.6)] animate-pulse' : 'bg-red-950 border-red-900 opacity-30'}`}></div>
                <div className="text-sm font-bold text-slate-300">Red LED</div>
                <div className="text-xs text-slate-500 font-mono">{redLedStatus ? 'ON (D7 HIGH)' : 'OFF (D7 LOW)'}</div>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center gap-3">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 ${buzzerStatus ? 'bg-slate-800 border-red-500 text-red-500 animate-ping' : 'bg-slate-900 border-slate-700 text-slate-600'}`}>
                  <Volume2 size={24} />
                </div>
                <div className="text-sm font-bold text-slate-300">Buzzer</div>
                <div className="text-xs text-slate-500 font-mono">{buzzerStatus ? 'ON (D4 HIGH)' : 'OFF (D4 LOW)'}</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-slate-50 mb-2">AI Classification Result</h3>
            <div className={`p-4 rounded-lg font-bold text-center text-xl tracking-widest ${riskLevel === 2 ? 'bg-red-900/30 text-red-500 border border-red-500/50' : riskLevel === 1 ? 'bg-amber-900/30 text-amber-500 border border-amber-500/50' : 'bg-green-900/30 text-green-500 border border-green-500/50'}`}>
              {riskLevel === 2 ? 'HIGH FIRE RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL'}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
export default ExperimentLab;
"""
with open(os.path.join(DIR, "pages", "ExperimentLab.jsx"), "w", encoding="utf-8") as f:
    f.write(lab_content)


# ---------------------------------------------------------
# 4. AIClassifier.jsx
# ---------------------------------------------------------
ai_content = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { BrainCircuit, ArrowDown, Database, Cpu } from 'lucide-react';

const AIClassifier = () => {
  const { temperature, smoke, humidity, riskLevel, aiConfidence } = useContext(SimulationContext);

  const isHighSmoke = smoke >= 65;
  const isHighTemp = temperature >= 45;
  const isWarnSmoke = smoke >= 40 && smoke < 65;
  const isWarnTemp = temperature >= 35 && temperature < 45;

  return (
    <div className="space-y-6 pb-20">
      <div>
        <h1 className="text-3xl font-bold text-slate-50 mb-2">AI Classifier Logic</h1>
        <p className="text-slate-400">Real-time explainable decision tree execution based on current simulation state.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Input Features */}
        <div className="md:col-span-1 space-y-4">
          <div className="glass-card p-4">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2"><Database size={16}/> Current Inputs</h3>
            <div className="space-y-3">
              <div className="bg-slate-900 p-3 rounded border border-slate-700 flex justify-between">
                <span className="text-slate-300">Temperature</span>
                <span className="font-mono text-slate-50 font-bold">{temperature.toFixed(1)} °C</span>
              </div>
              <div className="bg-slate-900 p-3 rounded border border-slate-700 flex justify-between">
                <span className="text-slate-300">Smoke Level</span>
                <span className="font-mono text-slate-50 font-bold">{smoke.toFixed(0)} %</span>
              </div>
              <div className="bg-slate-900 p-3 rounded border border-slate-700 flex justify-between">
                <span className="text-slate-300">Humidity</span>
                <span className="font-mono text-slate-50 font-bold">{humidity.toFixed(0)} %</span>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-4">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2"><Cpu size={16}/> Model Status</h3>
            <div className="flex justify-between items-center mb-2">
              <span className="text-slate-300">Confidence</span>
              <span className="font-mono text-primary font-bold">{aiConfidence}%</span>
            </div>
            <div className="w-full bg-slate-900 rounded-full h-2">
              <div className="bg-primary h-2 rounded-full" style={{width: `${aiConfidence}%`}}></div>
            </div>
          </div>
        </div>

        {/* Decision Tree */}
        <div className="md:col-span-2 glass-card p-6 flex flex-col items-center">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6 w-full text-center flex justify-center items-center gap-2"><BrainCircuit size={18} /> Active Decision Path</h3>
          
          <div className={`p-4 rounded-lg border w-64 text-center font-bold shadow-lg ${isHighSmoke || isWarnSmoke ? 'bg-amber-900/30 border-amber-500 text-amber-400' : 'bg-slate-800 border-slate-600 text-slate-300'}`}>
            Smoke {'>='} 40% ?<br/>
            <span className="text-xs font-normal opacity-70">Current: {smoke.toFixed(0)}%</span>
          </div>
          <ArrowDown className="text-slate-600 my-2" />
          
          <div className={`p-4 rounded-lg border w-64 text-center font-bold shadow-lg ${isHighSmoke ? 'bg-red-900/30 border-red-500 text-red-400' : isHighTemp || isWarnTemp ? 'bg-amber-900/30 border-amber-500 text-amber-400' : 'bg-slate-800 border-slate-600 text-slate-300'}`}>
            Temperature {'>='} 35°C ?<br/>
            <span className="text-xs font-normal opacity-70">Current: {temperature.toFixed(1)}°C</span>
          </div>
          <ArrowDown className="text-slate-600 my-2" />

          <div className="grid grid-cols-3 gap-4 w-full mt-4">
            <div className={`p-4 rounded-lg border text-center flex flex-col justify-center ${riskLevel === 0 ? 'bg-green-900/30 border-green-500 shadow-[0_0_15px_rgba(34,197,94,0.3)]' : 'bg-slate-900 border-slate-800 opacity-40'}`}>
              <h4 className="font-bold text-green-500 mb-1">NORMAL</h4>
              <p className="text-[10px] text-slate-400">Condition Not Met</p>
            </div>
            <div className={`p-4 rounded-lg border text-center flex flex-col justify-center ${riskLevel === 1 ? 'bg-amber-900/30 border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.3)]' : 'bg-slate-900 border-slate-800 opacity-40'}`}>
              <h4 className="font-bold text-amber-500 mb-1">WARNING</h4>
              <p className="text-[10px] text-slate-400">Partial Thresholds</p>
            </div>
            <div className={`p-4 rounded-lg border text-center flex flex-col justify-center ${riskLevel === 2 ? 'bg-red-900/30 border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)]' : 'bg-slate-900 border-slate-800 opacity-40'}`}>
              <h4 className="font-bold text-red-500 mb-1">HIGH FIRE RISK</h4>
              <p className="text-[10px] text-slate-400">Critical Thresholds</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
export default AIClassifier;
"""
with open(os.path.join(DIR, "pages", "AIClassifier.jsx"), "w", encoding="utf-8") as f:
    f.write(ai_content)

print("ExperimentLab and AIClassifier updated.")
