import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages"

content = """import React, { useState, useContext, useEffect } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { REQUIRED_CONNECTIONS } from './VirtualCircuit';
import { useNavigate } from 'react-router-dom';
import { BookOpen, CheckCircle, ChevronRight, ChevronLeft, AlertTriangle, ArrowRight, Info, ShieldAlert } from 'lucide-react';

const STEPS = [
  "Experiment Overview",
  "Required Components",
  "Before You Start",
  "Place Components",
  "Power Connections",
  "Connect MQ-2",
  "Connect DHT11",
  "Connect Outputs",
  "Validate Circuit",
  "Run & Observe"
];

const Guidelines = () => {
  const { circuitWires, circuitValidation, setCircuitValidation, circuitReady, setCircuitReady, isRunning, setIsRunning, riskLevel, temperature, smoke } = useContext(SimulationContext);
  const navigate = useNavigate();
  
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState(() => {
    const saved = localStorage.getItem('fireguard_guidelines');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('fireguard_guidelines', JSON.stringify(completedSteps));
  }, [completedSteps]);

  const markCompleted = () => {
    if (!completedSteps.includes(currentStep)) {
      setCompletedSteps([...completedSteps, currentStep]);
    }
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const validateCircuit = () => {
    const missing = [];
    let correctCount = 0;
    REQUIRED_CONNECTIONS.forEach(req => {
      const exists = circuitWires.some(w => {
        const fwd = w.startComp === req.fromComp && w.startPin === req.fromPin && w.endComp === req.toComp && req.toPins.includes(w.endPin);
        const rev = w.endComp === req.fromComp && w.endPin === req.fromPin && w.startComp === req.toComp && req.toPins.includes(w.startPin);
        return fwd || rev;
      });
      if (exists) correctCount++;
      else missing.push(req.desc);
    });
    const isValid = missing.length === 0;
    setCircuitValidation({ status: 'validated', missing, correct: correctCount, total: REQUIRED_CONNECTIONS.length, valid: isValid });
    if (isValid) setCircuitReady(true);
  };

  return (
    <div className="space-y-6 pb-20">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-amber-900/30 text-primary border border-primary/30 rounded-full text-xs font-bold mb-3 tracking-wider">
            <BookOpen size={14} /> GUIDED EXPERIMENT
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Experiment Guidelines</h1>
          <p className="text-slate-400">Step-by-step procedure for building, validating, and running the Early Warning System.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1 glass-card p-4 space-y-2">
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 px-2">Progress</h3>
          {STEPS.map((step, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentStep(idx)}
              className={`w-full flex items-center justify-between p-3 rounded-lg text-left transition-all ${currentStep === idx ? 'bg-primary/20 border border-primary/50 text-white' : 'hover:bg-slate-800 text-slate-400 border border-transparent'}`}
            >
              <span className="flex items-center gap-3 text-sm">
                <span className={`flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${completedSteps.includes(idx) ? 'bg-green-500 text-white' : 'bg-slate-700 text-slate-300'}`}>
                  {completedSteps.includes(idx) ? <CheckCircle size={14} /> : idx}
                </span>
                {step}
              </span>
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="lg:col-span-3 space-y-6">
          <div className="glass-card p-8 min-h-[500px] flex flex-col">
            
            {/* Step 0: Overview */}
            {currentStep === 0 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Experiment Objective</h2>
                <p className="text-slate-300 leading-relaxed text-lg">
                  The objective of this experiment is to build and simulate an IoT-based fire and smoke early warning system using an ESP8266, MQ-2 smoke/gas sensor, DHT11 temperature sensor, LEDs and buzzer. Sensor readings are processed by the system and classified into Normal, Warning or High Fire Risk states.
                </p>
                <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 flex flex-col md:flex-row items-center justify-between gap-4 text-center">
                  <div className="flex-1"><div className="font-bold text-primary mb-1">MQ-2 / DHT11</div><div className="text-sm text-slate-400">Environmental Sensors</div></div>
                  <ArrowRight className="text-slate-500 hidden md:block" />
                  <div className="flex-1"><div className="font-bold text-blue-400 mb-1">ESP8266 NodeMCU</div><div className="text-sm text-slate-400">AI Risk Classifier</div></div>
                  <ArrowRight className="text-slate-500 hidden md:block" />
                  <div className="flex-1"><div className="font-bold text-red-400 mb-1">LEDs + Buzzer</div><div className="text-sm text-slate-400">Dashboard Alerts</div></div>
                </div>
              </div>
            )}

            {/* Step 1: Components */}
            {currentStep === 1 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Required Components</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl flex gap-4 items-start">
                    <img src="/images/esp8266.jpg" className="w-20 h-20 object-cover rounded bg-white p-1" alt="ESP8266" onError={(e) => e.target.style.display='none'} />
                    <div>
                      <h4 className="font-bold text-white">ESP8266 NodeMCU</h4>
                      <p className="text-xs text-slate-400 mb-2">Main controller. Reads sensors and processes AI.</p>
                      <div className="flex flex-wrap gap-1"><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">A0</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">D2-D7</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">3V3</span></div>
                    </div>
                  </div>
                  <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl flex gap-4 items-start">
                    <img src="/images/dht11.jpg" className="w-20 h-20 object-cover rounded bg-white p-1" alt="DHT11" onError={(e) => e.target.style.display='none'} />
                    <div>
                      <h4 className="font-bold text-white">DHT11 Sensor</h4>
                      <p className="text-xs text-slate-400 mb-2">Measures temperature and humidity.</p>
                      <div className="flex flex-wrap gap-1"><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">VCC</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">DATA</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">GND</span></div>
                    </div>
                  </div>
                  <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl flex gap-4 items-start">
                    <div className="w-20 h-20 rounded bg-slate-800 border border-slate-600 flex items-center justify-center font-bold text-slate-400">MQ-2</div>
                    <div>
                      <h4 className="font-bold text-white">MQ-2 Gas Sensor</h4>
                      <p className="text-xs text-slate-400 mb-2">Detects smoke and combustible gases.</p>
                      <div className="flex flex-wrap gap-1"><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">VCC</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">GND</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">AO</span></div>
                    </div>
                  </div>
                  <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl flex gap-4 items-start">
                    <img src="/images/resistor.jpg" className="w-20 h-20 object-cover rounded bg-white p-1" alt="Resistor" onError={(e) => e.target.style.display='none'} />
                    <div>
                      <h4 className="font-bold text-white">LEDs + Resistors</h4>
                      <p className="text-xs text-slate-400 mb-2">Visual indicators. Require 220Ω series resistors.</p>
                      <div className="flex flex-wrap gap-1"><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">Anode</span><span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-mono">Cathode</span></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Checklist */}
            {currentStep === 2 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Before You Start</h2>
                <div className="space-y-3">
                  {['All virtual components are available in the workspace', 'Breadboard orientation is understood', 'Power and ground rails are identified', 'Sensor pins are identified', 'MQ-2 analog output compatibility is checked'].map((item, i) => (
                    <label key={i} className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700 cursor-pointer hover:bg-slate-800">
                      <input type="checkbox" className="w-5 h-5 rounded border-slate-600 text-primary focus:ring-primary bg-slate-900" />
                      <span className="text-slate-300">{item}</span>
                    </label>
                  ))}
                </div>
                <div className="bg-amber-900/20 border border-amber-700/50 p-4 rounded-xl flex gap-3">
                  <AlertTriangle className="text-amber-500 shrink-0" />
                  <p className="text-amber-200/80 text-sm">Do not assume that every physical MQ-2 module has the same output voltage. Verify the module specification before connecting physical AO to an ESP8266 analog input. Never test the real system using an open flame.</p>
                </div>
              </div>
            )}

            {/* Step 3: Place */}
            {currentStep === 3 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 1: Place the Components</h2>
                <p className="text-slate-300">Arrange the components on your virtual workbench logically to keep wiring organized.</p>
                <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 font-mono text-sm text-center text-slate-400 leading-loose">
                  [ MQ-2 ] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ DHT11 ] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ LEDs ] <br/>
                  │ <br/>
                  ┌──────────────────────────────┐<br/>
                  │ BREADBOARD                   │<br/>
                  └──────────────────────────────┘<br/>
                  │ <br/>
                  [ ESP8266 ] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ BUZZER ]
                </div>
                <button onClick={() => navigate('/circuit')} className="w-full py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold border border-slate-600 transition">Open Virtual Circuit</button>
              </div>
            )}

            {/* Step 4: Power */}
            {currentStep === 4 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 2: Power Connections</h2>
                <p className="text-slate-300">First establish the common ground and appropriate power connections between the ESP8266 and the components.</p>
                <ul className="space-y-4">
                  <li className="flex items-center gap-4 bg-slate-800 p-4 rounded-lg">
                    <span className="text-red-400 font-bold w-12 text-center">VCC</span>
                    <div className="h-0.5 flex-1 bg-red-400/30 relative"><div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1 border-4 border-transparent border-l-red-400/50"></div></div>
                    <span className="text-slate-300 text-sm">ESP8266 <strong className="text-white">3V3</strong> / <strong className="text-white">VIN</strong></span>
                  </li>
                  <li className="flex items-center gap-4 bg-slate-800 p-4 rounded-lg">
                    <span className="text-slate-400 font-bold w-12 text-center">GND</span>
                    <div className="h-0.5 flex-1 bg-slate-400/30 relative"><div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1 border-4 border-transparent border-l-slate-400/50"></div></div>
                    <span className="text-slate-300 text-sm">ESP8266 <strong className="text-white">GND</strong></span>
                  </li>
                </ul>
              </div>
            )}

            {/* Step 5: MQ2 */}
            {currentStep === 5 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 3: Connect MQ-2</h2>
                <p className="text-slate-300">The MQ-2 provides a continuously varying analog voltage representing smoke concentration.</p>
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
                  <div className="font-mono text-lg font-bold text-primary mb-2">MQ-2 AO &nbsp; ────→ &nbsp; ESP8266 A0</div>
                  <p className="text-sm text-slate-400">Connect the analog output (AO) to the ESP8266's single analog input pin (A0).</p>
                </div>
              </div>
            )}

            {/* Step 6: DHT11 */}
            {currentStep === 6 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 4: Connect DHT11</h2>
                <p className="text-slate-300">The DHT11 uses a proprietary 1-wire digital protocol to send temperature and humidity.</p>
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
                  <div className="font-mono text-lg font-bold text-blue-400 mb-2">DHT11 DATA &nbsp; ────→ &nbsp; ESP8266 D2</div>
                  <p className="text-sm text-slate-400">Connect the data pin to digital GPIO D2.</p>
                </div>
              </div>
            )}

            {/* Step 7: Outputs */}
            {currentStep === 7 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 5 & 6: Connect Outputs</h2>
                <p className="text-slate-300">Connect the visual and audible indicators. <strong className="text-red-400">IMPORTANT:</strong> LEDs must be connected in series with a 220Ω resistor to prevent burnout.</p>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm text-slate-300 bg-slate-900 rounded-lg overflow-hidden">
                    <thead className="bg-slate-800 text-white">
                      <tr><th className="p-3">Component</th><th className="p-3">ESP8266 Pin</th><th className="p-3">Purpose</th></tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                      <tr><td className="p-3">Green LED (+ Resistor)</td><td className="p-3 font-mono">D5</td><td className="p-3">NORMAL indicator</td></tr>
                      <tr><td className="p-3">Yellow LED (+ Resistor)</td><td className="p-3 font-mono">D6</td><td className="p-3">WARNING indicator</td></tr>
                      <tr><td className="p-3">Red LED (+ Resistor)</td><td className="p-3 font-mono">D7</td><td className="p-3">HIGH RISK indicator</td></tr>
                      <tr><td className="p-3">Buzzer (+)</td><td className="p-3 font-mono">D4</td><td className="p-3">Audible Alert</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Step 8: Validate */}
            {currentStep === 8 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 7: Validate the Circuit</h2>
                <p className="text-slate-300">Ensure your physical or virtual wiring matches the required connections.</p>
                
                <button onClick={validateCircuit} className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold border border-slate-600 transition text-lg">
                  VALIDATE CIRCUIT
                </button>
                
                {circuitValidation.status === 'validated' && (
                  <div className={`p-4 rounded-xl border ${circuitValidation.valid ? 'bg-green-900/30 border-green-700' : 'bg-red-900/20 border-red-800'}`}>
                    {circuitValidation.valid ? (
                      <div className="flex items-center gap-3 text-green-400 font-bold text-lg"><CheckCircle /> CIRCUIT VALID</div>
                    ) : (
                      <div>
                        <div className="flex items-center gap-3 text-red-400 font-bold text-lg mb-3"><AlertTriangle /> CIRCUIT INCOMPLETE</div>
                        <p className="text-slate-300 text-sm mb-2">The following connections are missing or incorrect:</p>
                        <ul className="list-disc pl-5 text-red-300/80 text-sm space-y-1 mb-4">
                          {circuitValidation.missing.map((m, i) => <li key={i}>{m}</li>)}
                        </ul>
                        <button onClick={() => navigate('/circuit')} className="px-4 py-2 bg-red-900/50 hover:bg-red-800 text-white rounded text-sm transition">Fix in Virtual Circuit</button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Step 9: Simulate */}
            {currentStep === 9 && (
              <div className="animate-fade-in space-y-6 flex-1">
                <h2 className="text-2xl font-bold text-white border-b border-slate-700 pb-4">Step 8 & 9: Run & Observe</h2>
                <p className="text-slate-300">Start the simulation and change the environmental parameters in the Experiment Lab.</p>
                
                <div className="flex gap-4 mb-6">
                  <button 
                    onClick={() => { if(circuitReady) setIsRunning(!isRunning); else navigate('/circuit'); }} 
                    className={`flex-1 py-4 rounded-xl font-bold transition flex items-center justify-center gap-2 ${circuitReady ? (isRunning ? 'bg-green-900/50 text-green-500 border border-green-800' : 'bg-primary text-white hover:bg-primary-bright') : 'bg-slate-800 text-slate-500 cursor-not-allowed'}`}
                  >
                    {circuitReady ? (isRunning ? 'SIMULATION RUNNING' : 'START SIMULATION') : 'VALIDATE CIRCUIT FIRST'}
                  </button>
                  <button onClick={() => navigate('/lab')} className="flex-1 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold border border-slate-600 transition">
                    Open Experiment Lab
                  </button>
                </div>

                <div className="grid grid-cols-3 gap-4 text-center">
                  <div className={`p-4 rounded-xl border ${riskLevel === 0 ? 'bg-green-900/30 border-green-500' : 'bg-slate-900 border-slate-700 opacity-50'}`}>
                    <h4 className="font-bold text-green-500 mb-2">NORMAL</h4>
                    <p className="text-xs text-slate-400">Green LED ON<br/>Buzzer OFF</p>
                  </div>
                  <div className={`p-4 rounded-xl border ${riskLevel === 1 ? 'bg-amber-900/30 border-amber-500' : 'bg-slate-900 border-slate-700 opacity-50'}`}>
                    <h4 className="font-bold text-amber-500 mb-2">WARNING</h4>
                    <p className="text-xs text-slate-400">Yellow LED ON<br/>Buzzer Alert</p>
                  </div>
                  <div className={`p-4 rounded-xl border ${riskLevel === 2 ? 'bg-red-900/30 border-red-500' : 'bg-slate-900 border-slate-700 opacity-50'}`}>
                    <h4 className="font-bold text-red-500 mb-2">HIGH RISK</h4>
                    <p className="text-xs text-slate-400">Red LED ON<br/>Buzzer ON</p>
                  </div>
                </div>

                <div className="mt-8 bg-blue-900/20 border border-blue-800/50 p-4 rounded-xl flex gap-3">
                  <ShieldAlert className="text-blue-500 shrink-0" />
                  <p className="text-blue-200/80 text-sm leading-relaxed">
                    <strong>Safety Note:</strong> The project is an educational early-warning prototype, not a certified fire-safety system. The exact classification thresholds are demonstration parameters and must be calibrated for the intended hardware and environment.
                  </p>
                </div>
              </div>
            )}

            {/* Navigation Footer */}
            <div className="mt-8 pt-4 border-t border-slate-700 flex justify-between">
              <button 
                onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                disabled={currentStep === 0}
                className="flex items-center gap-2 px-4 py-2 text-slate-400 hover:text-white disabled:opacity-30 transition"
              >
                <ChevronLeft size={20} /> Previous
              </button>
              <button 
                onClick={markCompleted}
                className="flex items-center gap-2 px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-bright transition font-bold"
              >
                {currentStep === STEPS.length - 1 ? 'Complete Experiment' : 'Next Step'} <ChevronRight size={20} />
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};
export default Guidelines;
"""

with open(os.path.join(DIR, "Guidelines.jsx"), "w", encoding="utf-8") as f:
    f.write(content)
print("Guidelines.jsx generated successfully.")
