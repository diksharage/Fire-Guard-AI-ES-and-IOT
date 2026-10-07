const fs = require('fs');
let content = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');

const autoWiresStr = `const autoWires = [
      { id: 'w1', startComp: 'mq2', startPin: 'VCC', endComp: 'esp', endPin: '3V3_1', color: '#ef4444' },
      { id: 'w2', startComp: 'mq2', startPin: 'GND', endComp: 'esp', endPin: 'GND1', color: '#1f2937' },
      { id: 'w3', startComp: 'mq2', startPin: 'A0', endComp: 'esp', endPin: 'A0', color: '#3b82f6' },
      
      { id: 'w4', startComp: 'dht11', startPin: 'VCC', endComp: 'esp', endPin: '3V3_1', color: '#ef4444' },
      { id: 'w5', startComp: 'dht11', startPin: 'GND', endComp: 'esp', endPin: 'GND1', color: '#1f2937' },
      { id: 'w6', startComp: 'dht11', startPin: 'DATA', endComp: 'esp', endPin: 'D2', color: '#eab308' },
      
      { id: 'w7', startComp: 'res1', startPin: 'P1', endComp: 'esp', endPin: 'D5', color: '#22c55e' },
      { id: 'w8', startComp: 'res1', startPin: 'P2', endComp: 'led_g', endPin: 'A', color: '#22c55e' },
      { id: 'w9', startComp: 'led_g', startPin: 'K', endComp: 'esp', endPin: 'GND2', color: '#1f2937' },
      
      { id: 'w10', startComp: 'res2', startPin: 'P1', endComp: 'esp', endPin: 'D6', color: '#eab308' },
      { id: 'w11', startComp: 'res2', startPin: 'P2', endComp: 'led_y', endPin: 'A', color: '#eab308' },
      { id: 'w12', startComp: 'led_y', startPin: 'K', endComp: 'esp', endPin: 'GND2', color: '#1f2937' },
      
      { id: 'w13', startComp: 'res3', startPin: 'P1', endComp: 'esp', endPin: 'D7', color: '#ef4444' },
      { id: 'w14', startComp: 'res3', startPin: 'P2', endComp: 'led_r', endPin: 'A', color: '#ef4444' },
      { id: 'w15', startComp: 'led_r', startPin: 'K', endComp: 'esp', endPin: 'GND3', color: '#1f2937' },
      
      { id: 'w16', startComp: 'buzzer', startPin: 'POS', endComp: 'esp', endPin: 'D4', color: '#f97316' },
      { id: 'w17', startComp: 'buzzer', startPin: 'NEG', endComp: 'esp', endPin: 'GND4', color: '#1f2937' }
    ];`;

content = content.replace(/const autoWires = \[[\s\S]*?\];/, autoWiresStr);
content = content.replace(/setValidation\(\{ status: 'validated', missing: \[\], valid: true, correct: 14, total: 14 \}\);/, "");

fs.writeFileSync('src/pages/VirtualCircuit.jsx', content);
