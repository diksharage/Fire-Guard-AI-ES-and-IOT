import React, { useState, useContext, useRef, useEffect } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Cpu, Info, Play, CheckCircle, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

// Pin definitions and coordinates relative to component top-left
const COMPONENT_DEF = {
  esp: {
    name: "ESP8266 NodeMCU",
    desc: "Microcontroller + Wi-Fi. Processes sensor data.",
    width: 200, height: 260,
    pins: [
      { id: 'A0', label: 'A0', x: 25, y: 35, type: 'analog' },
      { id: 'RSV1', label: 'RSV', x: 25, y: 50, type: 'gpio' },
      { id: 'RSV2', label: 'RSV', x: 25, y: 65, type: 'gpio' },
      { id: 'SD3', label: 'SD3', x: 25, y: 80, type: 'gpio' },
      { id: 'SD2', label: 'SD2', x: 25, y: 95, type: 'gpio' },
      { id: 'SD1', label: 'SD1', x: 25, y: 110, type: 'gpio' },
      { id: 'CMD', label: 'CMD', x: 25, y: 125, type: 'gpio' },
      { id: 'SD0', label: 'SD0', x: 25, y: 140, type: 'gpio' },
      { id: 'CLK', label: 'CLK', x: 25, y: 155, type: 'gpio' },
      { id: 'GND1', label: 'GND', x: 25, y: 170, type: 'gnd' },
      { id: '3V3_1', label: '3V3', x: 25, y: 185, type: 'power' },
      { id: 'EN', label: 'EN', x: 25, y: 200, type: 'gpio' },
      { id: 'RST', label: 'RST', x: 25, y: 215, type: 'gpio' },
      { id: 'GND2', label: 'GND', x: 25, y: 230, type: 'gnd' },
      { id: 'VIN', label: 'VIN', x: 25, y: 245, type: 'power' },

      { id: 'D0', label: 'D0', x: 175, y: 35, type: 'gpio' },
      { id: 'D1', label: 'D1', x: 175, y: 50, type: 'gpio' },
      { id: 'D2', label: 'D2', x: 175, y: 65, type: 'gpio' },
      { id: 'D3', label: 'D3', x: 175, y: 80, type: 'gpio' },
      { id: 'D4', label: 'D4', x: 175, y: 95, type: 'gpio' },
      { id: '3V3_2', label: '3V3', x: 175, y: 110, type: 'power' },
      { id: 'GND3', label: 'GND', x: 175, y: 125, type: 'gnd' },
      { id: 'D5', label: 'D5', x: 175, y: 140, type: 'gpio' },
      { id: 'D6', label: 'D6', x: 175, y: 155, type: 'gpio' },
      { id: 'D7', label: 'D7', x: 175, y: 170, type: 'gpio' },
      { id: 'D8', label: 'D8', x: 175, y: 185, type: 'gpio' },
      { id: 'RX', label: 'RX', x: 175, y: 200, type: 'gpio' },
      { id: 'TX', label: 'TX', x: 175, y: 215, type: 'gpio' },
      { id: 'GND4', label: 'GND', x: 175, y: 230, type: 'gnd' },
      { id: '3V3_3', label: '3V3', x: 175, y: 245, type: 'power' }
    ]
  },
  breadboard: {
    name: "Solderless Breadboard",
    desc: "Provides connection points for components and power rails.",
    width: 600, height: 200,
    pins: [
      { id: 'RAIL_V1', label: '5V/3.3V', x: 30, y: 20, type: 'power' },
      { id: 'RAIL_G1', label: 'GND', x: 30, y: 40, type: 'gnd' },
      { id: 'RAIL_V2', label: '5V/3.3V', x: 30, y: 180, type: 'power' },
      { id: 'RAIL_G2', label: 'GND', x: 30, y: 160, type: 'gnd' },
    ]
  },
  mq2: {
    name: "MQ-2 Sensor",
    desc: "Detects smoke and gas.",
    width: 80, height: 100,
    pins: [
      { id: 'VCC', label: 'VCC', x: 20, y: 95, type: 'power' },
      { id: 'GND', label: 'GND', x: 33, y: 95, type: 'gnd' },
      { id: 'D0', label: 'D0', x: 46, y: 95, type: 'gpio' },
      { id: 'A0', label: 'A0', x: 60, y: 95, type: 'analog' }
    ]
  },
  dht11: {
    name: "DHT11 Sensor",
    desc: "Temperature & Humidity.",
    width: 60, height: 80,
    pins: [
      { id: 'VCC', label: 'VCC', x: 15, y: 75, type: 'power' },
      { id: 'DATA', label: 'DATA', x: 30, y: 75, type: 'gpio' },
      { id: 'GND', label: 'GND', x: 45, y: 75, type: 'gnd' }
    ]
  },
  led_g: { name: "Green LED", desc: "NORMAL indicator.", width: 30, height: 70, pins: [{ id: 'A', label: '+', x: 10, y: 65, type: 'gpio' }, { id: 'K', label: '-', x: 20, y: 65, type: 'gnd' }] },
  led_y: { name: "Yellow LED", desc: "WARNING indicator.", width: 30, height: 70, pins: [{ id: 'A', label: '+', x: 10, y: 65, type: 'gpio' }, { id: 'K', label: '-', x: 20, y: 65, type: 'gnd' }] },
  led_r: { name: "Red LED", desc: "HIGH RISK indicator.", width: 30, height: 70, pins: [{ id: 'A', label: '+', x: 10, y: 65, type: 'gpio' }, { id: 'K', label: '-', x: 20, y: 65, type: 'gnd' }] },
  buzzer: { name: "Piezo Buzzer", desc: "Audible alarm.", width: 60, height: 60, pins: [{ id: 'POS', label: '+', x: 20, y: 55, type: 'gpio' }, { id: 'NEG', label: '-', x: 40, y: 55, type: 'gnd' }] },
  res1: { name: "220Î© Resistor", desc: "Current limiting for Green LED.", width: 80, height: 20, pins: [{ id: 'P1', label: '1', x: 5, y: 10, type: 'gpio' }, { id: 'P2', label: '2', x: 75, y: 10, type: 'gpio' }] },
  res2: { name: "220Î© Resistor", desc: "Current limiting for Yellow LED.", width: 80, height: 20, pins: [{ id: 'P1', label: '1', x: 5, y: 10, type: 'gpio' }, { id: 'P2', label: '2', x: 75, y: 10, type: 'gpio' }] },
  res3: { name: "220Î© Resistor", desc: "Current limiting for Red LED.", width: 80, height: 20, pins: [{ id: 'P1', label: '1', x: 5, y: 10, type: 'gpio' }, { id: 'P2', label: '2', x: 75, y: 10, type: 'gpio' }] }
};

