const fs = require('fs');

// 1. Update vite.config.js
let viteConfig = fs.readFileSync('vite.config.js', 'utf8');
viteConfig = viteConfig.replace(
  'export default defineConfig({',
  `export default defineConfig({\n  base: '/Fire-Guard-AI-ES-and-IOT/',`
);
fs.writeFileSync('vite.config.js', viteConfig);

// 2. Update App.jsx to use HashRouter
let appJsx = fs.readFileSync('src/App.jsx', 'utf8');
appJsx = appJsx.replace("import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';", 
                        "import { HashRouter as Router, Routes, Route } from 'react-router-dom';");
fs.writeFileSync('src/App.jsx', appJsx);

// 3. Update VirtualCircuit.jsx image paths
let vcJsx = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');
vcJsx = vcJsx.replace(/href="\/images\//g, 'href={`${import.meta.env.BASE_URL}images/');
// Since they are strings, wait! Replacing href="/images/x.jpg" with href={`${...}x.jpg`}
// Need to change the attribute quotes as well!
// Let's do a better replace:
vcJsx = vcJsx.replace(/href="\/images\/(.*?)"/g, "href={`${import.meta.env.BASE_URL}images/$1`}");
fs.writeFileSync('src/pages/VirtualCircuit.jsx', vcJsx);

// 4. Update Guidelines.jsx image paths
let glJsx = fs.readFileSync('src/pages/Guidelines.jsx', 'utf8');
glJsx = glJsx.replace(/src="\/images\/(.*?)"/g, "src={`${import.meta.env.BASE_URL}images/$1`}");
fs.writeFileSync('src/pages/Guidelines.jsx', glJsx);

console.log("Fixes applied.");
