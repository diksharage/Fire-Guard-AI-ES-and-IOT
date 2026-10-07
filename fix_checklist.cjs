const fs = require('fs');
let content = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');

const oldChecklist = `<div className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-300 space-y-1 mb-2">
                    <div>✓ MQ-2 → A0</div>
                    <div>✓ DHT11 → D2</div>
                    <div>✓ Green LED → D5</div>
                    <div>✓ Yellow LED → D6</div>
                    <div>✓ Red LED → D7</div>
                    <div>✓ Buzzer → D4</div>
                  </div>`;
const newChecklist = `<div className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-300 space-y-1 mb-2">
                    <div>✓ MQ-2 → A0 (3 Wires)</div>
                    <div>✓ DHT11 → D2 (3 Wires)</div>
                    <div>✓ Green LED → D5 (3 Wires)</div>
                    <div>✓ Yellow LED → D6 (3 Wires)</div>
                    <div>✓ Red LED → D7 (3 Wires)</div>
                    <div>✓ Buzzer → D4 (2 Wires)</div>
                    <div className="text-green-500 font-bold mt-2">17/17 - CIRCUIT VALID</div>
                  </div>`;
content = content.replace(oldChecklist, newChecklist);

fs.writeFileSync('src/pages/VirtualCircuit.jsx', content);
