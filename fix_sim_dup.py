import re

with open('src/context/SimulationContext.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all `const clearHistory = ...` lines
content = re.sub(r'const clearHistory = \(\) => \{.*?\};\n', '', content)
content = re.sub(r'clearHistory,\s*', '', content)

# Remove any duplicates of clearHistory that might span multiple lines if any
content = re.sub(r'const clearHistory = \(\) => \{\s*setSensorHistory\(\[\]\);\s*localStorage\.removeItem\([^)]+\);\s*\};\n', '', content)

# Add it once
content = content.replace(
    'return (\n    <SimulationContext.Provider value={{',
    'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };\n\n  return (\n    <SimulationContext.Provider value={{ clearHistory, '
)

with open('src/context/SimulationContext.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
