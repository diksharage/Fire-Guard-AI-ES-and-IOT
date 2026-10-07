const fs = require('fs');
let content = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');

const targetStr = `<text x="15" y="20" fill="#F5F5F5" fontSize="16" fontWeight="bold">+</text>`;
const replaceStr = `<text x="15" y="20" fill="#F5F5F5" fontSize="16" fontWeight="bold">+</text>
                <text x="30" y="85" fill={circuitReady && isRunning && riskLevel === 2 ? '#EF4444' : '#6B7280'} fontSize="12" fontWeight="bold" textAnchor="middle" className="pointer-events-none select-none">
                   {circuitReady && isRunning && riskLevel === 2 ? '🔊 BUZZER ACTIVE' : '🔇 BUZZER OFF'}
                </text>`;

content = content.replace(targetStr, replaceStr);

fs.writeFileSync('src/pages/VirtualCircuit.jsx', content);
