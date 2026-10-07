import React, { createContext, useState, useEffect } from 'react';

export const SimulationContext = createContext();

export const SimulationProvider = ({ children }) => {
  // Environmental States
  const [temperature, setTemperature] = useState(25);
  const [smoke, setSmoke] = useState(15);
  const [humidity, setHumidity] = useState(45);
  
  // AI States
  const [riskLevel, setRiskLevel] = useState(0); // 0=NORMAL, 1=WARNING, 2=HIGH RISK
  const [aiConfidence, setAiConfidence] = useState(95);
  const [alerts, setAlerts] = useState([]);
  
  // History
  const [sensorHistory, setSensorHistory] = useState(() => {
    const saved = localStorage.getItem('fireguard_history');
    return saved ? JSON.parse(saved) : [];
  });
  
  // Circuit States
  const [circuitWires, setCircuitWires] = useState([
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
  ]);
  const [circuitValidation, setCircuitValidation] = useState({ status: 'validated', missing: [], valid: true, correct: 17, total: 17 });
  const [circuitReady, setCircuitReady] = useState(true);
  
  // App States
  const [isRunning, setIsRunning] = useState(false);
  
  // Derived Hardware States
  const buzzerStatus = isRunning && circuitReady && riskLevel === 2;
  const greenLedStatus = isRunning && circuitReady && riskLevel === 0;
  const yellowLedStatus = isRunning && circuitReady && riskLevel === 1;
  const redLedStatus = isRunning && circuitReady && riskLevel === 2;

  // AI Classification Logic
  useEffect(() => {
    let newRisk = 0;
    let confidence = 85 + Math.random() * 10;
    
    // Demonstration parameters
    if (smoke >= 65 && temperature >= 45) {
      newRisk = 2; // HIGH RISK
      confidence = 92 + Math.random() * 6;
    } else if (smoke >= 40 || temperature >= 35) {
      newRisk = 1; // WARNING
      confidence = 88 + Math.random() * 8;
    } else {
      newRisk = 0; // NORMAL
      confidence = 95 + Math.random() * 4;
    }
    
    // Add Alert if risk increases
    if (newRisk > riskLevel) {
      const timestamp = new Date().toLocaleTimeString();
      let msg = newRisk === 2 ? 'High fire-risk condition detected in simulation.' : 'Smoke/Temp increased. Risk status changed to WARNING.';
      setAlerts(prev => [{ id: Date.now(), time: timestamp, message: msg, type: newRisk }, ...prev].slice(0, 10));
    }
    
    setRiskLevel(newRisk);
    setAiConfidence(Math.round(confidence));
  }, [temperature, smoke, humidity]);

  // History Logging
  useEffect(() => {
    localStorage.setItem('fireguard_history', JSON.stringify(sensorHistory));
  }, [sensorHistory]);

  useEffect(() => {
    let interval;
    if (isRunning && circuitReady) {
      interval = setInterval(() => {
        setSensorHistory(prev => {
          const newEntry = {
            time: new Date().toLocaleTimeString([], { hour12: false }),
            temperature,
            smoke,
            humidity,
            riskLevel,
            aiConfidence
          };
          return [...prev, newEntry].slice(-50); // Keep last 50 points
        });
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isRunning, circuitReady, temperature, smoke, humidity, riskLevel, aiConfidence]);

  const clearHistory = () => {
    setSensorHistory([]);
    setAlerts([]);
    localStorage.removeItem('fireguard_history');
  };

  const dismissAlert = (id) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  return (
    <SimulationContext.Provider value={{
      temperature, setTemperature,
      smoke, setSmoke,
      humidity, setHumidity,
      riskLevel,
      aiConfidence,
      alerts, dismissAlert,
      sensorHistory, clearHistory,
      circuitWires, setCircuitWires,
      circuitValidation, setCircuitValidation,
      circuitReady, setCircuitReady,
      isRunning, setIsRunning,
      buzzerStatus, greenLedStatus, yellowLedStatus, redLedStatus
    }}>
      {children}
    </SimulationContext.Provider>
  );
};
