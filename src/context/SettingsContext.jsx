import React, { createContext, useState, useEffect } from 'react';

export const SettingsContext = createContext();

export const SettingsProvider = ({ children }) => {
  const defaultSettings = {
    theme: 'dark', // dark, light, system
    experimentMode: 'easy', // easy, medium, hard
    buzzerSound: true,
    alertSounds: true,
    volume: 0.7,
    simulationSpeed: 'normal',
    autoStart: false,
    sensorAnimations: true,
    circuitAnimations: true,
    requireValidation: true,
    reduceAnimations: false,
    highContrast: false,
    largerText: false,
    dashboardPrefs: {
      showTemperature: true,
      showSmoke: true,
      showHumidity: true,
      showAiConfidence: true,
      showBuzzer: true,
      showIoT: true,
      showTrends: true
    }
  };

  const [settings, setSettings] = useState(() => {
    try {
      const saved = localStorage.getItem('fireguard_settings');
      return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
    } catch (e) {
      console.error("Failed to parse settings from localStorage:", e);
      return defaultSettings;
    }
  });

  useEffect(() => {
    localStorage.setItem('fireguard_settings', JSON.stringify(settings));
    
    // Apply theme
    let activeTheme = settings.theme;
    if (activeTheme === 'system') {
      activeTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    if (activeTheme === 'light') {
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
    }
  }, [settings]);

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const updateDashboardPref = (key, value) => {
    setSettings(prev => ({
      ...prev,
      dashboardPrefs: { ...prev.dashboardPrefs, [key]: value }
    }));
  };

  const resetAllSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings(defaultSettings);
    }
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, updateDashboardPref, resetAllSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};
