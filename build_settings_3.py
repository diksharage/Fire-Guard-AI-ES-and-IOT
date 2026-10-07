import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 3. UPDATE SIMULATION CONTEXT
sim_code = read_file('src/context/SimulationContext.jsx')

# We need to import SettingsContext at the top
if 'SettingsContext' not in sim_code:
    sim_code = sim_code.replace("import React, { createContext, useState, useEffect } from 'react';", "import React, { createContext, useState, useEffect, useContext } from 'react';\nimport { SettingsContext } from './SettingsContext';")

# We need to replace `const [isSoundEnabled, setIsSoundEnabled] = useState(true);` with getting it from Settings
if 'const [isSoundEnabled, setIsSoundEnabled] = useState(true);' in sim_code:
    sim_code = sim_code.replace("const [isSoundEnabled, setIsSoundEnabled] = useState(true);", "")
    
# We need to get `settings` inside the provider
if 'export const SimulationProvider = ({ children }) => {' in sim_code:
    if 'const { settings } = useContext(SettingsContext);' not in sim_code:
        sim_code = sim_code.replace(
            "export const SimulationProvider = ({ children }) => {",
            "export const SimulationProvider = ({ children }) => {\n  const { settings } = useContext(SettingsContext);\n  const isSoundEnabled = settings?.buzzerSound ?? true;"
        )

# Remove `setIsSoundEnabled` from provider value
sim_code = sim_code.replace("isSoundEnabled, setIsSoundEnabled,", "isSoundEnabled,")

# Add clearNotifications
if 'const clearNotifications = () => setNotifications([]);' not in sim_code:
    sim_code = sim_code.replace('const markAllRead = () => {', 'const clearNotifications = () => setNotifications([]);\n  const markAllRead = () => {')
    sim_code = sim_code.replace('notifications, addNotification, markAllRead,', 'notifications, addNotification, markAllRead, clearNotifications,')

# Add clearHistory
if 'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };' not in sim_code:
    sim_code = sim_code.replace('const [sensorHistory, setSensorHistory] = useState', 'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };\n  const [sensorHistory, setSensorHistory] = useState')
    sim_code = sim_code.replace('sensorHistory, setSensorHistory,', 'sensorHistory, setSensorHistory, clearHistory,')

write_file('src/context/SimulationContext.jsx', sim_code)
print("Updated SimulationContext")
