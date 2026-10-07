import { HashRouter as Router, Routes, Route } from 'react-router-dom';
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
import Settings from './pages/Settings';
import NotificationsPage from './pages/NotificationsPage';
import { SimulationProvider } from './context/SimulationContext';
import { SettingsProvider } from './context/SettingsContext';

function App() {
  return (
    <SettingsProvider>
      <SimulationProvider>
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
              <Route path="/settings" element={<Settings />} />
              <Route path="/notifications" element={<NotificationsPage />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </Layout>
        </Router>
      </SimulationProvider>
    </SettingsProvider>
  );
}

export default App;
