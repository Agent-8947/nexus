const fs = require('fs');
const path = require('path');
const React = require('react');
const { Document, Page, Text, View, StyleSheet, Font, renderToFile } = require('@react-pdf/renderer');

// --- STYLING ---
const styles = StyleSheet.create({
    page: { padding: 40, backgroundColor: '#ffffff', fontFamily: 'Helvetica', color: '#1a1a1a' },
    header: { marginBottom: 30, borderBottomWidth: 1, borderBottomColor: '#eeeeee', paddingBottom: 20 },
    version: { fontSize: 8, color: '#666666', marginBottom: 5, fontFamily: 'Courier' },
    h1: { fontSize: 40, fontWeight: 700, letterSpacing: -1 },
    sub: { fontSize: 14, color: '#666666', marginTop: 5 },
    section: { marginBottom: 25 },
    sectionTitle: { fontSize: 14, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 1, color: '#000000', marginBottom: 15, borderLeftWidth: 3, borderLeftColor: '#ff3b30', paddingLeft: 10 },
    grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 15 },
    node: { width: '47%', padding: 15, borderWeight: 1, borderColor: '#eeeeee', borderWidth: 1, marginBottom: 10 },
    nodeBadge: { fontSize: 8, textTransform: 'uppercase', color: '#666666', marginBottom: 5 },
    nodeTitle: { fontSize: 12, fontWeight: 700, marginBottom: 5 },
    nodeText: { fontSize: 10, lineHeight: 1.4, color: '#444444' },
    footer: { position: 'absolute', bottom: 30, left: 40, right: 40, fontSize: 8, color: '#999999', flexDirection: 'row', justifyContent: 'space-between', borderTopWidth: 1, borderTopColor: '#eeeeee', paddingTop: 10 }
});

const Node = ({ badge, title, text }) => (
    React.createElement(View, { style: styles.node },
        React.createElement(Text, { style: styles.nodeBadge }, badge),
        React.createElement(Text, { style: styles.nodeTitle }, title),
        React.createElement(Text, { style: styles.nodeText }, text)
    )
);

const PdfDocument = () => React.createElement(Document, {},
    React.createElement(Page, { size: "A4", style: styles.page },
        // HEADER
        React.createElement(View, { style: styles.header },
            React.createElement(Text, { style: styles.version }, "SYSTEM_BOOT_SUCCESS_v2.1 // NEXUS_CORE"),
            React.createElement(Text, { style: styles.h1 }, "NEXUS GRAND VISION"),
            React.createElement(Text, { style: styles.sub }, "Technical Intelligence Core & Strategic Asset Report")
        ),

        // SECTION 01
        React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, "01 Architecture"),
            React.createElement(View, { style: styles.grid },
                React.createElement(Node, { badge: "Kernel", title: "Supervisor Hub", text: "Central asynchronous dispatcher. Manages worker pool and delegates execution via intelligent channels." }),
                React.createElement(Node, { badge: "Bridge", title: "Contextual I/O", text: "Protocol bridge (MCP) providing atomic access to files, repositories, and databases." })
            )
        ),

        // SECTION 02
        React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, "02 Protection"),
            React.createElement(View, { style: styles.grid },
                React.createElement(Node, { badge: "Security", title: "Code Entropy Guard", text: "Monitors code degradation. Intellectual filter for hallucination suppression in autonomous agents." }),
                React.createElement(Node, { badge: "Health", title: "Self-Healing Logic", text: "Automatic environment reparation. Error tracing and real-time patching in isolated circuits." })
            )
        ),

        // SECTION 03
        React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, "03 Archetypes"),
            React.createElement(View, { style: styles.grid },
                React.createElement(Node, { badge: "The Auditor", title: "The Security Mind", text: "Specialized role for vulnerability discovery and absolute Stack Purity." }),
                React.createElement(Node, { badge: "The Engineer", title: "The Builder", text: "Aggressive feature deployment and performance optimization." }),
                React.createElement(Node, { badge: "The Visionary", title: "Strategic Insight", text: "Long-term trajectory planning based on NEXUS analytics." })
            )
        ),

        React.createElement(View, { style: styles.footer },
            React.createElement(Text, null, "ID: IDE-OPTIMUS-2026"),
            React.createElement(Text, null, "CONFIDENTIAL // FORM: NEXUS_DOC_V1")
        )
    ),

    React.createElement(Page, { size: "A4", style: styles.page },
        // SECTION 04
        React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, "04 Skill DNA"),
            React.createElement(View, { style: styles.grid },
                React.createElement(Node, { badge: "Visual", title: "Motion Engine", text: "GSAP timelines and GLSL shaders for precision visual feedback." }),
                React.createElement(Node, { badge: "System", title: "Turbo Boost", text: "RAM and CPU optimization. Ultra-fast garbage collection and priority management." }),
                React.createElement(Node, { badge: "Global", title: "840+ Skills", text: "Distributed Antigravity knowledge library available for hot-loading." })
            )
        ),

        // SECTION 05
        React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, "05 Roadmap"),
            React.createElement(View, { style: styles.grid },
                React.createElement(Node, { badge: "2026 Q3", title: "Adaptive Agent Swarms", text: "Transition from static delegation to dynamic collaboration with shared project state." }),
                React.createElement(Node, { badge: "2026 Q4", title: "Autonomous CI/CD Guard", text: "Direct pipeline integration for autonomous build repair and regression fixing." }),
                React.createElement(Node, { badge: "2027 Q1", title: "Reasoning Audit Layer", text: "High-fidelity visualization of agent reasoning chains for absolute transparency." }),
            )
        ),

        React.createElement(View, { style: styles.footer },
            React.createElement(Text, null, "NEXUS GRAND VISION // PAGE 02"),
            React.createElement(Text, null, "OPERATIONAL STATUS: ACTIVE")
        )
    )
);

async function generate() {
    const outputPath = path.resolve(__dirname, '../../outputs/NEXUS_GRAND_VISION_v2.pdf');
    console.log(`[*] Generating Grand Vision PDF...`);
    await renderToFile(React.createElement(PdfDocument), outputPath);
    console.log(`[+] PDF Generated: ${outputPath}`);
}

generate().catch(err => {
    console.error('[-] PDF Generation Failed:', err);
    process.exit(1);
});
