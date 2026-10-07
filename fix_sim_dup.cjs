const fs = require('fs');
let content = fs.readFileSync('src/context/SimulationContext.jsx', 'utf8');

content = content.replace(/const clearHistory = \(\) => \{[\s\S]*?\};\n/g, '');
content = content.replace(/clearHistory,/g, '');

const returnRegex = /return \(\s*<SimulationContext\.Provider value=\{\{/g;
content = content.replace(returnRegex, 'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };\n\n  return (\n    <SimulationContext.Provider value={{ clearHistory,');

fs.writeFileSync('src/context/SimulationContext.jsx', content);
