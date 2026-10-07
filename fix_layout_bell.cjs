const fs = require('fs');
let content = fs.readFileSync('src/components/Layout.jsx', 'utf8');

const regex = /\{\/\* Notification Bell \*\/\}\s*<button.*?<\/button>/s;

const newBell = `{/* Notification Bell */}
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
                          <div key={notif.id} className={\`p-3 border-b border-slate-700/50 hover:bg-slate-700/50 transition-colors \${!notif.read ? 'bg-slate-700/30' : ''}\`}>
                            <div className="flex items-center gap-2 mb-1">
                               {notif.type === 'danger' && <span className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>}
                               {notif.type === 'warning' && <span className="w-2 h-2 rounded-full bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.8)]"></span>}
                               {notif.type === 'system' && <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]"></span>}
                               <span className={\`text-xs font-bold \${notif.type === 'danger' ? 'text-red-400' : notif.type === 'warning' ? 'text-yellow-400' : 'text-green-400'}\`}>{notif.title}</span>
                            </div>
                            <p className="text-sm text-slate-300">{notif.message}</p>
                            <p className="text-[10px] text-slate-500 mt-1">{new Date(notif.timestamp).toLocaleTimeString()}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>`;

content = content.replace(regex, newBell);

fs.writeFileSync('src/components/Layout.jsx', content);
