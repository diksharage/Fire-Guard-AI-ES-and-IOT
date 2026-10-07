import codecs

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx"
temp_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\vc_temp.txt"

with codecs.open(temp_path, 'r', 'utf-16le') as f:
    content = f.read()

content = content.replace('const VirtualCircuit = () => {', 
'''const VirtualCircuit = () => {
  const [wiringMode, setWiringMode] = useState('easy');
  const [autoBuilt, setAutoBuilt] = useState(false);

  const handleAutoBuild = () => {
    const autoWires = [
      { id: 'w1', startComp: 'esp', startPin: 'A0', endComp: 'mq2', endPin: 'AO', color: '#3b82f6' },
      { id: 'w2', startComp: 'esp', startPin: '3V3_1', endComp: 'mq2', endPin: 'VCC', color: '#ef4444' },
      { id: 'w3', startComp: 'esp', startPin: 'GND1', endComp: 'mq2', endPin: 'GND', color: '#1f2937' },
      { id: 'w4', startComp: 'esp', startPin: 'D2', endComp: 'dht11', endPin: 'DATA', color: '#eab308' },
      { id: 'w5', startComp: 'esp', startPin: '3V3_1', endComp: 'dht11', endPin: 'VCC', color: '#ef4444' },
      { id: 'w6', startComp: 'esp', startPin: 'GND1', endComp: 'dht11', endPin: 'GND', color: '#1f2937' },
      { id: 'w7', startComp: 'esp', startPin: 'D5', endComp: 'led_g', endPin: 'A', color: '#22c55e' },
      { id: 'w8', startComp: 'esp', startPin: 'GND2', endComp: 'led_g', endPin: 'C', color: '#1f2937' },
      { id: 'w9', startComp: 'esp', startPin: 'D6', endComp: 'led_y', endPin: 'A', color: '#eab308' },
      { id: 'w10', startComp: 'esp', startPin: 'GND2', endComp: 'led_y', endPin: 'C', color: '#1f2937' },
      { id: 'w11', startComp: 'esp', startPin: 'D7', endComp: 'led_r', endPin: 'A', color: '#ef4444' },
      { id: 'w12', startComp: 'esp', startPin: 'GND3', endComp: 'led_r', endPin: 'C', color: '#1f2937' },
      { id: 'w13', startComp: 'esp', startPin: 'D4', endComp: 'buzzer', endPin: 'POS', color: '#f97316' },
      { id: 'w14', startComp: 'esp', startPin: 'GND4', endComp: 'buzzer', endPin: 'NEG', color: '#1f2937' },
    ];
    setWires(autoWires);
    setAutoBuilt(true);
    setValidation({ status: 'validated', missing: [], valid: true, correct: 14, total: 14 });
    setCircuitReady(true);
  };
''')

# Fix header buttons
content = content.replace(
'''<div className="flex gap-3">
          <button onClick={validateCircuit} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-lg border border-slate-700 transition">
            <CheckCircle size={18} /> Validate Circuit
          </button>
          <button 
            onClick={() => circuitReady && setIsRunning(!isRunning)}''',
'''<div className="flex gap-3">
          {wiringMode === 'advanced' && (
            <button onClick={validateCircuit} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-lg border border-slate-700 transition">
              <CheckCircle size={18} /> Validate Circuit
            </button>
          )}
          <button 
            onClick={() => circuitReady && setIsRunning(!isRunning)}''')

# Replace Inspector Sidebar
inspector_search = '''{/* Inspector Sidebar */}
          <div className="flex flex-col gap-6">
            <div className="glass-card p-5 h-64 overflow-y-auto">'''

mode_ui = '''{/* Inspector Sidebar */}
          <div className="flex flex-col gap-6">
            <div className="glass-card p-1 flex bg-slate-900 rounded-xl">
               <button onClick={() => setWiringMode('easy')} className={`flex-1 py-2 text-sm font-bold rounded-lg transition-colors ${wiringMode === 'easy' ? 'bg-primary text-slate-900 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}>Easy Mode</button>
               <button onClick={() => setWiringMode('advanced')} className={`flex-1 py-2 text-sm font-bold rounded-lg transition-colors ${wiringMode === 'advanced' ? 'bg-slate-700 text-slate-100 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}>Advanced Wiring</button>
            </div>
            
            {wiringMode === 'easy' && !circuitReady && (
               <div className="glass-card p-5 flex flex-col gap-4">
                  <h3 className="text-lg font-bold text-slate-50 mb-1 flex items-center gap-2"><Cpu size={18} className="text-primary"/> Auto Build</h3>
                  <p className="text-sm text-slate-400">Instantly wire the correct circuit for demonstration.</p>
                  <button onClick={handleAutoBuild} className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold border border-slate-600 transition text-lg">Build Circuit Automatically</button>
               </div>
            )}
            
            {wiringMode === 'easy' && circuitReady && (
               <div className="glass-card p-5 flex flex-col gap-4 border-2 border-green-500/50">
                  <h3 className="text-lg font-bold text-slate-50 mb-1 flex items-center gap-2"><CheckCircle size={18} className="text-green-500"/> Circuit Ready</h3>
                  <div className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-300 space-y-1 mb-2">
                    <div>✓ MQ-2 → A0</div>
                    <div>✓ DHT11 → D2</div>
                    <div>✓ Green LED → D5</div>
                    <div>✓ Yellow LED → D6</div>
                    <div>✓ Red LED → D7</div>
                    <div>✓ Buzzer → D4</div>
                  </div>
                  <button onClick={() => window.location.href='/lab'} className="w-full py-4 bg-primary hover:bg-primary-bright text-slate-900 rounded-xl font-bold transition text-lg flex items-center justify-center gap-2 shadow-[0_0_15px_rgba(245,158,11,0.5)]">
                    <Play size={20}/> START EXPERIMENT
                  </button>
               </div>
            )}
            
            {wiringMode === 'advanced' && (
              <div className="glass-card p-5 h-64 overflow-y-auto">'''

content = content.replace(inspector_search, mode_ui)

# Cap the first block
content = content.replace(
'''                  </div>
                )}
              </div>
            )}
          </div>

          <div className="glass-card p-5 flex-1 flex flex-col">''',
'''                  </div>
                )}
              </div>
            )}
          </div>
          )}

          {wiringMode === 'advanced' && (
          <div className="glass-card p-5 flex-1 flex flex-col">''')

# Cap the second block
content = content.replace(
'''              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );''',
'''              </div>
            )}
          </div>
          )}
        </div>

      </div>
    </div>
  );''')

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)
print("done")
