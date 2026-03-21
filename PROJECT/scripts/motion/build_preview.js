const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3033;
const filePath = path.join(__dirname, '..', '..', 'outputs', 'Legal_DevOps_Pure_Hero.html');

const server = http.createServer((req, res) => {
    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(500);
            res.end(`Error loading file: ${err}`);
        } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`\n🚀 [NEXUS MOTION] PREVIEW SERVER ACTIVE`);
    console.log(`💎 Access Premium Showcase at: http://localhost:${PORT}`);
    console.log(`File served: ${filePath}\n`);
    console.log(`Press Ctrl+C to terminate session.`);
});
