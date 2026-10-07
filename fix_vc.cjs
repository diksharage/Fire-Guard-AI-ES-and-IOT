const fs = require('fs');
let content = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');

const validateFnRegex = /const validateCircuit = \(\) => \{[\s\S]*?if \(isValid\) setCircuitReady\(true\);\s*\};/;
const newValidate = `
  useEffect(() => {
    const missing = [];
    let correctCount = 0;
    
    REQUIRED_CONNECTIONS.forEach(req => {
      const exists = wires.some(w => {
        const fwd = w.startComp === req.fromComp && w.startPin === req.fromPin && w.endComp === req.toComp && req.toPins.includes(w.endPin);
        const rev = w.endComp === req.fromComp && w.endPin === req.fromPin && w.startComp === req.toComp && req.toPins.includes(w.startPin);
        return fwd || rev;
      });
      if (exists) correctCount++;
      else missing.push(req.desc);
    });

    const isValid = missing.length === 0;
    setValidation({ status: 'validated', missing, correct: correctCount, total: REQUIRED_CONNECTIONS.length, valid: isValid });
    setCircuitReady(isValid);
    if (!isValid && isRunning) {
      setIsRunning(false);
    }
  }, [wires, setValidation, setCircuitReady, isRunning, setIsRunning]);
`;

content = content.replace(validateFnRegex, newValidate);

content = content.replace(/\{wiringMode === 'advanced' && \(\s*<button onClick=\{validateCircuit\}[\s\S]*?<\/button>\s*\)\}/, '');

const coordsRegex = /const \[components, setComponents\] = useState\(\{[\s\S]*?\}\);/;
const newCoords = `const [components, setComponents] = useState({
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
    });`;
content = content.replace(coordsRegex, newCoords);

fs.writeFileSync('src/pages/VirtualCircuit.jsx', content);
