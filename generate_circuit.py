import os

content = """import React, { useState, useContext, useRef, useEffect, useMemo } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Cpu, Wind, Thermometer, Info, Play, CheckCircle, AlertTriangle, XCircle, Trash2 } from 'lucide-react';

// Define components and their pins
const COMPONENT_DEF = {
  esp: {
    name: "ESP8266 NodeMCU",
    desc: "Microcontroller + Wi-Fi. Processes sensor data and sends to cloud.",
    width: 140, height: 260,
    pins: [
      { id: 'A0', label: 'A0', x: -10, y: 20, type: 'analog' },
      { id: 'GND1', label: 'GND', x: -10, y: 180, type: 'gnd' },
      { id: '3V3_1', label: '3V3', x: -10, y: 200, type: 'power' },
      { id: 'VIN', label: 'VIN', x: -10, y: 240, type: 'power' },
      { id: 'D0', label: 'D0', x: 150, y: 20, type: 'gpio' },
      { id: 'D1', label: 'D1', x: 150, y: 40, type: 'gpio' },
      { id: 'D2', label: 'D2', x: 150, y: 60, type: 'gpio' },
      { id: 'D3', label: 'D3', x: 150, y: 80, type: 'gpio' },
      { id: 'D4', label: 'D4', x: 150, y: 100, type: 'gpio' },
      { id: '3V3_2', label: '3V3', x: 150, y: 120, type: 'power' },
      { id: 'GND2', label: 'GND', x: 150, y: 140, type: 'gnd' },
      { id: 'D5', label: 'D5', x: 150, y: 160, type: 'gpio' },
      { id: 'D6', label: 'D6', x: 150, y: 180, type: 'gpio' },
      { id: 'D7', label: 'D7', x: 150, y: 200, type: 'gpio' },
      { id: 'D8', label: 'D8', x: 150, y: 220, type: 'gpio' },
      { id: 'GND3', label: 'GND', x: 150, y: 240, type: 'gnd' }
    ]
  },
  mq2: {
    name: "MQ-2 Gas Sensor",
    desc: "Detects smoke and combustible gases.",
    width: 60, height: 80,
    pins: [
      { id: 'VCC', label: 'VCC', x: 10, y: 90, type: 'power' },
      { id: 'GND', label: 'GND', x: 25, y: 90, type: 'gnd' },
      { id: 'D0', label: 'D0', x: 40, y: 90, type: 'gpio' },
      { id: 'A0', label: 'A0', x: 55, y: 90, type: 'analog' }
    ]
  },
  dht11: {
    name: "DHT11 Sensor",
    desc: "Temperature and humidity measurement.",
    width: 50, height: 70,
    pins: [
      { id: 'VCC', label: 'VCC', x: 10, y: 80, type: 'power' },
      { id: 'DATA', label: 'DATA', x: 25, y: 80, type: 'gpio' },
      { id: 'GND', label: 'GND', x: 40, y: 80, type: 'gnd' }
    ]
  },
  led_g: { name: "Green LED", desc: "Indicates NORMAL state.", width: 30, height: 60, pins: [{ id: 'A', label: 'Anode (+)', x: 10, y: 70, type: 'gpio' }, { id: 'K', label: 'Cathode (-)', x: 25, y: 70, type: 'gnd' }] },
  led_y: { name: "Yellow LED", desc: "Indicates WARNING state.", width: 30, height: 60, pins: [{ id: 'A', label: 'Anode (+)', x: 10, y: 70, type: 'gpio' }, { id: 'K', label: 'Cathode (-)', x: 25, y: 70, type: 'gnd' }] },
  led_r: { name: "Red LED", desc: "Indicates HIGH FIRE RISK.", width: 30, height: 60, pins: [{ id: 'A', label: 'Anode (+)', x: 10, y: 70, type: 'gpio' }, { id: 'K', label: 'Cathode (-)', x: 25, y: 70, type: 'gnd' }] },
  buzzer: { name: "Piezo Buzzer", desc: "Audible alarm.", width: 50, height: 50, pins: [{ id: 'POS', label: '+', x: 15, y: 60, type: 'gpio' }, { id: 'NEG', label: '-', x: 35, y: 60, type: 'gnd' }] }
};

const REQUIRED_CONNECTIONS = [
  { fromComp: 'mq2', fromPin: 'VCC', toComp: 'esp', toPins: ['3V3_1', '3V3_2', 'VIN'], desc: "MQ-2 VCC -> ESP8266 Power" },
  { fromComp: 'mq2', fromPin: 'GND', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "MQ-2 GND -> ESP8266 Ground" },
  { fromComp: 'mq2', fromPin: 'A0', toComp: 'esp', toPins: ['A0'], desc: "MQ-2 A0 -> ESP8266 A0" },
  { fromComp: 'dht11', fromPin: 'VCC', toComp: 'esp', toPins: ['3V3_1', '3V3_2', 'VIN'], desc: "DHT11 VCC -> ESP8266 Power" },
  { fromComp: 'dht11', fromPin: 'GND', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "DHT11 GND -> ESP8266 Ground" },
  { fromComp: 'dht11', fromPin: 'DATA', toComp: 'esp', toPins: ['D2'], desc: "DHT11 DATA -> ESP8266 D2" },
  { fromComp: 'led_g', fromPin: 'A', toComp: 'esp', toPins: ['D5'], desc: "Green LED Anode -> ESP8266 D5" },
  { fromComp: 'led_g', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "Green LED Cathode -> ESP8266 Ground" },
  { fromComp: 'led_y', fromPin: 'A', toComp: 'esp', toPins: ['D6'], desc: "Yellow LED Anode -> ESP8266 D6" },
  { fromComp: 'led_y', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "Yellow LED Cathode -> ESP8266 Ground" },
  { fromComp: 'led_r', fromPin: 'A', toComp: 'esp', toPins: ['D7'], desc: "Red LED Anode -> ESP8266 D7" },
  { fromComp: 'led_r', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "Red LED Cathode -> ESP8266 Ground" },
  { fromComp: 'buzzer', fromPin: 'POS', toComp: 'esp', toPins: ['D4'], desc: "Buzzer + -> ESP8266 D4" },
  { fromComp: 'buzzer', fromPin: 'NEG', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3'], desc: "Buzzer - -> ESP8266 Ground" },
];

const VirtualCircuit = () => {
  const { riskLevel, temperature, smoke, isRunning, setIsRunning } = useContext(SimulationContext);
  
  const [components, setComponents] = useState({
    esp: { x: 350, y: 150 },
    mq2: { x: 50, y: 100 },
    dht11: { x: 50, y: 300 },
    led_g: { x: 700, y: 50 },
    led_y: { x: 700, y: 150 },
    led_r: { x: 700, y: 250 },
    buzzer: { x: 700, y: 350 }
  });
  
  const [wires, setWires] = useState([]);
  const [dragging, setDragging] = useState(null);
  const [wiring, setWiring] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [selectedComp, setSelectedComp] = useState(null);
  
  const [validation, setValidation] = useState({ status: 'idle', missing: [], incorrect: [], valid: false });
  const [circuitReady, setCircuitReady] = useState(false);
  
  const svgRef = useRef(null);

  // Stop simulation initially until circuit is built
  useEffect(() => {
    if (!circuitReady && isRunning) {
      setIsRunning(false);
    }
  }, [circuitReady, isRunning, setIsRunning]);

  const getRelativeCoordinates = (e) => {
    if (!svgRef.current) return { x: 0, y: 0 };
    const rect = svgRef.current.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  };

  const handleMouseDown = (e, compId) => {
    if (wiring) return; // Don't drag while wiring
    const pos = getRelativeCoordinates(e);
    setDragging({
      comp: compId,
      offsetX: pos.x - components[compId].x,
      offsetY: pos.y - components[compId].y
    });
    setSelectedComp(compId);
  };

  const handleMouseMove = (e) => {
    const pos = getRelativeCoordinates(e);
    setMousePos(pos);
    
    if (dragging) {
      setComponents(prev => ({
        ...prev,
        [dragging.comp]: {
          x: pos.x - dragging.offsetX,
          y: pos.y - dragging.offsetY
        }
      }));
    }
  };

  const handleMouseUp = () => {
    setDragging(null);
  };

  const handlePinClick = (e, compId, pinId) => {
    e.stopPropagation();
    
    if (!wiring) {
      // Start wiring
      setWiring({ comp: compId, pin: pinId });
    } else {
      // Finish wiring
      if (wiring.comp === compId && wiring.pin === pinId) {
        // Cancel if clicking same pin
        setWiring(null);
        return;
      }
      
      // Determine wire color
      let color = '#9ca3af'; // gray default
      const pinType = COMPONENT_DEF[compId].pins.find(p => p.id === pinId)?.type;
      const startPinType = COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin)?.type;
      
      if (pinType === 'power' || startPinType === 'power') color = '#ef4444'; // Red
      else if (pinType === 'gnd' || startPinType === 'gnd') color = '#111827'; // Black
      else if (pinType === 'analog' || startPinType === 'analog') color = '#eab308'; // Yellow
      else if (pinType === 'gpio' || startPinType === 'gpio') color = '#3b82f6'; // Blue
      
      setWires(prev => [...prev, {
        id: Date.now().toString(),
        startComp: wiring.comp,
        startPin: wiring.pin,
        endComp: compId,
        endPin: pinId,
        color
      }]);
      
      setWiring(null);
      setValidation({ status: 'idle', missing: [], incorrect: [], valid: false });
      setCircuitReady(false);
    }
  };

  const removeWire = (id, e) => {
    e.stopPropagation();
    setWires(prev => prev.filter(w => w.id !== id));
    setValidation({ status: 'idle', missing: [], incorrect: [], valid: false });
    setCircuitReady(false);
  };

  const validateCircuit = () => {
    const missing = [];
    let correctCount = 0;
    
    // Check required connections
    REQUIRED_CONNECTIONS.forEach(req => {
      // Check if a wire exists between req.fromComp(req.fromPin) and req.toComp(req.toPins[])
      const exists = wires.some(w => {
        const matchForward = w.startComp === req.fromComp && w.startPin === req.fromPin && w.endComp === req.toComp && req.toPins.includes(w.endPin);
        const matchReverse = w.endComp === req.fromComp && w.endPin === req.fromPin && w.startComp === req.toComp && req.toPins.includes(w.startPin);
        return matchForward || matchReverse;
      });
      
      if (exists) {
        correctCount++;
      } else {
        missing.push(req.desc);
      }
    });

    const isValid = missing.length === 0;
    setValidation({
      status: 'validated',
      missing,
      correct: correctCount,
      total: REQUIRED_CONNECTIONS.length,
      valid: isValid
    });
    
    if (isValid) {
      setCircuitReady(true);
    }
  };

  // Helper to render pins
  const renderPins = (compId, def) => {
    return def.pins.map(pin => {
      const isWiring = wiring?.comp === compId && wiring?.pin === pin.id;
      return (
        <g key={pin.id} transform={`translate(${pin.x}, ${pin.y})`} onClick={(e) => handlePinClick(e, compId, pin.id)} className="cursor-pointer group">
          <circle cx="0" cy="0" r="6" fill="#1C222D" stroke={isWiring ? "#F59E0B" : "#F5F5F5"} strokeWidth="2" />
          <circle cx="0" cy="0" r="3" fill={isWiring ? "#F59E0B" : "#9CA3AF"} />
          
          {/* Tooltip on hover */}
          <rect x="-10" y="-25" width="40" height="15" fill="#080B12" className="hidden group-hover:block" rx="2" />
          <text x="10" y="-14" fill="#F5F5F5" fontSize="10" textAnchor="middle" className="hidden group-hover:block">{pin.label}</text>
        </g>
      );
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Interactive Circuit Laboratory</h1>
          <p className="text-slate-400">Connect the components correctly to enable the simulation.</p>
        </div>
        <div className="flex gap-3">
          <button onClick={validateCircuit} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg border border-slate-700 transition">
            <CheckCircle size={18} /> Validate Circuit
          </button>
          <button 
            onClick={() => circuitReady && setIsRunning(true)} 
            disabled={!circuitReady || isRunning}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition ${circuitReady ? (isRunning ? 'bg-green-900/50 text-green-500 border border-green-900' : 'bg-primary text-white hover:bg-primary-bright') : 'bg-slate-800 text-slate-500 cursor-not-allowed'}`}
          >
            <Play size={18} /> {isRunning ? 'Running' : 'Run Simulation'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Main Workspace */}
        <div className="lg:col-span-3 glass-card p-1 min-h-[600px] bg-[#080B12] relative overflow-hidden" 
             onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}>
          
          <svg ref={svgRef} className="w-full h-full min-h-[600px]" onClick={() => { if(wiring) setWiring(null); setSelectedComp(null); }}>
            
            {/* Grid Pattern */}
            <defs>
              <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1" fill="#2A3342" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />

            {/* Breadboard Visual (Background Decor) */}
            <g transform="translate(150, 450)">
              <rect width="600" height="120" rx="10" fill="#E5E7EB" stroke="#9CA3AF" strokeWidth="2" />
              <rect width="600" height="2" y="20" fill="#EF4444" opacity="0.5" />
              <rect width="600" height="2" y="100" fill="#3B82F6" opacity="0.5" />
              <text x="10" y="15" fontSize="10" fill="#EF4444" fontWeight="bold">+</text>
              <text x="10" y="115" fontSize="10" fill="#3B82F6" fontWeight="bold">-</text>
              <text x="250" y="65" fontSize="24" fill="#9CA3AF" opacity="0.3" fontWeight="bold" letterSpacing="5">BREADBOARD</text>
            </g>

            {/* Render Wires */}
            {wires.map((wire) => {
              const startComp = components[wire.startComp];
              const startPinDef = COMPONENT_DEF[wire.startComp].pins.find(p => p.id === wire.startPin);
              const endComp = components[wire.endComp];
              const endPinDef = COMPONENT_DEF[wire.endComp].pins.find(p => p.id === wire.endPin);
              
              if(!startComp || !endComp || !startPinDef || !endPinDef) return null;

              const x1 = startComp.x + startPinDef.x;
              const y1 = startComp.y + startPinDef.y;
              const x2 = endComp.x + endPinDef.x;
              const y2 = endComp.y + endPinDef.y;
              
              // bezier curve for realistic wire
              const dx = Math.abs(x2 - x1);
              const path = `M ${x1} ${y1} C ${x1 + dx/2} ${y1}, ${x2 - dx/2} ${y2}, ${x2} ${y2}`;

              const isSelected = selectedComp === wire.startComp || selectedComp === wire.endComp;
              const opacity = (selectedComp && !isSelected) ? 0.2 : 1;

              return (
                <g key={wire.id} opacity={opacity}>
                  <path d={path} stroke={wire.color} strokeWidth="5" fill="none" className="drop-shadow-md cursor-pointer hover:stroke-red-500" onClick={(e) => removeWire(wire.id, e)} />
                  {/* Highlight core */}
                  <path d={path} stroke="#ffffff" strokeWidth="1" fill="none" opacity="0.3" className="pointer-events-none" />
                </g>
              );
            })}

            {/* Active Wiring line */}
            {wiring && (
              <path 
                d={`M ${components[wiring.comp].x + COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin).x} ${components[wiring.comp].y + COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin).y} L ${mousePos.x} ${mousePos.y}`} 
                stroke="#F59E0B" strokeWidth="3" fill="none" strokeDasharray="5,5" className="animate-pulse pointer-events-none" 
              />
            )}

            {/* Render Components */}
            {/* ESP8266 */}
            <g transform={`translate(${components.esp.x}, ${components.esp.y})`} onMouseDown={(e) => handleMouseDown(e, 'esp')} className="cursor-move">
              <rect width="140" height="260" rx="8" fill="#1C222D" stroke={selectedComp === 'esp' ? '#F59E0B' : '#2A3342'} strokeWidth="3" className="drop-shadow-xl" />
              <rect x="35" y="10" width="70" height="30" fill="#080B12" rx="4" /> {/* USB */}
              <rect x="25" y="60" width="90" height="120" fill="#111827" stroke="#2A3342" /> {/* Shield */}
              <text x="70" y="120" fill="#9CA3AF" fontSize="12" textAnchor="middle" transform="rotate(-90 70 120)">ESP8266MOD</text>
              <circle cx="115" cy="165" r="4" fill={circuitReady && isRunning ? "#3B82F6" : "#2A3342"} className={circuitReady && isRunning ? "animate-pulse" : ""} />
              {/* Pin Labels */}
              {COMPONENT_DEF.esp.pins.map(p => <text key={p.id} x={p.x < 70 ? p.x + 25 : p.x - 25} y={p.y + 4} fill="#9CA3AF" fontSize="10" textAnchor={p.x < 70 ? 'start' : 'end'} className="pointer-events-none font-mono">{p.label}</text>)}
              {renderPins('esp', COMPONENT_DEF.esp)}
            </g>

            {/* MQ-2 */}
            <g transform={`translate(${components.mq2.x}, ${components.mq2.y})`} onMouseDown={(e) => handleMouseDown(e, 'mq2')} className="cursor-move">
              <rect width="70" height="80" rx="4" fill="#7F1D1D" stroke={selectedComp === 'mq2' ? '#F59E0B' : '#450A0A'} strokeWidth="2" className="drop-shadow-lg" />
              <circle cx="35" cy="35" r="25" fill="#9CA3AF" stroke="#E5E7EB" strokeWidth="4" />
              <circle cx="35" cy="35" r="15" fill="#4B5563" />
              <text x="35" y="38" fill="#111827" fontSize="10" textAnchor="middle" fontWeight="bold">MQ-2</text>
              {circuitReady && isRunning && smoke > 300 && <circle cx="35" cy="35" r="30" fill="#9CA3AF" opacity="0.3" className="animate-ping pointer-events-none" />}
              {COMPONENT_DEF.mq2.pins.map(p => <text key={p.id} x={p.x} y={p.y - 15} fill="#FCA5A5" fontSize="8" textAnchor="middle" className="pointer-events-none font-mono">{p.label}</text>)}
              {renderPins('mq2', COMPONENT_DEF.mq2)}
            </g>

            {/* DHT11 */}
            <g transform={`translate(${components.dht11.x}, ${components.dht11.y})`} onMouseDown={(e) => handleMouseDown(e, 'dht11')} className="cursor-move">
              <rect width="50" height="70" rx="2" fill="#1E3A8A" stroke={selectedComp === 'dht11' ? '#F59E0B' : '#172554'} strokeWidth="2" className="drop-shadow-lg" />
              <rect x="5" y="5" width="40" height="50" fill="#2563EB" />
              <line x1="10" y1="15" x2="40" y2="15" stroke="#1E40AF" strokeWidth="2" />
              <line x1="10" y1="25" x2="40" y2="25" stroke="#1E40AF" strokeWidth="2" />
              <line x1="10" y1="35" x2="40" y2="35" stroke="#1E40AF" strokeWidth="2" />
              <text x="25" y="50" fill="#BFDBFE" fontSize="10" textAnchor="middle" fontWeight="bold">DHT11</text>
              {COMPONENT_DEF.dht11.pins.map(p => <text key={p.id} x={p.x} y={p.y - 12} fill="#93C5FD" fontSize="8" textAnchor="middle" className="pointer-events-none font-mono">{p.label}</text>)}
              {renderPins('dht11', COMPONENT_DEF.dht11)}
            </g>

            {/* Green LED */}
            <g transform={`translate(${components.led_g.x}, ${components.led_g.y})`} onMouseDown={(e) => handleMouseDown(e, 'led_g')} className="cursor-move">
              <rect width="35" height="50" fill="transparent" />
              <path d="M 10 30 L 10 70 M 25 30 L 25 70" stroke="#9CA3AF" strokeWidth="3" />
              <rect x="7" y="45" width="6" height="12" fill="#FCD34D" stroke="#D97706" /> {/* Resistor on Anode */}
              <circle cx="17.5" cy="15" r="15" fill={circuitReady && isRunning && riskLevel === 0 ? "#22C55E" : "#064E3B"} stroke="#14532D" strokeWidth="2" className={circuitReady && isRunning && riskLevel === 0 ? "drop-shadow-[0_0_15px_rgba(34,197,94,0.8)]" : ""} />
              <path d="M 5 25 Q 17.5 15 30 25" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.3" />
              {renderPins('led_g', COMPONENT_DEF.led_g)}
            </g>

            {/* Yellow LED */}
            <g transform={`translate(${components.led_y.x}, ${components.led_y.y})`} onMouseDown={(e) => handleMouseDown(e, 'led_y')} className="cursor-move">
              <rect width="35" height="50" fill="transparent" />
              <path d="M 10 30 L 10 70 M 25 30 L 25 70" stroke="#9CA3AF" strokeWidth="3" />
              <rect x="7" y="45" width="6" height="12" fill="#FCD34D" stroke="#D97706" />
              <circle cx="17.5" cy="15" r="15" fill={circuitReady && isRunning && riskLevel === 1 ? "#F59E0B" : "#78350F"} stroke="#451A03" strokeWidth="2" className={circuitReady && isRunning && riskLevel === 1 ? "drop-shadow-[0_0_15px_rgba(245,158,11,0.8)] animate-pulse" : ""} />
              <path d="M 5 25 Q 17.5 15 30 25" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.3" />
              {renderPins('led_y', COMPONENT_DEF.led_y)}
            </g>

            {/* Red LED */}
            <g transform={`translate(${components.led_r.x}, ${components.led_r.y})`} onMouseDown={(e) => handleMouseDown(e, 'led_r')} className="cursor-move">
              <rect width="35" height="50" fill="transparent" />
              <path d="M 10 30 L 10 70 M 25 30 L 25 70" stroke="#9CA3AF" strokeWidth="3" />
              <rect x="7" y="45" width="6" height="12" fill="#FCD34D" stroke="#D97706" />
              <circle cx="17.5" cy="15" r="15" fill={circuitReady && isRunning && riskLevel === 2 ? "#EF4444" : "#7F1D1D"} stroke="#450A0A" strokeWidth="2" className={circuitReady && isRunning && riskLevel === 2 ? "drop-shadow-[0_0_15px_rgba(239,68,68,0.8)] animate-pulse" : ""} />
              <path d="M 5 25 Q 17.5 15 30 25" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.3" />
              {renderPins('led_r', COMPONENT_DEF.led_r)}
            </g>

            {/* Buzzer */}
            <g transform={`translate(${components.buzzer.x}, ${components.buzzer.y})`} onMouseDown={(e) => handleMouseDown(e, 'buzzer')} className="cursor-move">
              <rect width="50" height="50" fill="transparent" />
              <circle cx="25" cy="25" r="25" fill="#111827" stroke={selectedComp === 'buzzer' ? '#F59E0B' : '#374151'} strokeWidth="3" className="drop-shadow-xl" />
              <circle cx="25" cy="25" r="15" fill="#080B12" />
              {circuitReady && isRunning && riskLevel === 2 && <circle cx="25" cy="25" r="35" stroke="#EF4444" strokeWidth="2" fill="none" className="animate-ping pointer-events-none" />}
              <path d="M 15 45 L 15 60 M 35 45 L 35 60" stroke="#9CA3AF" strokeWidth="3" />
              <text x="15" y="15" fill="#F5F5F5" fontSize="14" fontWeight="bold">+</text>
              {renderPins('buzzer', COMPONENT_DEF.buzzer)}
            </g>

          </svg>
          
          {/* Instructions overlay */}
          <div className="absolute top-4 left-4 bg-slate-900/80 p-3 rounded border border-slate-700 pointer-events-none">
            <h4 className="text-primary font-bold text-sm mb-1">Wiring Instructions</h4>
            <p className="text-xs text-slate-300">1. Drag components to arrange.</p>
            <p className="text-xs text-slate-300">2. Click a pin to start a wire.</p>
            <p className="text-xs text-slate-300">3. Click destination pin to connect.</p>
            <p className="text-xs text-slate-300">4. Click a wire to remove it.</p>
          </div>
        </div>

        {/* Sidebar Inspector & Validation */}
        <div className="flex flex-col gap-6">
          
          <div className="glass-card p-5 h-64 overflow-y-auto">
            <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2"><CheckCircle size={18} className="text-primary"/> Validation</h3>
            
            {validation.status === 'idle' && (
              <p className="text-sm text-slate-400">Click "Validate Circuit" to check your connections.</p>
            )}
            
            {validation.status === 'validated' && (
              <div>
                <div className="text-2xl font-bold text-white mb-2">{validation.correct} / {validation.total}</div>
                {validation.valid ? (
                  <div className="bg-green-900/30 text-green-400 p-3 rounded-lg border border-green-800 text-sm flex gap-2 items-start">
                    <CheckCircle size={16} className="mt-0.5 shrink-0" />
                    <div>All required connections complete! You can now run the simulation.</div>
                  </div>
                ) : (
                  <div className="bg-red-900/20 p-3 rounded-lg border border-red-800/50 text-sm">
                    <div className="text-red-400 font-bold mb-2 flex items-center gap-1"><AlertTriangle size={16}/> Missing Connections:</div>
                    <ul className="list-disc pl-4 text-slate-300 text-xs space-y-1">
                      {validation.missing.map((msg, i) => <li key={i}>{msg}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="glass-card p-5 flex-1 flex flex-col">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Info size={18} className="text-primary"/> Inspector
            </h3>
            
            {selectedComp ? (
              <div className="flex-1 flex flex-col">
                <h4 className="text-primary font-bold text-xl mb-1">{COMPONENT_DEF[selectedComp].name}</h4>
                <p className="text-sm text-slate-300 mb-4">{COMPONENT_DEF[selectedComp].desc}</p>
                
                <h5 className="font-semibold text-slate-200 text-xs uppercase tracking-wider mb-2">Connected Pins:</h5>
                <div className="bg-slate-900/50 rounded p-2 text-xs font-mono space-y-1 border border-slate-700 flex-1 overflow-y-auto">
                  {wires.filter(w => w.startComp === selectedComp || w.endComp === selectedComp).length === 0 && (
                    <span className="text-slate-500">No connections yet.</span>
                  )}
                  {wires.map(w => {
                    if(w.startComp === selectedComp) {
                      return <div key={w.id} className="text-slate-300">[{w.startPin}] → {COMPONENT_DEF[w.endComp].name} [{w.endPin}]</div>
                    } else if (w.endComp === selectedComp) {
                      return <div key={w.id} className="text-slate-300">[{w.endPin}] ← {COMPONENT_DEF[w.startComp].name} [{w.startPin}]</div>
                    }
                    return null;
                  })}
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-center">
                <Cpu size={48} className="mb-4 opacity-30" />
                <p className="text-sm">Select a component on the workbench to inspect its properties and wiring.</p>
              </div>
            )}
          </div>
          
        </div>

      </div>
    </div>
  );
};
export default VirtualCircuit;
"""

with open(r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Generated new VirtualCircuit.jsx")
