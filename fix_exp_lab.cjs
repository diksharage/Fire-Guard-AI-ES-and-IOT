const fs = require('fs');
let content = fs.readFileSync('src/pages/ExperimentLab.jsx', 'utf8');

const target = `const { 
    temperature, setTemperature,`;
    
const replacement = `const { 
    isSoundEnabled, setIsSoundEnabled,
    temperature, setTemperature,`;

content = content.replace(target, replacement);

fs.writeFileSync('src/pages/ExperimentLab.jsx', content);
