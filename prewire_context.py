import codecs

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\context\SimulationContext.jsx"
with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

initial_wires = """[
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
  ]"""

content = content.replace("const [circuitWires, setCircuitWires] = useState([]);", 
                          f"const [circuitWires, setCircuitWires] = useState({initial_wires});")

content = content.replace("const [circuitValidation, setCircuitValidation] = useState({ status: 'idle', missing: [], valid: false, correct: 0, total: 17 });", 
                          "const [circuitValidation, setCircuitValidation] = useState({ status: 'validated', missing: [], valid: true, correct: 14, total: 14 });")

content = content.replace("const [circuitReady, setCircuitReady] = useState(false);", 
                          "const [circuitReady, setCircuitReady] = useState(true);")

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)

print("SimulationContext initialized with pre-wired circuit.")
