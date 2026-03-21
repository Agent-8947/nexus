const fs = require('fs');
const path = require('path');
const React = require('react');
const { Document, Page, Text, View, StyleSheet, Font, renderToFile } = require('@react-pdf/renderer');

// --- STYLING (Deep Dark Nexus Theme) ---
const styles = StyleSheet.create({
    page: {
        padding: 0,
        backgroundColor: '#0F1115',
        fontFamily: 'Helvetica',
        color: '#FFFFFF',
    },
    slideCover: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 40,
    },
    nexusLogo: {
        fontSize: 64,
        fontWeight: 'bold',
        letterSpacing: -2,
        color: '#FF5E00',
        marginBottom: 10,
    },
    nexusSubtitle: {
        fontSize: 20,
        color: 'rgba(255, 255, 255, 0.6)',
        letterSpacing: 4,
        textTransform: 'uppercase',
        marginBottom: 40,
    },
    accentLine: {
        width: 120,
        height: 4,
        backgroundColor: '#FF5E00',
        borderRadius: 2,
        marginBottom: 30,
    },
    versionBadge: {
        backgroundColor: 'rgba(255, 94, 0, 0.1)',
        borderWidth: 1,
        borderColor: '#FF5E00',
        padding: 4,
        paddingHorizontal: 12,
        borderRadius: 4,
    },
    versionText: {
        fontSize: 10,
        color: '#FF5E00',
        fontWeight: 'bold',
    },
    slideContent: {
        padding: 40,
        height: '100%',
    },
    slideHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        marginBottom: 30,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255, 255, 255, 0.1)',
        paddingBottom: 10,
    },
    slideTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    slideNumber: {
        fontSize: 12,
        color: 'rgba(255, 255, 255, 0.3)',
    },
    grid: {
        flexDirection: 'row',
        gap: 20,
        flexWrap: 'wrap',
    },
    panel: {
        backgroundColor: '#1A1D23',
        borderRadius: 12,
        padding: 20,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.05)',
    },
    panelTitle: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#FF5E00',
        marginBottom: 10,
        textTransform: 'uppercase',
    },
    panelText: {
        fontSize: 11,
        lineHeight: 1.5,
        color: 'rgba(255, 255, 255, 0.8)',
    },
    table: {
        marginTop: 10,
        width: '100%',
    },
    tableRow: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255, 255, 255, 0.05)',
        paddingVertical: 10,
    },
    tableCellLabel: {
        width: '40%',
        fontSize: 10,
        color: 'rgba(255, 255, 255, 0.4)',
        textTransform: 'uppercase',
    },
    tableCellValue: {
        width: '60%',
        fontSize: 12,
        color: '#FFFFFF',
        fontWeight: 'bold',
    },
    footer: {
        position: 'absolute',
        bottom: 20,
        left: 40,
        right: 40,
        flexDirection: 'row',
        justifyContent: 'space-between',
        fontSize: 8,
        color: 'rgba(255, 255, 255, 0.2)',
        textTransform: 'uppercase',
        letterSpacing: 1,
    }
});

// --- HELPER WRAPPERS ---
const SlideHeader = ({ title, number }) => React.createElement(View, { style: styles.slideHeader },
    React.createElement(Text, { style: styles.slideTitle }, title),
    React.createElement(Text, { style: styles.slideNumber }, number)
);

const Footer = () => React.createElement(View, { style: styles.footer },
    React.createElement(Text, {}, "NEXUS SYSTEM // 2026 ARCHITECTURE"),
    React.createElement(Text, {}, "STRICTLY CONFIDENTIAL")
);

const NexusPresentation = () => React.createElement(Document, {},
    // Slide 1: Cover
    React.createElement(Page, { size: "A4", orientation: "landscape", style: styles.page },
        React.createElement(View, { style: styles.slideCover },
            React.createElement(Text, { style: styles.nexusLogo }, "NEXUS PRIME"),
            React.createElement(Text, { style: styles.nexusSubtitle }, "Agnostic Architecture Engine"),
            React.createElement(View, { style: styles.accentLine }),
            React.createElement(View, { style: styles.versionBadge },
                React.createElement(Text, { style: styles.versionText }, "v2026.1 // HYBRID CORE")
            )
        ),
        React.createElement(Footer)
    ),

    // Slide 2: Vision
    React.createElement(Page, { size: "A4", orientation: "landscape", style: styles.page },
        React.createElement(View, { style: styles.slideContent },
            React.createElement(SlideHeader, { title: "01. The Architectural Vision", number: "02/05" }),
            React.createElement(View, { style: styles.grid },
                React.createElement(View, { style: [styles.panel, { width: 330 }] },
                    React.createElement(Text, { style: styles.panelTitle }, "Performance Target"),
                    React.createElement(Text, { style: styles.panelText }, "Engineering 100k msg/s on 6GB RAM. IPC-optimized.")
                ),
                React.createElement(View, { style: [styles.panel, { width: 330 }] },
                    React.createElement(Text, { style: styles.panelTitle }, "Agnostic Core"),
                    React.createElement(Text, { style: styles.panelText }, "Dynamic Tool Selection (Rust/Python/Go) based on task.")
                )
            ),
            React.createElement(View, { style: [styles.panel, { marginTop: 20, width: 680 }] },
                React.createElement(Text, { style: styles.panelTitle }, "Key Metric Matrix"),
                React.createElement(View, { style: styles.table },
                    React.createElement(View, { style: styles.tableRow },
                        React.createElement(Text, { style: styles.tableCellLabel }, "Throughput"),
                        React.createElement(Text, { style: styles.tableCellValue }, "100k msg/s [VALIDATED]")
                    ),
                    React.createElement(View, { style: styles.tableRow },
                        React.createElement(Text, { style: styles.tableCellLabel }, "Memory Footprint"),
                        React.createElement(Text, { style: styles.tableCellValue }, "~480MB Total Load")
                    )
                )
            )
        ),
        React.createElement(Footer)
    ),

    // Slide 3: Stack
    React.createElement(Page, { size: "A4", orientation: "landscape", style: styles.page },
        React.createElement(View, { style: styles.slideContent },
            React.createElement(SlideHeader, { title: "02. Core Hybrid Stack", number: "03/05" }),
            React.createElement(View, { style: styles.grid },
                React.createElement(View, { style: [styles.panel, { width: 220 }] },
                    React.createElement(Text, { style: styles.panelTitle }, "Frontend"),
                    React.createElement(Text, { style: styles.panelText }, "Astro v5 + Hono\nEdge Rendering")
                ),
                React.createElement(View, { style: [styles.panel, { width: 220 }] },
                    React.createElement(Text, { style: styles.panelTitle }, "Intelligence"),
                    React.createElement(Text, { style: styles.panelText }, "Python 3.13\nClaude 3.7 Sonnet")
                ),
                React.createElement(View, { style: [styles.panel, { width: 220 }] },
                    React.createElement(Text, { style: styles.panelTitle }, "Infra"),
                    React.createElement(Text, { style: styles.panelText }, "Named Pipes (IPC)\nSQLite (Local)")
                )
            )
        ),
        React.createElement(Footer)
    )
);

async function generate() {
    const outputPath = path.resolve(__dirname, '../../outputs/Nexus_Presentation_V3.pdf');
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    console.log(`[*] Building Presentation V3 via @react-pdf/renderer...`);
    await renderToFile(React.createElement(NexusPresentation), outputPath);
    console.log(`[+] Executive Presentation Generated: ${outputPath}`);
}

generate().catch(err => {
    console.error('[-] Presentation Generation Failed:', err);
    process.exit(1);
});
