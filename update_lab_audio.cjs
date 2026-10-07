const fs = require('fs');
let content = fs.readFileSync('src/pages/ExperimentLab.jsx', 'utf8');

// Add VolumeX to lucide-react imports if missing
if (!content.includes('VolumeX')) {
    content = content.replace('Volume2', 'Volume2, VolumeX');
}

// Extract isSoundEnabled from context
content = content.replace('const { temperature, setTemperature', 'const { isSoundEnabled, setIsSoundEnabled, temperature, setTemperature');

// Add the Volume toggle button
const resetBtn = `{isRunning && (
            <button onClick={handleReset} className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors shadow-lg" title="Reset Experiment">
              <RotateCcw size={20} />
            </button>
          )}`;

const newBtns = `{isRunning && (
            <button onClick={handleReset} className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors shadow-lg" title="Reset Experiment">
              <RotateCcw size={20} />
            </button>
          )}
          <button 
            onClick={() => setIsSoundEnabled(!isSoundEnabled)} 
            className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors shadow-lg" 
            title={isSoundEnabled ? "Mute Buzzer" : "Unmute Buzzer"}
          >
            {isSoundEnabled ? <Volume2 size={20} className="text-green-400" /> : <VolumeX size={20} className="text-slate-500" />}
          </button>`;

if (content.includes(resetBtn)) {
   content = content.replace(resetBtn, newBtns);
} else {
   console.log("Could not find resetBtn block");
}

fs.writeFileSync('src/pages/ExperimentLab.jsx', content);
