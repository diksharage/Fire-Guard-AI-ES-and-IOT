const fs = require('fs');
let content = fs.readFileSync('src/context/SimulationContext.jsx', 'utf8');

// Completely rip out any clearHistory definition block manually
content = content.replace(/const clearHistory = \(\) => \{\s*setSensorHistory\(\[\]\);\s*localStorage\.removeItem\("fireguard_history"\);\s*\};\n/g, '');
content = content.replace(/const clearHistory = \(\) => \{\s*setSensorHistory\(\[\]\);\s*localStorage\.removeItem\('fireguard_history'\);\s*\};\n/g, '');
content = content.replace(/clearHistory,\s*/g, '');

const returnRegex = /return \(\s*<SimulationContext\.Provider value=\{\{/g;
content = content.replace(returnRegex, 'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };\n\n  return (\n    <SimulationContext.Provider value={{ clearHistory, ');

fs.writeFileSync('src/context/SimulationContext.jsx', content);
