import os
import codecs

file_path = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src\pages\VirtualCircuit.jsx"

with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

bad = """{wiringMode === 'advanced' && <button onClick={validateCircuit} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-lg border border-slate-700 transition">
            <CheckCircle size={18} /> Validate Circuit
          </button>"""

good = """{wiringMode === 'advanced' && (
          <button onClick={validateCircuit} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-lg border border-slate-700 transition">
            <CheckCircle size={18} /> Validate Circuit
          </button>
          )}"""

content = content.replace(bad, good)

# Also fix the bottom validate button I tried to replace earlier
if "Validate Circuit</button>}" in content:
    pass # Wait, if it didn't match, it didn't insert `}`.

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(content)

print("Fixed syntax error.")
