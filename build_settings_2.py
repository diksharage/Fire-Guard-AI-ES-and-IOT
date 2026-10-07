import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

settings_code = """import React, { useContext } from 'react';
import { SettingsContext } from '../context/SettingsContext';
import { SimulationContext } from '../context/SimulationContext';
import { Moon, Sun, Monitor, ShieldAlert, Activity, Volume2, VolumeX, Bell, Database, Trash2, RotateCcw } from 'lucide-react';

const Settings = () => {
  const { settings, updateSetting, updateDashboardPref, resetAllSettings } = useContext(SettingsContext);
  const { clearHistory, clearNotifications } = useContext(SimulationContext);

  const Section = ({ title, icon, children }) => (
    <div className="glass-card p-6 mb-6">
      <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2 mb-6 pb-4 border-b border-slate-700/50">
        {icon} {title}
      </h3>
      <div className="space-y-6">
        {children}
      </div>
    </div>
  );

  const Toggle = ({ label, desc, checked, onChange }) => (
    <div className="flex items-center justify-between">
      <div>
        <p className="font-semibold text-slate-200">{label}</p>
        <p className="text-sm text-slate-400">{desc}</p>
      </div>
      <button 
        onClick={() => onChange(!checked)}
        className={`w-12 h-6 rounded-full transition-colors relative flex items-center ${checked ? 'bg-primary' : 'bg-slate-700'}`}
      >
        <span className={`w-4 h-4 rounded-full bg-white absolute transition-transform ${checked ? 'translate-x-7' : 'translate-x-1'}`} />
      </button>
    </div>
  );

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12">
      <div>
        <h1 className="text-3xl font-bold text-slate-50">Settings</h1>
        <p className="text-slate-400">Configure your FireGuard AI laboratory experience</p>
      </div>

      <Section title="Appearance" icon={<Moon size={24} className="text-indigo-400" />}>
        <div>
          <p className="font-semibold text-slate-200 mb-3">Theme</p>
          <div className="flex gap-4">
            {['dark', 'light', 'system'].map(t => (
              <button 
                key={t}
                onClick={() => updateSetting('theme', t)}
                className={`flex-1 py-3 px-4 rounded-xl border flex items-center justify-center gap-2 capitalize transition-colors ${
                  settings.theme === t 
                    ? 'bg-primary/20 border-primary text-primary' 
                    : 'bg-slate-800/50 border-slate-700 text-slate-400 hover:bg-slate-800'
                }`}
              >
                {t === 'dark' ? <Moon size={18}/> : t === 'light' ? <Sun size={18}/> : <Monitor size={18}/>}
                {t}
              </button>
            ))}
          </div>
        </div>
      </Section>

      <Section title="Experiment Mode" icon={<ShieldAlert size={24} className="text-orange-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { id: 'easy', title: 'EASY', desc: 'Guided simulation with automatic circuit setup.' },
            { id: 'medium', title: 'MEDIUM', desc: 'Partially guided simulation with more interaction.' },
            { id: 'hard', title: 'HARD', desc: 'Manual virtual laboratory with full circuit validation.' }
          ].map(m => (
            <button 
              key={m.id}
              onClick={() => updateSetting('experimentMode', m.id)}
              className={`p-4 rounded-xl border text-left transition-colors ${
                settings.experimentMode === m.id 
                  ? 'bg-primary/20 border-primary text-primary-bright' 
                  : 'bg-slate-800/50 border-slate-700 text-slate-400 hover:bg-slate-800'
              }`}
            >
              <h4 className="font-bold mb-1">{m.title}</h4>
              <p className="text-sm opacity-80 leading-relaxed">{m.desc}</p>
            </button>
          ))}
        </div>
      </Section>

      <Section title="Sound & Alerts" icon={<Volume2 size={24} className="text-green-400" />}>
        <Toggle 
          label="Buzzer Sound" 
          desc="Play repeating virtual buzzer sound on HIGH FIRE RISK."
          checked={settings.buzzerSound}
          onChange={(val) => updateSetting('buzzerSound', val)}
        />
        <Toggle 
          label="Alert Sounds" 
          desc="Play sounds for system notifications and warnings."
          checked={settings.alertSounds}
          onChange={(val) => updateSetting('alertSounds', val)}
        />
      </Section>

      <Section title="Dashboard Preferences" icon={<Activity size={24} className="text-blue-400" />}>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <Toggle label="Show Temperature" desc="Display temperature card" checked={settings.dashboardPrefs.showTemperature} onChange={(v) => updateDashboardPref('showTemperature', v)} />
          <Toggle label="Show Smoke Level" desc="Display smoke/gas card" checked={settings.dashboardPrefs.showSmoke} onChange={(v) => updateDashboardPref('showSmoke', v)} />
          <Toggle label="Show Humidity" desc="Display humidity card" checked={settings.dashboardPrefs.showHumidity} onChange={(v) => updateDashboardPref('showHumidity', v)} />
          <Toggle label="Show AI Confidence" desc="Display AI model confidence" checked={settings.dashboardPrefs.showAiConfidence} onChange={(v) => updateDashboardPref('showAiConfidence', v)} />
          <Toggle label="Show Buzzer" desc="Display buzzer status" checked={settings.dashboardPrefs.showBuzzer} onChange={(v) => updateDashboardPref('showBuzzer', v)} />
          <Toggle label="Show IoT Connection" desc="Display IoT status" checked={settings.dashboardPrefs.showIoT} onChange={(v) => updateDashboardPref('showIoT', v)} />
        </div>
      </Section>

      <Section title="Data & History" icon={<Database size={24} className="text-purple-400" />}>
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 p-4 bg-slate-800/50 rounded-lg">
            <div>
              <p className="font-bold text-slate-200">Clear Experiment History</p>
              <p className="text-sm text-slate-400">Permanently delete all sensor and alert history.</p>
            </div>
            <button onClick={() => window.confirm('Clear history?') && clearHistory?.()} className="px-4 py-2 bg-slate-700 hover:bg-red-900/50 hover:text-red-400 transition-colors rounded-lg flex items-center gap-2 text-sm font-bold">
              <Trash2 size={16}/> Clear History
            </button>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 p-4 bg-slate-800/50 rounded-lg">
            <div>
              <p className="font-bold text-slate-200">Reset All Settings</p>
              <p className="text-sm text-slate-400">Restore default laboratory configuration.</p>
            </div>
            <button onClick={resetAllSettings} className="px-4 py-2 bg-slate-700 hover:bg-orange-900/50 hover:text-orange-400 transition-colors rounded-lg flex items-center gap-2 text-sm font-bold">
              <RotateCcw size={16}/> Reset Settings
            </button>
          </div>
        </div>
      </Section>

      <div className="text-center py-8">
        <p className="text-slate-500 font-bold">FireGuard AI</p>
        <p className="text-sm text-slate-600">AI-Based Fire & Smoke Early Warning System &bull; Version 1.0.0</p>
      </div>
    </div>
  );
};

export default Settings;
"""
write_file('src/pages/Settings.jsx', settings_code)

