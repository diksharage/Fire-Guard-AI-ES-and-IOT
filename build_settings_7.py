import re

with open('src/context/SimulationContext.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# We need to import SettingsContext at the top
if 'SettingsContext' not in code:
    code = code.replace("import React, { createContext, useState, useEffect } from 'react';", "import React, { createContext, useState, useEffect, useContext } from 'react';\nimport { SettingsContext } from './SettingsContext';")

# We need to replace `const [isSoundEnabled, setIsSoundEnabled] = useState(true);` with getting it from Settings
code = re.sub(r'const \[isSoundEnabled, setIsSoundEnabled\] = useState\(true\);\s*', '', code)
    
# We need to get `settings` inside the provider
if 'export const SimulationProvider = ({ children }) => {' in code:
    if 'const { settings } = useContext(SettingsContext);' not in code:
        code = code.replace(
            "export const SimulationProvider = ({ children }) => {",
            "export const SimulationProvider = ({ children }) => {\n  const { settings } = useContext(SettingsContext);\n  const isSoundEnabled = settings?.buzzerSound ?? true;"
        )

# Remove `setIsSoundEnabled` from provider value
code = code.replace("isSoundEnabled, setIsSoundEnabled,", "isSoundEnabled,")

# Add clearNotifications
if 'const clearNotifications = () => setNotifications([]);' not in code:
    code = code.replace('const markAllRead = () => {', 'const clearNotifications = () => setNotifications([]);\n  const markAllRead = () => {')
    code = code.replace('notifications, addNotification, markAllRead,', 'notifications, addNotification, markAllRead, clearNotifications,')

# Add clearHistory (Check if it's already there first!)
if 'clearHistory' not in code:
    code = code.replace('const [sensorHistory, setSensorHistory] = useState', 'const clearHistory = () => { setSensorHistory([]); localStorage.removeItem("fireguard_history"); };\n  const [sensorHistory, setSensorHistory] = useState')
    code = code.replace('sensorHistory, setSensorHistory,', 'sensorHistory, setSensorHistory, clearHistory,')

with open('src/context/SimulationContext.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated SimulationContext flawlessly")
