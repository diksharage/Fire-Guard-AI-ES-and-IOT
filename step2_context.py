import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

context_path = os.path.join(DIR, "context", "SimulationContext.jsx")
with open(context_path, "r", encoding="utf-8") as f:
    content = f.read()

if "circuitWires" not in content:
    # Insert new state variables right after demoStage
    insert_idx = content.find("const [demoStage, setDemoStage] = useState(0);")
    if insert_idx != -1:
        insert_idx += len("const [demoStage, setDemoStage] = useState(0);")
        
        new_state = """
  const [circuitWires, setCircuitWires] = useState([]);
  const [circuitValidation, setCircuitValidation] = useState({ status: 'idle', missing: [], valid: false, correct: 0, total: 17 });
  const [circuitReady, setCircuitReady] = useState(false);
"""
        content = content[:insert_idx] + new_state + content[insert_idx:]

    # Update Provider value
    provider_idx = content.find("demoStage")
    if provider_idx != -1:
        content = content.replace("demoMode, setDemoMode, demoStage", 
                                  "demoMode, setDemoMode, demoStage, circuitWires, setCircuitWires, circuitValidation, setCircuitValidation, circuitReady, setCircuitReady")

    with open(context_path, "w", encoding="utf-8") as f:
        f.write(content)

print("SimulationContext.jsx updated successfully.")
