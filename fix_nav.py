import codecs

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx"
with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

if 'useNavigate' not in content:
    content = content.replace("import { Cpu, Info, Play, CheckCircle, AlertTriangle } from 'lucide-react';", 
                              "import { Cpu, Info, Play, CheckCircle, AlertTriangle } from 'lucide-react';\nimport { useNavigate } from 'react-router-dom';")
    
    content = content.replace("const [autoBuilt, setAutoBuilt] = useState(false);", 
                              "const [autoBuilt, setAutoBuilt] = useState(false);\n  const navigate = useNavigate();")

    content = content.replace("window.location.href='/lab'", "navigate('/lab')")

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)

print("Navigation fixed.")
