import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

vc = read_file('src/pages/VirtualCircuit.jsx')
if 'SettingsContext' not in vc:
    vc = vc.replace("import { SimulationContext } from '../context/SimulationContext';", "import { SimulationContext } from '../context/SimulationContext';\nimport { SettingsContext } from '../context/SettingsContext';")
    
    # Replace internal wiringMode state with settings.experimentMode
    vc = vc.replace("const [wiringMode, setWiringMode] = useState('easy');", "const { settings } = useContext(SettingsContext);\n  const wiringMode = settings?.experimentMode || 'easy';")

write_file('src/pages/VirtualCircuit.jsx', vc)
print("Updated VirtualCircuit.jsx")
