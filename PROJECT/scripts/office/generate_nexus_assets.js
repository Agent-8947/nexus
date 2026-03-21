const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const HTMLToDOCX = require('html-to-docx');

const OUTPUT_DIR = path.resolve(__dirname, '../../outputs');
const TEMPLATE_DIR = path.resolve(__dirname, '../../templates');

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// Helper to read templates
function getTemplate(filename) {
    const filePath = path.join(TEMPLATE_DIR, filename);
    if (!fs.existsSync(filePath)) {
        throw new Error(`Template not found: ${filePath}`);
    }
    return fs.readFileSync(filePath, 'utf8');
}

// --- СБОРКА DOCX ЧЕРЕЗ HTML-TO-DOCX ---
async function generateDOCXFromHTML(unusedContent, outputPath) {
    const inlineHtml = getTemplate('docx_template.html');

    console.log(`[*] Generating DOCX from HTML via html-to-docx...`);
    const fileBuffer = await HTMLToDOCX(inlineHtml, null, {
        table: { row: { cantSplit: true } },
        footer: true,
        pageNumber: true
    });

    fs.writeFileSync(outputPath, fileBuffer);
    console.log(`[+] Executive DOCX Generated: ${outputPath}`);
}

// --- СБОРКА HTML LANDING PAGE (LUXURY PRIME / IDE OPTIMUS) ---
function generateLandingPage(outputPath) {
    const html = getTemplate('landing_template.html');
    fs.writeFileSync(outputPath, html);
    console.log('[+] Luxury Landing Page Generated');
}

// --- СБОРКА HTML ДЛЯ СТРОГОГО PDF (RAMS STYLE) ---
function generateHTMLForPDF(outputPath) {
    const html = getTemplate('pdf_template.html');
    fs.writeFileSync(outputPath, html);
    console.log(`[+] PDF HTML Scaffold Generated`);
}

// --- MSEDGE CONVERSION ---
function createPDF(htmlPath, pdfPath) {
    try {
        const edgePaths = [
            'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        ];

        let browserExe = null;
        for (const p of edgePaths) {
            if (fs.existsSync(p)) { browserExe = p; break; }
        }

        if (browserExe) {
            const cmd = `"${browserExe}" --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="${pdfPath}" --no-pdf-header-footer "file:///${htmlPath.replace(/\\/g, '/')}"`;
            execSync(cmd, { stdio: 'ignore' });
            console.log(`[+] Executive PDF Generated: ${pdfPath}`);
        } else {
            console.log(`[-] WARNING: No chromium browser found.`);
        }
    } catch (e) {
        console.log(`[-] Error printing PDF: ${e.message}`);
    }
}

async function main() {
    console.log("=== NEXUS OMNI-GENERATOR V5.1 (OPTIMIZED) ===");

    const docxPath = path.join(OUTPUT_DIR, 'Nexus_Architecture.docx');
    const landingPath = path.join(OUTPUT_DIR, 'Nexus_Landing.html');

    const htmlPdfScaffoldPath = path.join(OUTPUT_DIR, '.tmp_pdf_scaffold.html');
    const pdfPath = path.join(OUTPUT_DIR, 'Nexus_Architecture.pdf');

    await generateDOCXFromHTML(null, docxPath);
    generateLandingPage(landingPath);

    generateHTMLForPDF(htmlPdfScaffoldPath);
    createPDF(htmlPdfScaffoldPath, pdfPath);

    if (fs.existsSync(htmlPdfScaffoldPath)) fs.unlinkSync(htmlPdfScaffoldPath);

    console.log("=== SEQUENCE COMPLETED ===");
}

main().catch(console.error);
