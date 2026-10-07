import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update index.css completely
index_css = """@import "tailwindcss";

@theme {
  --color-darker: #080B12;
  --color-sidebar: #151923;
  --color-card: #1C222D;
  
  --color-primary: #F59E0B;
  --color-primary-bright: #FFB020;
  
  --color-danger: #EF4444;
  --color-warning: #F59E0B;
  --color-safe: #22C55E;

  /* Premium Charcoal Palette mappings */
  --color-slate-50: #f5f5f5;
  --color-slate-100: #f5f5f5;
  --color-slate-200: #f5f5f5;
  --color-slate-300: #d1d5db;
  --color-slate-400: #9ca3af;
  --color-slate-500: #6b7280;
  --color-slate-600: #4b5563;
  --color-slate-700: #2a3342;
  --color-slate-800: #151923;
  --color-slate-900: #080b12;
}

body {
  @apply bg-darker text-slate-200 overflow-x-hidden;
}

.glass-card {
  @apply bg-card border border-slate-700 rounded-xl shadow-xl;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: var(--color-darker); 
}
::-webkit-scrollbar-thumb {
  background: var(--color-slate-700); 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--color-slate-500); 
}
"""
with open(os.path.join(DIR, "index.css"), "w", encoding="utf-8") as f:
    f.write(index_css)


# Layout overrides
replace_in_file(os.path.join(DIR, "components", "Layout.jsx"), [
    ("bg-card border-r border-slate-800", "bg-sidebar border-r border-slate-700"),
    ("text-orange-500 animate-pulse", "text-primary animate-pulse"),
    ("bg-primary/10 text-primary", "bg-primary/10 text-primary"),
    ("border-b border-slate-800", "border-b border-slate-700"),
])

# Controls overrides
replace_in_file(os.path.join(DIR, "components", "Controls.jsx"), [
    ("accent-orange-500", "accent-primary"),
    ("text-orange-400", "text-primary"),
    ("hover:bg-orange-500", "hover:bg-primary-bright"),
])

# Dashboard overrides
replace_in_file(os.path.join(DIR, "pages", "Dashboard.jsx"), [
    ("bg-orange-500/20 text-orange-500", "bg-primary/20 text-primary"),
    ("bg-blue-500/20 text-blue-400", "bg-primary/20 text-primary"),
    ("#f97316", "#f59e0b"),
])

# AI Classifier overrides
replace_in_file(os.path.join(DIR, "pages", "AIClassifier.jsx"), [
    ("bg-blue-900/50 border-2 border-blue-500 text-blue-100", "bg-slate-800 border-2 border-primary text-slate-200"),
    ("bg-blue-900/50 border-2 border-blue-500", "bg-slate-800 border-2 border-primary"),
    ("text-blue-100", "text-slate-200"),
    ("text-orange-400", "text-primary"),
    ("#f97316", "#f59e0b"),
])

# IoT Dashboard overrides
replace_in_file(os.path.join(DIR, "pages", "IoTDashboard.jsx"), [
    ("border-t-blue-500", "border-t-primary"),
    ("text-blue-500 mb-2", "text-primary mb-2"),
    ("text-blue-400", "text-primary-bright"),
    ("text-blue-300", "text-slate-400"),
    ("text-orange-300", "text-primary-bright"),
    ("text-purple-300", "text-slate-300"),
])

# Analytics overrides
replace_in_file(os.path.join(DIR, "pages", "Analytics.jsx"), [
    ("text-orange-400", "text-primary"),
    ("#f97316", "#f59e0b"),
])

# Virtual Circuit overrides
replace_in_file(os.path.join(DIR, "pages", "VirtualCircuit.jsx"), [
    ("#3b82f6", "#9ca3af"),
    ("text-orange-500", "text-primary"),
    ("bg-blue-500", "bg-primary"),
])

# Experiment Lab
replace_in_file(os.path.join(DIR, "pages", "ExperimentLab.jsx"), [
    ("text-orange-400", "text-primary"),
    ("hover:bg-orange-500", "hover:bg-primary-bright"),
])

# History
replace_in_file(os.path.join(DIR, "pages", "History.jsx"), [
    ("text-orange-400", "text-primary"),
])

print("Color theme updated.")
