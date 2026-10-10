import React, { useContext } from 'react';
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

        {/* Disclaimer */}
        <div className="md:col-span-3 mt-4 p-4 border border-blue-900/50 bg-blue-900/10 rounded-lg text-sm text-slate-400">
          <strong>Note:</strong> This decision tree uses simplified simulation/demonstration thresholds to illustrate AI classification logic. It does not claim to represent universal real-world fire-safety standards.
        </div>
      </div>
    </div>
  );
};
export default AIClassifier;
