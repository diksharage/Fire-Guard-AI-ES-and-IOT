import os

DIR = r"C:\Users\Diksha\OneDrive\Desktop\ES and IOT\FireGuard-AI\src"

# 1. Update App.jsx
app_jsx = """
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import VirtualCircuit from './pages/VirtualCircuit';
import ExperimentLab from './pages/ExperimentLab';
import AIClassifier from './pages/AIClassifier';
import IoTDashboard from './pages/IoTDashboard';
import Analytics from './pages/Analytics';
import History from './pages/History';
import About from './pages/About';
import Guidelines from './pages/Guidelines';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/guidelines" element={<Guidelines />} />
          <Route path="/circuit" element={<VirtualCircuit />} />
          <Route path="/lab" element={<ExperimentLab />} />
          <Route path="/ai" element={<AIClassifier />} />
          <Route path="/iot" element={<IoTDashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
"""
with open(os.path.join(DIR, "App.jsx"), "w", encoding="utf-8") as f:
    f.write(app_jsx.strip() + "\\n")


# 2. Update Layout.jsx
layout_path = os.path.join(DIR, "components", "Layout.jsx")
with open(layout_path, "r", encoding="utf-8") as f:
    layout = f.read()

# Add BookOpen to lucide imports
if "BookOpen" not in layout:
    layout = layout.replace("from 'lucide-react';", "BookOpen, from 'lucide-react';").replace("BookOpen, from", "BookOpen,")

# Add Guidelines to navItems as the second item
if "path: '/guidelines'" not in layout:
    nav_str = "const navItems = ["
    new_nav = "const navItems = [\n    { path: '/guidelines', label: 'Experiment Guidelines', icon: <BookOpen size={20} /> },"
    layout = layout.replace(nav_str, new_nav)

with open(layout_path, "w", encoding="utf-8") as f:
    f.write(layout)

print("App.jsx and Layout.jsx updated successfully.")
