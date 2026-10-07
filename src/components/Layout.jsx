import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { Flame, LayoutDashboard, Cpu, FlaskConical, BrainCircuit, Wifi, BarChart3, History, Info, Menu, X, Bell, BookOpen, Moon, Sun } from 'lucide-react';
import { useContext } from 'react';
import { SimulationContext } from '../context/SimulationContext';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
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

  const { riskLevel, notifications = [], markAllRead } = useContext(SimulationContext);
  const [showNotifications, setShowNotifications] = useState(false);
  const unreadCount = notifications.filter(n => !n.read).length;

  const navGroups = [
    {
      group: "MAIN",
      items: [
        { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
      ]
    },
    {
      group: "EXPERIMENT",
      items: [
        { path: '/circuit', label: 'Virtual Circuit', icon: <Cpu size={20} /> },
        { path: '/lab', label: 'Experiment Lab', icon: <FlaskConical size={20} /> },
        { path: '/guidelines', label: 'Experiment Guidelines', icon: <BookOpen size={20} /> },
      ]
    },
    {
      group: "INTELLIGENCE & MONITORING",
      items: [
        { path: '/ai', label: 'AI Classifier', icon: <BrainCircuit size={20} /> },
        { path: '/iot', label: 'IoT Monitoring', icon: <Wifi size={20} /> },
        { path: '/analytics', label: 'Sensor Analytics', icon: <BarChart3 size={20} /> },
        { path: '/history', label: 'History', icon: <History size={20} /> },
      ]
    },
    {
      group: "SYSTEM",
      items: [
        { path: '/about', label: 'About System', icon: <Info size={20} /> },
      ]
    }
  ];

  return (
    <div className="flex h-screen bg-darker overflow-hidden font-sans transition-colors duration-300">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-sidebar border-r border-slate-700 transition-transform duration-300 md:relative md:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center justify-between p-4 border-b border-slate-700 h-16 shrink-0">
          <div className="flex items-center gap-2 text-primary font-bold text-xl">
            <Flame className="text-primary animate-pulse" />
            FireGuard AI
          </div>
          <button onClick={() => setSidebarOpen(false)} className="md:hidden text-slate-400 hover:text-slate-50 transition-colors">
            <X size={24} />
          </button>
        </div>
        <nav className="p-3 space-y-6 overflow-y-auto h-[calc(100vh-4rem)]">
          {navGroups.map((group, gIdx) => (
            <div key={gIdx}>
              {group.group && <div className="px-3 mb-2 text-[10px] text-slate-500 uppercase font-bold tracking-widest">{group.group}</div>}
              <div className="space-y-1">
                {group.items.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={() => setSidebarOpen(false)}
                    className={({ isActive }) => 
                      `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                        isActive ? 'bg-primary/10 text-primary font-medium' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                      }`
                    }
                  >
                    {item.icon}
                    {item.label}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8 bg-card/50 backdrop-blur-sm border-b border-slate-700 shrink-0 transition-colors duration-300">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebarOpen(true)} className="md:hidden text-slate-400 hover:text-slate-50 transition-colors">
              <Menu size={24} />
            </button>
            <div className="hidden sm:flex flex-col">
              <h1 className="text-sm font-semibold text-slate-200">Virtual Fire & Smoke Early Warning Laboratory</h1>
              <span className="text-xs text-slate-400">Simulation Environment</span>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="hidden md:flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${riskLevel === 2 ? 'bg-red-400' : riskLevel === 1 ? 'bg-yellow-400' : 'bg-green-400'}`}></span>
                <span className={`relative inline-flex rounded-full h-3 w-3 ${riskLevel === 2 ? 'bg-red-500' : riskLevel === 1 ? 'bg-yellow-500' : 'bg-green-500'}`}></span>
              </span>
              <span className="text-sm font-medium text-slate-300">
                {riskLevel === 2 ? 'HIGH RISK' : riskLevel === 1 ? 'WARNING' : 'NORMAL'}
              </span>
            </div>
            
            <div className="flex items-center gap-2 sm:gap-4">
              {/* Notification Bell */}
              <div className="relative">
                <button 
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="relative text-slate-400 hover:text-primary transition-colors p-2 rounded-full hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <Bell size={20} />
                  {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] text-slate-50 font-bold border-2 border-card">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
                </button>
                
                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-72 sm:w-80 bg-slate-800 border border-slate-700 rounded-lg shadow-xl z-50 overflow-hidden">
                    <div className="p-3 border-b border-slate-700 flex justify-between items-center bg-slate-900">
                      <h3 className="font-bold text-slate-100">Notifications</h3>
                      {unreadCount > 0 && (
                        <button onClick={markAllRead} className="text-xs text-primary hover:text-primary-bright transition">Mark all as read</button>
                      )}
                    </div>
                    <div className="max-h-96 overflow-y-auto">
                      {notifications.length === 0 ? (
                        <div className="p-4 text-center text-slate-400 text-sm">No notifications</div>
                      ) : (
                        notifications.map(notif => (
                          <div key={notif.id} className={`p-3 border-b border-slate-700/50 hover:bg-slate-700/50 transition-colors ${!notif.read ? 'bg-slate-700/30' : ''}`}>
                            <div className="flex items-center gap-2 mb-1">
                               {notif.type === 'danger' && <span className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>}
                               {notif.type === 'warning' && <span className="w-2 h-2 rounded-full bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.8)]"></span>}
                               {notif.type === 'system' && <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]"></span>}
                               <span className={`text-xs font-bold ${notif.type === 'danger' ? 'text-red-400' : notif.type === 'warning' ? 'text-yellow-400' : 'text-green-400'}`}>{notif.title}</span>
                            </div>
                            <p className="text-sm text-slate-300">{notif.message}</p>
                            <p className="text-[10px] text-slate-500 mt-1">{new Date(notif.timestamp).toLocaleTimeString()}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Theme Toggle */}
              <button 
                onClick={toggleTheme} 
                title={theme === 'dark' ? "Switch to Light Mode" : "Switch to Dark Mode"}
                className="text-slate-400 hover:text-primary transition-colors p-2 rounded-full hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary flex items-center justify-center"
              >
                {theme === 'dark' ? <Moon size={20} /> : <Sun size={20} />}
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};
export default Layout;
