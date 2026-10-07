const fs = require('fs');

let vcJsx = fs.readFileSync('src/pages/VirtualCircuit.jsx', 'utf8');
vcJsx = vcJsx.replace('href="/images/esp8266.jpg"', 'href={`${import.meta.env.BASE_URL}images/esp8266.jpg`}');
vcJsx = vcJsx.replace('href="/images/dht11.jpg"', 'href={`${import.meta.env.BASE_URL}images/dht11.jpg`}');
vcJsx = vcJsx.replace('href="/images/resistor.jpg"', 'href={`${import.meta.env.BASE_URL}images/resistor.jpg`}');
fs.writeFileSync('src/pages/VirtualCircuit.jsx', vcJsx);

let glJsx = fs.readFileSync('src/pages/Guidelines.jsx', 'utf8');
glJsx = glJsx.replace('src="/images/esp8266.jpg"', 'src={`${import.meta.env.BASE_URL}images/esp8266.jpg`}');
glJsx = glJsx.replace('src="/images/dht11.jpg"', 'src={`${import.meta.env.BASE_URL}images/dht11.jpg`}');
glJsx = glJsx.replace('src="/images/resistor.jpg"', 'src={`${import.meta.env.BASE_URL}images/resistor.jpg`}');
fs.writeFileSync('src/pages/Guidelines.jsx', glJsx);
