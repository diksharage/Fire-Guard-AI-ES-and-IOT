import os
import re

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

circuit_path = os.path.join(DIR, "pages", "VirtualCircuit.jsx")
with open(circuit_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Context Destructuring
content = content.replace(
    "const { riskLevel, smoke, isRunning, setIsRunning } = useContext(SimulationContext);",
    "const { riskLevel, smoke, isRunning, setIsRunning, circuitWires: wires, setCircuitWires: setWires, circuitValidation: validation, setCircuitValidation: setValidation, circuitReady, setCircuitReady } = useContext(SimulationContext);"
)

# Remove local states for these
content = re.sub(r"const \[wires, setWires\] = useState\(\[\]\);\s*", "", content)
content = re.sub(r"const \[validation, setValidation\] = useState\([^)]+\);\s*", "", content)
content = re.sub(r"const \[circuitReady, setCircuitReady\] = useState\(false\);\s*", "", content)

# Export REQUIRED_CONNECTIONS so Guidelines can use it
content = content.replace("const REQUIRED_CONNECTIONS = [", "export const REQUIRED_CONNECTIONS = [")

with open(circuit_path, "w", encoding="utf-8") as f:
    f.write(content)

print("VirtualCircuit.jsx updated successfully.")
