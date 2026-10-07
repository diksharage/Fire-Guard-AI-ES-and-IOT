import React, { useContext } from 'react';
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
