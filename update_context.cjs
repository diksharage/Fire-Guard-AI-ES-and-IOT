const fs = require('fs');
let content = fs.readFileSync('src/context/SimulationContext.jsx', 'utf8');

const newStates = `
  // App States
  const [isRunning, setIsRunning] = useState(false);
  const [isSoundEnabled, setIsSoundEnabled] = useState(true);
  
  // Notification State
  const [notifications, setNotifications] = useState([]);
  
  const addNotification = (title, message, type) => {
    setNotifications(prev => [{
      id: Date.now().toString() + Math.random().toString(),
      type,
      title,
      message,
      timestamp: new Date(),
      read: false
    }, ...prev]);
  };
  
  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({...n, read: true})));
  };
`;
content = content.replace('  // App States\n  const [isRunning, setIsRunning] = useState(false);', newStates);

const providerReturn = 'return (\n    <SimulationContext.Provider value={{';
const audioLogic = `
  // Buzzer Audio Setup
  const audioCtxRef = React.useRef(null);
  const oscillatorRef = React.useRef(null);
  const gainNodeRef = React.useRef(null);
  const beepIntervalRef = React.useRef(null);

  useEffect(() => {
    if (beepIntervalRef.current) {
      clearInterval(beepIntervalRef.current);
      beepIntervalRef.current = null;
    }
    
    if (buzzerStatus && isSoundEnabled) {
      if (!audioCtxRef.current) {
        audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
      }
      
      if (audioCtxRef.current.state === 'suspended') {
        audioCtxRef.current.resume();
      }

      if (!oscillatorRef.current) {
        const ctx = audioCtxRef.current;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'square';
        osc.frequency.value = 750;
        gain.gain.value = 0;
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        
        oscillatorRef.current = osc;
        gainNodeRef.current = gain;
      }
      
      let isOn = false;
      beepIntervalRef.current = setInterval(() => {
        isOn = !isOn;
        if (gainNodeRef.current && audioCtxRef.current) {
          gainNodeRef.current.gain.setTargetAtTime(isOn ? 0.1 : 0, audioCtxRef.current.currentTime, 0.015);
        }
      }, 300);
      
    } else {
      if (gainNodeRef.current && audioCtxRef.current) {
         gainNodeRef.current.gain.setTargetAtTime(0, audioCtxRef.current.currentTime || 0, 0.015);
      }
    }
    
    return () => {
      if (beepIntervalRef.current) {
        clearInterval(beepIntervalRef.current);
        beepIntervalRef.current = null;
      }
    };
  }, [buzzerStatus, isSoundEnabled]);

  // Notification Generator
  const prevRiskRef = React.useRef(riskLevel);
  const prevIsRunningRef = React.useRef(isRunning);
  const prevCircuitValidRef = React.useRef(circuitValidation.valid);

  useEffect(() => {
    if (prevRiskRef.current !== riskLevel) {
      if (riskLevel === 1 && prevRiskRef.current === 0) {
        addNotification("WARNING", "Environmental conditions require attention.", "warning");
      } else if (riskLevel === 2 && prevRiskRef.current !== 2) {
        addNotification("HIGH FIRE RISK", "Immediate virtual alert triggered.", "danger");
      }
      prevRiskRef.current = riskLevel;
    }

    if (prevIsRunningRef.current !== isRunning) {
      if (isRunning) {
        addNotification("SYSTEM", "Experiment started — monitoring active.", "system");
        if (audioCtxRef.current && audioCtxRef.current.state === 'suspended') {
           audioCtxRef.current.resume();
        }
      }
      prevIsRunningRef.current = isRunning;
    }

    if (prevCircuitValidRef.current !== circuitValidation.valid) {
      if (circuitValidation.valid) {
        addNotification("SYSTEM", "Circuit validated successfully.", "system");
      } else {
        addNotification("SYSTEM", "Circuit validation incomplete.", "warning");
      }
      prevCircuitValidRef.current = circuitValidation.valid;
    }
  }, [riskLevel, isRunning, circuitValidation.valid]);

  return (
    <SimulationContext.Provider value={{
      notifications, addNotification, markAllRead,
      isSoundEnabled, setIsSoundEnabled,
`;
content = content.replace(providerReturn, audioLogic);

fs.writeFileSync('src/context/SimulationContext.jsx', content);
