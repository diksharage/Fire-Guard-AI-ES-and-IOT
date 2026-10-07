import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 4. UPDATE DASHBOARD (Read preferences)
dash_code = read_file('src/pages/Dashboard.jsx')
if 'SettingsContext' not in dash_code:
    dash_code = dash_code.replace("import { SimulationContext } from '../context/SimulationContext';", "import { SimulationContext } from '../context/SimulationContext';\nimport { SettingsContext } from '../context/SettingsContext';")
    dash_code = dash_code.replace("dismissAlert } = useContext(SimulationContext);", "dismissAlert } = useContext(SimulationContext);\n  const { settings } = useContext(SettingsContext);\n  const prefs = settings?.dashboardPrefs || {};")

# Add conditional rendering to Dashboard items based on prefs
# Example for Temperature:
dash_code = dash_code.replace('<div className="glass-card p-5">', '{prefs.showTemperature !== false && (<div className="glass-card p-5">', 1)
dash_code = dash_code.replace('</div>\n          <div className="glass-card p-5">\n            <div className="flex items-center gap-3', '</div>)}\n          {prefs.showSmoke !== false && (<div className="glass-card p-5">\n            <div className="flex items-center gap-3', 1)
# Humidity
dash_code = dash_code.replace('</div>\n          <div className="glass-card p-5">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Droplets />', '</div>)}\n          {prefs.showHumidity !== false && (<div className="glass-card p-5">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Droplets />', 1)
# AI Confidence
dash_code = dash_code.replace('</div>\n          <div className="glass-card p-5">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><BrainCircuit />', '</div>)}\n          {prefs.showAiConfidence !== false && (<div className="glass-card p-5">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><BrainCircuit />', 1)
# Buzzer
dash_code = dash_code.replace('</div>\n          <div className="glass-card p-5 lg:col-span-2">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Volume2 />', '</div>)}\n          {prefs.showBuzzer !== false && (<div className="glass-card p-5 lg:col-span-2">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Volume2 />', 1)
# IoT
dash_code = dash_code.replace('</div>\n          <div className="glass-card p-5 lg:col-span-2">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Activity />', '</div>)}\n          {prefs.showIoT !== false && (<div className="glass-card p-5 lg:col-span-2">\n            <div className="flex items-center gap-3 text-slate-400 mb-3"><Activity />', 1)
# Trends
dash_code = dash_code.replace('</div>\n        </div>\n\n        {/* Charts & History */}', '</div>)}\n        </div>\n\n        {/* Charts & History */}')
if '{prefs.showTrends !== false && (' not in dash_code:
    dash_code = dash_code.replace('{/* Charts & History */}\n        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">', '{/* Charts & History */}\n        {prefs.showTrends !== false && (\n        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">')
    dash_code = dash_code.replace('</div>\n      </div>\n    </div>\n  );\n};', '</div>\n        )}\n      </div>\n    </div>\n  );\n};')

write_file('src/pages/Dashboard.jsx', dash_code)

# 5. UPDATE EXPERIMENT LAB
lab_code = read_file('src/pages/ExperimentLab.jsx')
if 'SettingsContext' not in lab_code:
    lab_code = lab_code.replace("import { SimulationContext } from '../context/SimulationContext';", "import { SimulationContext } from '../context/SimulationContext';\nimport { SettingsContext } from '../context/SettingsContext';")
    lab_code = lab_code.replace("} = useContext(SimulationContext);", "} = useContext(SimulationContext);\n  const { settings, updateSetting } = useContext(SettingsContext);")
    lab_code = lab_code.replace("onClick={() => setIsSoundEnabled(!isSoundEnabled)}", "onClick={() => updateSetting('buzzerSound', !settings.buzzerSound)}")
    lab_code = lab_code.replace("isSoundEnabled ?", "settings.buzzerSound ?")

write_file('src/pages/ExperimentLab.jsx', lab_code)

print("Updated Dashboard and ExperimentLab")
