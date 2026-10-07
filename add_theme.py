import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

# 1. Update index.css
index_css = """@import "tailwindcss";

:root {
  --app-darker: #080B12;
  --app-sidebar: #151923;
  --app-card: #1C222D;
  
  --app-primary: #F59E0B;
  --app-primary-bright: #FFB020;
  
  --app-slate-50: #ffffff;
  --app-slate-100: #f5f5f5;
  --app-slate-200: #e5e7eb;
  --app-slate-300: #d1d5db;
  --app-slate-400: #9ca3af;
  --app-slate-500: #6b7280;
  --app-slate-600: #4b5563;
  --app-slate-700: #2a3342;
  --app-slate-800: #151923;
  --app-slate-900: #080b12;
}

.light {
  --app-darker: #F3F4F6;
  --app-sidebar: #FFFFFF;
  --app-card: #FFFFFF;
  
  --app-primary: #D97706;
  --app-primary-bright: #F59E0B;
  
  /* Inverted slate scale */
  --app-slate-900: #FFFFFF;
  --app-slate-800: #F9FAFB;
  --app-slate-700: #E5E7EB;
  --app-slate-600: #D1D5DB;
  --app-slate-500: #9CA3AF;
  --app-slate-400: #6B7280;
  --app-slate-300: #4B5563;
  --app-slate-200: #374151;
  --app-slate-100: #1F2937;
  --app-slate-50:  #111827;
}

@theme {
  --color-darker: var(--app-darker);
  --color-sidebar: var(--app-sidebar);
  --color-card: var(--app-card);
  
  --color-primary: var(--app-primary);
  --color-primary-bright: var(--app-primary-bright);
  
  --color-danger: #EF4444;
  --color-warning: #F59E0B;
  --color-safe: #22C55E;

  --color-slate-50: var(--app-slate-50);
  --color-slate-100: var(--app-slate-100);
  --color-slate-200: var(--app-slate-200);
  --color-slate-300: var(--app-slate-300);
  --color-slate-400: var(--app-slate-400);
  --color-slate-500: var(--app-slate-500);
  --color-slate-600: var(--app-slate-600);
  --color-slate-700: var(--app-slate-700);
  --color-slate-800: var(--app-slate-800);
  --color-slate-900: var(--app-slate-900);
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


# 2. Replace text-white with text-slate-50 globally in JSX files
import glob

jsx_files = glob.glob(os.path.join(DIR, "**", "*.jsx"), recursive=True)
for file in jsx_files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "text-white" in content:
        content = content.replace("text-white", "text-slate-50")
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)


# 3. Update Layout.jsx with Theme Toggle
layout_path = os.path.join(DIR, "components", "Layout.jsx")
with open(layout_path, "r", encoding="utf-8") as f:
    layout = f.read()

# Add Moon and Sun to imports
if "Moon" not in layout:
    layout = layout.replace("Bell , BookOpen }", "Bell, BookOpen, Moon, Sun }")

# Add state and effect for theme
if "const [theme, setTheme]" not in layout:
    # Find Layout start
    insert_point = layout.find("const [sidebarOpen, setSidebarOpen] = useState(false);")
    theme_logic = """
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('fireguard_theme') || 'dark';
  });

  import { useEffect } from 'react';
  // Note: we can't do top level import inside component easily, so we use React.useEffect if needed, but since useEffect is not imported from react, we will just patch the react import.
"""
    # Fix import React first
    if "useEffect" not in layout:
        layout = layout.replace("import { useState }", "import { useState, useEffect }")
    
    theme_logic = """
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('fireguard_theme') || 'dark';
  });

  useEffect(() => {
    if (theme === 'light') {
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
    }
    localStorage.setItem('fireguard_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };
"""
    layout = layout[:insert_point] + theme_logic + layout[insert_point:]

# Add toggle button near the notifications bell
if "toggleTheme" in layout:
    bell_idx = layout.find("<Bell size={20} />")
    if bell_idx != -1:
        # wrap it in the parent div logic
        button_html = """
              <button onClick={toggleTheme} className="text-slate-400 hover:text-slate-50 transition-colors p-2 rounded-full hover:bg-slate-800">
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>
"""
        # Find the div containing the bell
        target = '<button className="text-slate-400 hover:text-slate-50 transition-colors relative">'
        t_idx = layout.find(target)
        if t_idx != -1:
            layout = layout[:t_idx] + button_html + layout[t_idx:]

with open(layout_path, "w", encoding="utf-8") as f:
    f.write(layout)

print("Theme support added successfully.")
