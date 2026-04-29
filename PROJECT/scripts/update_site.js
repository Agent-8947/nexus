const fs = require('fs');

let docText = fs.readFileSync('extracted_docs.json', 'utf8');
let docs = JSON.parse(docText);

let jsCode = fs.readFileSync('tmp_translations.js', 'utf8');

// We can execute the JS code to get the T object
let T;
eval(jsCode.replace('const T =', 'T ='));

function parseText(text, lang) {
    let lines = text.split('\n').map(l => l.trim()).filter(l => l);
    
    let ag = [];
    let mcp = [];
    let wf = [];
    
    let mode = ''; // 'agents', 'mcp', 'workflows'
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        if (line.includes('Total agents and skills')) { mode = ''; continue; }
        if (line.includes('Total MCP connectors')) { mode = ''; continue; }
        if (line.includes('Total workflows')) { mode = ''; continue; }
        
        if (line.includes('NEXUS OS AI Agent Fleet') || line.includes('Флот AI-агентов NEXUS OS') || line.includes('Флот AI-агентів NEXUS OS')) {
            mode = 'agents';
            continue;
        }
        if (line.includes('MCP Neural Net — 22') || line.includes('MCP Neural Net — 22 зовнішні')) {
            mode = 'mcp';
            continue;
        }
        if (line.includes('24 Slash Commands') || line.includes('24 Slash-команды') || line.includes('24 Slash-Команди')) {
            mode = 'workflows';
            continue;
        }
        
        // Parsing logic based on empty lines and lengths
        if (mode === 'agents') {
            // Usually we have Title, then Description.
            // Title is short, no dot at end.
            if (line.length < 40 && !line.endsWith('.') && !line.endsWith(':') && i+1 < lines.length && lines[i+1].length > 40) {
                ag.push({
                    b: "Agent", 
                    h: line,
                    p: lines[i+1],
                    t: ""
                });
                i++; // skip description
            }
        }
        if (mode === 'mcp') {
            // Mongoose style: lowercase short words
            if (line.length < 30 && line === line.toLowerCase() && !line.includes(' ') && i+1 < lines.length && lines[i+1].length > 20) {
                mcp.push([ line, lines[i+1] ]);
                i++;
            }
        }
        if (mode === 'workflows') {
            // In Workflows, we don't have the list in the text it seems...
            // Let's print out what we see
        }
    }
    return { ag, mcp };
}

for (let lang of ['en', 'ru', 'ua']) {
    let data = parseText(docs[lang], lang);
    if (data.ag.length > 0) {
        T[lang].ag = data.ag;
        T[lang].s3 = data.ag.length.toString(); // Update agent count string
    }
    if (data.mcp.length > 0) {
        T[lang].mcp = data.mcp;
        T[lang].s2 = data.mcp.length.toString(); // Update MCP count
    }
}

// Convert back to JS:
let newJsCode = "const T = " + JSON.stringify(T, null, 4) + ";";
fs.writeFileSync('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', newJsCode);
console.log("Updated JS written.");