export const REQUIRED_CONNECTIONS = [
  { fromComp: 'mq2', fromPin: 'VCC', toComp: 'esp', toPins: ['3V3_1', '3V3_2', '3V3_3', 'VIN'], desc: "MQ-2 VCC â†’ ESP8266 3V3/VIN" },
  { fromComp: 'mq2', fromPin: 'GND', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "MQ-2 GND â†’ ESP8266 GND" },
  { fromComp: 'mq2', fromPin: 'A0', toComp: 'esp', toPins: ['A0'], desc: "MQ-2 AO â†’ ESP8266 A0" },
  { fromComp: 'dht11', fromPin: 'VCC', toComp: 'esp', toPins: ['3V3_1', '3V3_2', '3V3_3', 'VIN'], desc: "DHT11 VCC â†’ ESP8266 3V3/VIN" },
  { fromComp: 'dht11', fromPin: 'GND', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "DHT11 GND â†’ ESP8266 GND" },
  { fromComp: 'dht11', fromPin: 'DATA', toComp: 'esp', toPins: ['D2'], desc: "DHT11 DATA â†’ ESP8266 D2" },
  { fromComp: 'res1', fromPin: 'P1', toComp: 'esp', toPins: ['D5'], desc: "Resistor 1 â†’ ESP8266 D5" },
  { fromComp: 'res1', fromPin: 'P2', toComp: 'led_g', toPins: ['A'], desc: "Resistor 1 â†’ Green LED Anode" },
  { fromComp: 'led_g', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "Green LED Cathode â†’ ESP8266 GND" },
  { fromComp: 'res2', fromPin: 'P1', toComp: 'esp', toPins: ['D6'], desc: "Resistor 2 â†’ ESP8266 D6" },
  { fromComp: 'res2', fromPin: 'P2', toComp: 'led_y', toPins: ['A'], desc: "Resistor 2 â†’ Yellow LED Anode" },
  { fromComp: 'led_y', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "Yellow LED Cathode â†’ ESP8266 GND" },
  { fromComp: 'res3', fromPin: 'P1', toComp: 'esp', toPins: ['D7'], desc: "Resistor 3 â†’ ESP8266 D7" },
  { fromComp: 'res3', fromPin: 'P2', toComp: 'led_r', toPins: ['A'], desc: "Resistor 3 â†’ Red LED Anode" },
  { fromComp: 'led_r', fromPin: 'K', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "Red LED Cathode â†’ ESP8266 GND" },
  { fromComp: 'buzzer', fromPin: 'POS', toComp: 'esp', toPins: ['D4'], desc: "Buzzer + â†’ ESP8266 D4" },
  { fromComp: 'buzzer', fromPin: 'NEG', toComp: 'esp', toPins: ['GND1', 'GND2', 'GND3', 'GND4'], desc: "Buzzer - â†’ ESP8266 GND" },
];

