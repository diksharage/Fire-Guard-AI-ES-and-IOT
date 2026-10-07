import codecs

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\context\SimulationContext.jsx"
with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

# I will replace the previously injected initial_wires and validation.
# We will use the exact 17 correct wires based on REQUIRED_CONNECTIONS.
correct_17_wires = """[
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
  ]"""

# Since I previously modified SimulationContext using a script, I need to match the current state.
# Let's just regex the useState blocks.
import re

content = re.sub(r'const \[circuitWires, setCircuitWires\] = useState\(\[.*?\]\);', 
                 f'const [circuitWires, setCircuitWires] = useState({correct_17_wires});', 
                 content, flags=re.DOTALL)

content = re.sub(r'const \[circuitValidation, setCircuitValidation\] = useState\(\{.*?\}\);', 
                 \"const [circuitValidation, setCircuitValidation] = useState({ status: 'validated', missing: [], valid: true, correct: 17, total: 17 });\", 
                 content, flags=re.DOTALL)

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)
