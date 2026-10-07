import codecs
import re

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx"
with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

# Update component coordinates to be on the breadboard
# Breadboard is at (100, 350)
coords = """
    const [components, setComponents] = useState({
      breadboard: { x: 100, y: 350 },
      esp: { x: 300, y: 50 },
      mq2: { x: 50, y: 50 },
      dht11: { x: 150, y: 50 },
      led_g: { x: 150, y: 400 },
      res1: { x: 130, y: 460 },
      led_y: { x: 250, y: 400 },
      res2: { x: 230, y: 460 },
      led_r: { x: 350, y: 400 },
      res3: { x: 330, y: 460 },
      buzzer: { x: 550, y: 370 }
    });
"""
content = re.sub(r'const \[components, setComponents\] = useState\(\{.*?\}\);', coords.strip(), content, flags=re.DOTALL)

# Update handleAutoBuild
auto_wires = """
  const handleAutoBuild = () => {
    const autoWires = [
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
    ];
    setWires(autoWires);
    setAutoBuilt(true);
    setValidation({ status: 'validated', missing: [], valid: true, correct: 17, total: 17 });
    setCircuitReady(true);
  };
"""
content = re.sub(r'const handleAutoBuild = \(\) => \{.*?\n  \};\n', auto_wires.strip() + "\n", content, flags=re.DOTALL)


# Let's add useEffect in VirtualCircuit.jsx to auto-validate whenever wires change
# Wait, validateCircuit checks wires. Let's make sure validateCircuit works properly and call it on wires change.
validate_eff = """
  // Auto-validate circuit whenever wires change
  useEffect(() => {
    let missing = [];
    let correctCount = 0;

    REQUIRED_CONNECTIONS.forEach(req => {
      const exists = wires.some(w => {
        const matchForward = (w.startComp === req.fromComp && w.startPin === req.fromPin && w.endComp === req.toComp && req.toPins.includes(w.endPin));
        const matchReverse = (w.endComp === req.fromComp && w.endPin === req.fromPin && w.startComp === req.toComp && req.toPins.includes(w.startPin));
        return matchForward || matchReverse;
      });
      if (exists) correctCount++;
      else missing.push(req.desc);
    });

    const isValid = missing.length === 0;
    setValidation({ status: 'validated', missing, correct: correctCount, total: REQUIRED_CONNECTIONS.length, valid: isValid });
    setCircuitReady(isValid);
    if (!isValid) {
       setIsRunning(false); // Disable simulation lock if broken
    }
  }, [wires, setValidation, setCircuitReady, setIsRunning]);
"""

# Let's see if there is an existing validateCircuit. We can just replace it.
content = re.sub(r'const validateCircuit = \(\) => \{.*?\n  \};\n', validate_eff.strip() + "\n", content, flags=re.DOTALL)

# Now, we also need to change the check in "Circuit Ready" checklist
checklist = """<div className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-300 space-y-1 mb-2">
                    <div>✓ MQ-2 → A0 (3 Wires)</div>
                    <div>✓ DHT11 → D2 (3 Wires)</div>
                    <div>✓ Green LED → D5 (3 Wires)</div>
                    <div>✓ Yellow LED → D6 (3 Wires)</div>
                    <div>✓ Red LED → D7 (3 Wires)</div>
                    <div>✓ Buzzer → D4 (2 Wires)</div>
                    <div className="text-green-500 font-bold mt-2">17/17 - CIRCUIT VALID</div>
                  </div>"""

content = re.sub(r'<div className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-300 space-y-1 mb-2">.*?</div>\n                  <button onClick=\{\(\) => navigate\(\'/lab\'\)\}', checklist + "\n                  <button onClick={() => navigate('/lab')}", content, flags=re.DOTALL)

# Update validation button since it is now auto-validating
# Instead of a validate button, we just show the validation status
# Replace `{wiringMode === 'advanced' && (<button onClick={validateCircuit}...> Validate Circuit </button>)}`
# with nothing or a status text. Let's just remove the button, because it's auto-validating!
content = re.sub(r'\{wiringMode === \'advanced\' && \(\s*<button onClick=\{validateCircuit\}.*?</button>\s*\)\}', '', content, flags=re.DOTALL)

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)