const VirtualCircuit = () => {
  const [wiringMode, setWiringMode] = useState('easy');
  const [autoBuilt, setAutoBuilt] = useState(false);
  const navigate = useNavigate();

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
    
    setCircuitReady(true);
  };

  const { riskLevel, smoke, isRunning, setIsRunning, circuitWires: wires, setCircuitWires: setWires, circuitValidation: validation, setCircuitValidation: setValidation, circuitReady, setCircuitReady } = useContext(SimulationContext);
  
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
  
  const [dragging, setDragging] = useState(null);
  const [wiring, setWiring] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [selectedComp, setSelectedComp] = useState(null);
  const svgRef = useRef(null);

  useEffect(() => {
    if (!circuitReady && isRunning) setIsRunning(false);
  }, [circuitReady, isRunning, setIsRunning]);

  const getRelativeCoordinates = (e) => {
    if (!svgRef.current) return { x: 0, y: 0 };
    const rect = svgRef.current.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  };

  const handleMouseDown = (e, compId) => {
    if (wiring) return;
    const pos = getRelativeCoordinates(e);
    setDragging({ comp: compId, offsetX: pos.x - components[compId].x, offsetY: pos.y - components[compId].y });
    setSelectedComp(compId);
  };

  const handleMouseMove = (e) => {
    const pos = getRelativeCoordinates(e);
    setMousePos(pos);
    if (dragging) {
      setComponents(prev => ({ ...prev, [dragging.comp]: { x: pos.x - dragging.offsetX, y: pos.y - dragging.offsetY } }));
    }
  };

  const handleMouseUp = () => setDragging(null);

  const handlePinClick = (e, compId, pinId) => {
    e.stopPropagation();
    if (!wiring) {
      setWiring({ comp: compId, pin: pinId });
    } else {
      if (wiring.comp === compId && wiring.pin === pinId) { setWiring(null); return; }
      
      let color = '#9ca3af'; // Dupont wire colors
      const pinType = COMPONENT_DEF[compId].pins.find(p => p.id === pinId)?.type;
      const startType = COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin)?.type;
      
      if (pinType === 'power' || startType === 'power') color = '#EF4444'; 
      else if (pinType === 'gnd' || startType === 'gnd') color = '#151923'; 
      else if (pinType === 'analog' || startType === 'analog') color = '#F59E0B'; 
      else color = '#22C55E'; 
      
      setWires(prev => [...prev, { id: Date.now().toString(), startComp: wiring.comp, startPin: wiring.pin, endComp: compId, endPin: pinId, color }]);
      setWiring(null);
      setValidation({ status: 'idle', missing: [], valid: false });
      setCircuitReady(false);
    }
  };

  const removeWire = (id, e) => {
    e.stopPropagation();
    setWires(prev => prev.filter(w => w.id !== id));
    setValidation({ status: 'idle', missing: [], valid: false });
    setCircuitReady(false);
  };

  
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


  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-50">Realistic Virtual Laboratory</h1>
          <p className="text-slate-400">Connect the physical pins using Dupont wires.</p>
        </div>
        <div className="flex gap-3">
          
          <button 
            onClick={() => circuitReady && setIsRunning(!isRunning)} 
            disabled={!circuitReady}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition ${circuitReady ? (isRunning ? 'bg-green-900/50 text-green-500 border border-green-900' : 'bg-primary text-slate-50 hover:bg-primary-bright') : 'bg-slate-800 text-slate-500 cursor-not-allowed'}`}
          >
            <Play size={18} /> {isRunning ? 'Stop Simulation' : 'Run Simulation'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Workspace */}
        <div className="lg:col-span-3 glass-card p-1 min-h-[600px] bg-white relative overflow-hidden rounded-xl shadow-inner border-4 border-slate-700" 
             onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}>
          
          <svg ref={svgRef} className="w-full h-full min-h-[600px]" onClick={() => { if(wiring) setWiring(null); setSelectedComp(null); }}>
            
            {/* Grid Pattern */}
            <defs>
              <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1" fill="#E5E7EB" />
              </pattern>
              
              <radialGradient id="ledGlowG" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#4ADE80" stopOpacity="1" />
                <stop offset="100%" stopColor="#22C55E" stopOpacity="0.2" />
              </radialGradient>
              <radialGradient id="ledGlowY" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#FBBF24" stopOpacity="1" />
                <stop offset="100%" stopColor="#F59E0B" stopOpacity="0.2" />
              </radialGradient>
              <radialGradient id="ledGlowR" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#F87171" stopOpacity="1" />
                <stop offset="100%" stopColor="#EF4444" stopOpacity="0.2" />
              </radialGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />

            {/* Wires */}
            {wires.map((wire) => {
              const startComp = components[wire.startComp];
              const startPinDef = COMPONENT_DEF[wire.startComp].pins.find(p => p.id === wire.startPin);
              const endComp = components[wire.endComp];
              const endPinDef = COMPONENT_DEF[wire.endComp].pins.find(p => p.id === wire.endPin);
              if(!startComp || !endComp || !startPinDef || !endPinDef) return null;
              const x1 = startComp.x + startPinDef.x, y1 = startComp.y + startPinDef.y;
              const x2 = endComp.x + endPinDef.x, y2 = endComp.y + endPinDef.y;
              const dx = Math.abs(x2 - x1);
              const path = `M ${x1} ${y1} C ${x1 + dx*0.6} ${y1}, ${x2 - dx*0.6} ${y2}, ${x2} ${y2}`;
              const opacity = (selectedComp && selectedComp !== wire.startComp && selectedComp !== wire.endComp) ? 0.3 : 1;
              return (
                <g key={wire.id} opacity={opacity}>
                  <path d={path} stroke={wire.color} strokeWidth="6" fill="none" className="drop-shadow-md cursor-pointer" onClick={(e) => removeWire(wire.id, e)} />
                  <path d={path} stroke="#ffffff" strokeWidth="1" fill="none" opacity="0.4" className="pointer-events-none" />
                  <circle cx={x1} cy={y1} r="3" fill="#111827" className="pointer-events-none" />
                  <circle cx={x2} cy={y2} r="3" fill="#111827" className="pointer-events-none" />
                </g>
              );
            })}

            {/* Active Wire */}
            {wiring && (
              <path d={`M ${components[wiring.comp].x + COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin).x} ${components[wiring.comp].y + COMPONENT_DEF[wiring.comp].pins.find(p => p.id === wiring.pin).y} L ${mousePos.x} ${mousePos.y}`} 
                stroke="#F59E0B" strokeWidth="4" fill="none" strokeDasharray="5,5" className="pointer-events-none" />
            )}

            {/* BREADBOARD (Photorealistic SVG fallback) */}
            <g transform={`translate(${components.breadboard.x}, ${components.breadboard.y})`} onMouseDown={(e) => handleMouseDown(e, 'breadboard')} className="cursor-move">
              <rect width="600" height="200" rx="8" fill="#F8FAFC" stroke="#CBD5E1" strokeWidth="2" className="drop-shadow-lg" />
              <rect x="0" y="25" width="600" height="2" fill="#EF4444" />
              <rect x="0" y="45" width="600" height="2" fill="#3B82F6" />
              <rect x="0" y="155" width="600" height="2" fill="#3B82F6" />
              <rect x="0" y="175" width="600" height="2" fill="#EF4444" />
              <rect x="0" y="95" width="600" height="10" fill="#E2E8F0" />
              {/* Terminal holes rendering (visual only to keep DOM light) */}
              <pattern id="bb-holes" width="15" height="15" patternUnits="userSpaceOnUse">
                <rect width="6" height="6" fill="#1E293B" rx="1" />
              </pattern>
              <rect x="30" y="10" width="540" height="15" fill="url(#bb-holes)" />
              <rect x="30" y="55" width="540" height="30" fill="url(#bb-holes)" />
              <rect x="30" y="115" width="540" height="30" fill="url(#bb-holes)" />
              <rect x="30" y="180" width="540" height="15" fill="url(#bb-holes)" />
              <text x="300" y="103" fill="#94A3B8" fontSize="12" textAnchor="middle" fontWeight="bold">SOLDERLESS BREADBOARD</text>
              {/* Render interactive pins */}
              {COMPONENT_DEF.breadboard.pins.map(p => (
                <g key={p.id} transform={`translate(${p.x}, ${p.y})`} onClick={(e) => handlePinClick(e, 'breadboard', p.id)} className="cursor-pointer">
                  <rect x="-6" y="-6" width="12" height="12" fill="transparent" stroke={wiring?.comp==='breadboard' && wiring?.pin===p.id ? '#F59E0B' : 'none'} strokeWidth="2" />
                </g>
              ))}
            </g>

            {/* ESP8266 (Real Image or realistic fallback) */}
            <g transform={`translate(${components.esp.x}, ${components.esp.y})`} onMouseDown={(e) => handleMouseDown(e, 'esp')} className="cursor-move">
              <image href="/images/esp8266.jpg" width="200" height="260" preserveAspectRatio="xMidYMid slice" className="drop-shadow-xl rounded" />
              <rect width="200" height="260" fill="none" stroke={selectedComp === 'esp' ? '#F59E0B' : '#000'} strokeWidth="2" rx="4" />
              {/* Interactive overlay pins */}
              {COMPONENT_DEF.esp.pins.map(p => {
                const isW = wiring?.comp === 'esp' && wiring?.pin === p.id;
                return (
                  <g key={p.id} transform={`translate(${p.x}, ${p.y})`} onClick={(e) => handlePinClick(e, 'esp', p.id)} className="cursor-pointer group">
                    <rect x="-8" y="-6" width="16" height="12" fill="#F59E0B" opacity={isW ? "0.8" : "0"} className="hover:opacity-50" />
                    <rect x="-25" y="-10" width="50" height="20" fill="#1C222D" opacity="0.9" className="hidden group-hover:block" rx="2" />
                    <text x="0" y="4" fill="#F59E0B" fontSize="12" textAnchor="middle" className="hidden group-hover:block font-bold">{p.label}</text>
                  </g>
                );
              })}
            </g>

            {/* MQ-2 */}
            <g transform={`translate(${components.mq2.x}, ${components.mq2.y})`} onMouseDown={(e) => handleMouseDown(e, 'mq2')} className="cursor-move">
              <rect width="80" height="100" fill="#1E3A8A" rx="4" className="drop-shadow-lg" stroke={selectedComp === 'mq2' ? '#F59E0B' : '#1e3a8a'} />
              <circle cx="40" cy="40" r="30" fill="#D1D5DB" stroke="#9CA3AF" strokeWidth="3" />
              <circle cx="40" cy="40" r="20" fill="#4B5563" />
              <text x="40" y="43" fill="#F8FAFC" fontSize="10" textAnchor="middle" fontWeight="bold">MQ-2</text>
              {COMPONENT_DEF.mq2.pins.map(p => (
                <g key={p.id} transform={`translate(${p.x}, ${p.y})`} onClick={(e) => handlePinClick(e, 'mq2', p.id)} className="cursor-pointer group">
                  <circle cx="0" cy="0" r="5" fill="#FCD34D" stroke="#B45309" />
                  <text x="0" y="-12" fill="#F1F5F9" fontSize="9" textAnchor="middle" className="font-mono">{p.label}</text>
                  {wiring?.comp==='mq2' && wiring?.pin===p.id && <circle cx="0" cy="0" r="8" stroke="#F59E0B" fill="none" strokeWidth="2" />}
                </g>
              ))}
            </g>

            {/* DHT11 */}
            <g transform={`translate(${components.dht11.x}, ${components.dht11.y})`} onMouseDown={(e) => handleMouseDown(e, 'dht11')} className="cursor-move">
              <image href="/images/dht11.jpg" width="60" height="80" preserveAspectRatio="xMidYMid slice" className="drop-shadow-lg rounded" />
              <rect width="60" height="80" fill="none" stroke={selectedComp === 'dht11' ? '#F59E0B' : '#0369A1'} strokeWidth="2" rx="4" />
              {COMPONENT_DEF.dht11.pins.map(p => (
                <g key={p.id} transform={`translate(${p.x}, ${p.y})`} onClick={(e) => handlePinClick(e, 'dht11', p.id)} className="cursor-pointer group">
                  <circle cx="0" cy="0" r="5" fill="#F59E0B" opacity={wiring?.comp==='dht11' && wiring?.pin===p.id ? "1" : "0"} className="hover:opacity-80" />
                  <text x="0" y="-10" fill="#0369A1" fontSize="10" textAnchor="middle" fontWeight="bold" className="drop-shadow-md">{p.label}</text>
                </g>
              ))}
            </g>

            {/* LEDs */}
            {[
              { id: 'led_g', comp: components.led_g, color: '#22C55E', active: riskLevel === 0, glow: 'url(#ledGlowG)' },
              { id: 'led_y', comp: components.led_y, color: '#F59E0B', active: riskLevel === 1, glow: 'url(#ledGlowY)' },
              { id: 'led_r', comp: components.led_r, color: '#EF4444', active: riskLevel === 2, glow: 'url(#ledGlowR)' }
            ].map(led => (
              <g key={led.id} transform={`translate(${led.comp.x}, ${led.comp.y})`} onMouseDown={(e) => handleMouseDown(e, led.id)} className="cursor-move">
                <path d="M 10 30 L 10 65 M 20 30 L 20 65" stroke="#9CA3AF" strokeWidth="2" />
                <circle cx="15" cy="15" r="15" fill={circuitReady && isRunning && led.active ? led.glow : `${led.color}80`} stroke={led.color} strokeWidth="2" />
                <path d="M 5 25 Q 15 10 25 25" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.6" />
                {COMPONENT_DEF[led.id].pins.map(p => (
                  <circle key={p.id} cx={p.x} cy={p.y} r="4" fill="#FCD34D" className="cursor-pointer hover:stroke-orange-500" strokeWidth="2" onClick={(e) => handlePinClick(e, led.id, p.id)} />
                ))}
              </g>
            ))}

            {/* Resistors */}
            {['res1', 'res2', 'res3'].map(res => (
              <g key={res} transform={`translate(${components[res].x}, ${components[res].y})`} onMouseDown={(e) => handleMouseDown(e, res)} className="cursor-move">
                <image href="/images/resistor.jpg" width="80" height="20" preserveAspectRatio="xMidYMid slice" className="drop-shadow-md" />
                {COMPONENT_DEF[res].pins.map(p => (
                  <rect key={p.id} x={p.x-5} y={p.y-5} width="10" height="10" fill="#F59E0B" opacity={wiring?.comp===res && wiring?.pin===p.id ? "1" : "0"} className="cursor-pointer hover:opacity-50" onClick={(e) => handlePinClick(e, res, p.id)} />
                ))}
              </g>
            ))}

            {/* Buzzer */}
            <g transform={`translate(${components.buzzer.x}, ${components.buzzer.y})`} onMouseDown={(e) => handleMouseDown(e, 'buzzer')} className="cursor-move">
              <circle cx="30" cy="30" r="30" fill="#111827" stroke="#374151" strokeWidth="3" className="drop-shadow-xl" />
              <circle cx="30" cy="30" r="8" fill="#030712" />
              {circuitReady && isRunning && riskLevel === 2 && <circle cx="30" cy="30" r="35" stroke="#EF4444" strokeWidth="3" fill="none" className="animate-ping pointer-events-none" />}
              <text x="15" y="20" fill="#F5F5F5" fontSize="16" fontWeight="bold">+</text>
              {COMPONENT_DEF.buzzer.pins.map(p => (
                <circle key={p.id} cx={p.x} cy={p.y} r="4" fill="#FCD34D" className="cursor-pointer" onClick={(e) => handlePinClick(e, 'buzzer', p.id)} />
              ))}
            </g>

          </svg>
        </div>

        {/* Inspector Sidebar */}
        <div className="flex flex-col gap-6">
          <div className="glass-card p-5 h-64 overflow-y-auto">
            <h3 className="text-lg font-bold text-slate-50 mb-3 flex items-center gap-2"><CheckCircle size={18} className="text-primary"/> Validation</h3>
            {validation.status === 'idle' && <p className="text-sm text-slate-400">Click "Validate Circuit" to check your connections.</p>}
            {validation.status === 'validated' && (
              <div>
                <div className="text-2xl font-bold text-slate-50 mb-2">{validation.correct} / {validation.total}</div>
                {validation.valid ? (
                  <div className="bg-green-900/30 text-green-400 p-3 rounded-lg border border-green-800 text-sm flex gap-2">
                    <CheckCircle size={16} className="shrink-0" />
                    <div>Circuit VALID. You can now start the experiment.</div>
                  </div>
                ) : (
                  <div className="bg-red-900/20 p-3 rounded-lg border border-red-800/50 text-sm">
                    <div className="text-red-400 font-bold mb-2 flex items-center gap-1"><AlertTriangle size={16}/> Missing:</div>
                    <ul className="list-disc pl-4 text-slate-300 text-xs space-y-1">
                      {validation.missing.map((msg, i) => <li key={i}>{msg}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="glass-card p-5 flex-1 flex flex-col">
            <h3 className="text-lg font-bold text-slate-50 mb-4 flex items-center gap-2"><Info size={18} className="text-primary"/> Inspector</h3>
            {selectedComp ? (
              <div className="flex-1 flex flex-col">
                <h4 className="text-primary font-bold text-xl mb-1">{COMPONENT_DEF[selectedComp].name}</h4>
                <p className="text-sm text-slate-300 mb-4">{COMPONENT_DEF[selectedComp].desc}</p>
                <h5 className="font-semibold text-slate-200 text-xs uppercase mb-2">Connected Pins:</h5>
                <div className="bg-slate-900 rounded p-2 text-xs font-mono space-y-1 border border-slate-700 flex-1 overflow-y-auto">
                  {wires.filter(w => w.startComp === selectedComp || w.endComp === selectedComp).length === 0 && <span className="text-slate-500">No connections.</span>}
                  {wires.map(w => {
                    if(w.startComp === selectedComp) return <div key={w.id} className="text-slate-300">[{w.startPin}] â†’ {COMPONENT_DEF[w.endComp].name} [{w.endPin}]</div>;
                    if (w.endComp === selectedComp) return <div key={w.id} className="text-slate-300">[{w.endPin}] â† {COMPONENT_DEF[w.startComp].name} [{w.startPin}]</div>;
                    return null;
                  })}
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-center">
                <Cpu size={48} className="mb-4 opacity-30" />
                <p className="text-sm">Select a realistic component to inspect.</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
export default VirtualCircuit;

