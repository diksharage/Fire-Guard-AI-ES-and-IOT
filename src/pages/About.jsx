import React from 'react';
import { FileText, Cpu, Server, ShieldAlert } from 'lucide-react';

const About = () => {
  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold text-slate-50 mb-2">About FireGuard AI</h1>
        <p className="text-slate-400 text-lg">Virtual Fire & Smoke Early Warning Laboratory</p>
      </div>

      <div className="glass-card p-8 space-y-6 text-slate-300 leading-relaxed">
        
        <section>
          <h2 className="text-xl font-bold text-slate-50 mb-3 flex items-center gap-2"><ShieldAlert className="text-primary"/> The Problem & Solution</h2>
          <p className="mb-3">
            Small fires can escalate quickly into dangerous situations when abnormal smoke or temperature goes undetected early on. Traditional smoke detectors often trigger late or lack intelligent analysis to distinguish between minor issues and severe threats.
          </p>
          <p>
            <strong>Solution:</strong> This virtual laboratory simulates an ESP8266-based IoT early warning system. By combining physical sensor inputs (MQ-2, DHT11) with an AI Decision Tree classifier, the system continuously analyzes environmental conditions and rates of change to predict fire risks instantly.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-bold text-slate-50 mb-3 flex items-center gap-2"><Cpu className="text-primary"/> Simulated Hardware Components</h2>
          <ul className="list-disc list-inside space-y-2 ml-2">
            <li><strong>ESP8266 NodeMCU:</strong> The core microcontroller providing processing and Wi-Fi connectivity.</li>
            <li><strong>MQ-2 Gas Sensor:</strong> Detects smoke and combustible gases via analog input.</li>
            <li><strong>DHT11 Sensor:</strong> Measures ambient temperature via digital input.</li>
            <li><strong>LED Indicators:</strong> Visual state representation (Green = Normal, Yellow = Warning, Red = High Risk).</li>
            <li><strong>Piezo Buzzer:</strong> Provides local audible alerts during emergencies.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-slate-50 mb-3 flex items-center gap-2"><Server className="text-primary"/> Virtual vs. Real Hardware</h2>
          <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
            <p className="mb-2"><strong className="text-primary">VIRTUAL MODE (Current):</strong> The browser generates simulated sensor values. The Decision Tree runs in JavaScript, and the dashboard updates purely through software state.</p>
            <p><strong className="text-blue-400">REAL HARDWARE MODE:</strong> The exact same architecture can be applied to physical hardware. The real MQ-2 and DHT11 feed data to a physical ESP8266, which transmits JSON payloads over Wi-Fi to a backend server to drive this dashboard.</p>
          </div>
        </section>

        <section>
          <h2 className="text-xl font-bold text-slate-50 mb-3 flex items-center gap-2"><FileText className="text-primary"/> System Architecture</h2>
          <div className="bg-slate-900 p-6 rounded-lg font-mono text-sm text-center">
            <div className="text-slate-400">Environment</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-slate-50 font-bold border border-slate-700 inline-block px-4 py-2 rounded">MQ-2 + DHT11 Sensors</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-blue-400 font-bold border border-blue-900 bg-blue-900/20 inline-block px-4 py-2 rounded">ESP8266 Microcontroller</div>
            <div className="text-primary my-1">↓</div>
            <div className="text-purple-400 font-bold border border-purple-900 bg-purple-900/20 inline-block px-4 py-2 rounded">AI Risk Classification (Decision Tree)</div>
            <div className="text-primary my-1">↓</div>
            <div className="grid grid-cols-2 gap-4 mt-2 max-w-md mx-auto">
              <div className="text-red-400 border border-red-900 bg-red-900/20 p-2 rounded">Local: LED + Buzzer</div>
              <div className="text-green-400 border border-green-900 bg-green-900/20 p-2 rounded">Cloud: IoT Dashboard & Alerts</div>
            </div>
          </div>
        </section>
        
        <div className="text-xs text-slate-500 text-center mt-8 pt-4 border-t border-slate-800">
          This is an educational simulation created for demonstration purposes. 
          Thresholds and logic are designed to illustrate the concept of AI-based early warning systems and should not be used for actual life-safety applications without professional calibration.
        </div>
      </div>
    </div>
  );
};
export default About;