notifications_code = """import React, { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';
import { Bell, CheckCircle, AlertTriangle, ShieldAlert } from 'lucide-react';

const NotificationsPage = () => {
  const { notifications, markAllRead, clearNotifications } = useContext(SimulationContext);

  const getIcon = (type) => {
    switch(type) {
      case 'danger': return <ShieldAlert className="text-red-500" />;
      case 'warning': return <AlertTriangle className="text-yellow-500" />;
      case 'system': return <CheckCircle className="text-green-500" />;
      default: return <Bell className="text-blue-500" />;
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-50">Notifications</h1>
          <p className="text-slate-400">System alerts and experiment events</p>
        </div>
        <div className="flex gap-3">
          <button onClick={markAllRead} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-bold transition-colors">
            Mark all read
          </button>
          <button onClick={() => window.confirm('Clear all notifications?') && clearNotifications?.()} className="px-4 py-2 bg-red-900/20 hover:bg-red-900/40 text-red-400 rounded-lg text-sm font-bold transition-colors">
            Clear all
          </button>
        </div>
      </div>

      <div className="glass-card overflow-hidden">
        {notifications.length === 0 ? (
          <div className="p-12 text-center text-slate-500 flex flex-col items-center">
            <Bell size={48} className="mb-4 opacity-20" />
            <p className="text-lg font-medium">No notifications yet</p>
            <p className="text-sm mt-1">System events will appear here.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-700/50">
            {notifications.map(notif => (
              <div key={notif.id} className={`p-4 flex gap-4 hover:bg-slate-800/30 transition-colors ${!notif.read ? 'bg-slate-800/50' : ''}`}>
                <div className="mt-1 shrink-0">
                  {getIcon(notif.type)}
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <h4 className={`font-bold ${notif.type==='danger' ? 'text-red-400' : notif.type==='warning' ? 'text-yellow-400' : 'text-green-400'}`}>
                      {notif.title}
                    </h4>
                    <span className="text-xs text-slate-500">{new Date(notif.timestamp).toLocaleString()}</span>
                  </div>
                  <p className="text-slate-300 mt-1">{notif.message}</p>
                </div>
                {!notif.read && (
                  <div className="w-2 h-2 rounded-full bg-primary self-center shrink-0 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
export default NotificationsPage;
"""
write_file('src/pages/NotificationsPage.jsx', notifications_code)
print("Settings and Notifications pages created.")
