const fs = require('fs');
const path = require('path');
const React = require('react');
const { Document, Page, Text, View, StyleSheet, Font, renderToFile } = require('@react-pdf/renderer');

// --- FONTS (Using URL for Inter as per template) ---
// Font.register({
//     family: 'Inter',
//     fonts: [
//         { src: 'https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2', fontWeight: 400 },
//         { src: 'https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuI6fAZ9hiA.woff2', fontWeight: 500 },
//         { src: 'https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuFuYAZ9hiA.woff2', fontWeight: 700 },
//     ],
// });

// --- STYLING (Based on Luxury Technical Aesthetic) ---
const styles = StyleSheet.create({
    page: {
        padding: 40,
        backgroundColor: '#F2F2F2',
        fontFamily: 'Helvetica',
        color: '#222222',
        position: 'relative',
        height: '100%',
    },
    coverPage: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'flex-start',
        height: '100%',
    },
    panel: {
        backgroundColor: '#E8E8E8',
        borderRadius: 20,
        padding: 30,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.5)',
        marginBottom: 20,
        width: '100%',
    },
    luxuryTag: {
        fontSize: 9,
        fontWeight: 700,
        color: '#FF5E00',
        textTransform: 'uppercase',
        letterSpacing: 4,
        marginBottom: 15,
    },
    h1: {
        fontSize: 48,
        fontWeight: 700,
        marginBottom: 5,
        letterSpacing: -2,
        textTransform: 'uppercase',
    },
    h2: {
        fontSize: 18,
        fontWeight: 500,
        color: 'rgba(34, 34, 34, 0.6)',
        letterSpacing: -0.5,
    },
    indicator: {
        width: 100,
        height: 6,
        borderRadius: 3,
        backgroundColor: '#FF5E00',
        marginVertical: 30,
    },
    metaRow: {
        flexDirection: 'row',
        gap: 30,
        marginTop: 10,
    },
    metaBox: {
        flexDirection: 'column',
    },
    metaLabel: {
        fontSize: 8,
        fontWeight: 700,
        color: 'rgba(34, 34, 34, 0.4)',
        textTransform: 'uppercase',
        marginBottom: 2,
    },
    metaValue: {
        fontSize: 12,
        fontWeight: 700,
    },
    sectionTitle: {
        fontSize: 16,
        fontWeight: 700,
        color: '#222222',
        borderBottomWidth: 3,
        borderBottomColor: '#C2C2C2',
        paddingBottom: 5,
        marginTop: 20,
        marginBottom: 15,
        textTransform: 'uppercase',
        letterSpacing: -0.5,
    },
    text: {
        fontSize: 12,
        fontWeight: 400,
        lineHeight: 1.5,
        marginBottom: 10,
    },
    table: {
        marginTop: 15,
        backgroundColor: '#E8E8E8',
        borderRadius: 10,
        overflow: 'hidden',
    },
    tableHeader: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomColor: '#C2C2C2',
        backgroundColor: '#E8E8E8',
        padding: 12,
    },
    tableRow: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomColor: '#C2C2C2',
        padding: 12,
    },
    headerCell: {
        fontSize: 8,
        fontWeight: 700,
        textTransform: 'uppercase',
        flex: 1,
    },
    cell: {
        fontSize: 11,
        fontWeight: 500,
        flex: 1,
    },
    footer: {
        position: 'absolute',
        bottom: 25,
        left: 40,
        right: 40,
        fontSize: 8,
        fontWeight: 700,
        color: 'rgba(34, 34, 34, 0.4)',
        textTransform: 'uppercase',
        letterSpacing: 2,
    }
});

// --- COMPONENTS ---
const MetaBox = ({ label, value, color }) => React.createElement(View, { style: styles.metaBox },
    React.createElement(Text, { style: styles.metaLabel }, label),
    React.createElement(Text, { style: [styles.metaValue, color ? { color } : {}] }, value)
);

const PdfDocument = () => React.createElement(Document, {},
    // PAGE 1: COVER
    React.createElement(Page, { size: "A4", style: [styles.page, styles.coverPage] },
        React.createElement(View, { style: styles.panel },
            React.createElement(Text, { style: styles.luxuryTag }, "NEXUS // STRATEGIC ASSET"),
            React.createElement(Text, { style: styles.h1 }, "IDE OPTIMUS"),
            React.createElement(Text, { style: styles.h2 }, "High-Performance Messaging Architecture"),
            React.createElement(View, { style: styles.indicator }),
            React.createElement(View, { style: styles.metaRow },
                React.createElement(MetaBox, { label: "VERSION", value: "6.0.4-STABLE" }),
                React.createElement(MetaBox, { label: "STATUS", value: "ACTIVE [PRODUCTION]", color: "#AEC6A6" })
            )
        )
    ),

    // PAGE 2: ARCHITECTURE
    React.createElement(Page, { size: "A4", style: styles.page },
        React.createElement(Text, { style: styles.sectionTitle }, "01. Phase: Analysis & Objectives"),
        React.createElement(View, { style: [styles.panel, { padding: 20 }] },
            React.createElement(Text, { style: [styles.text, { fontWeight: 700, fontSize: 14 }] }, "The 100k Challenge"),
            React.createElement(Text, { style: styles.text }, "IDE OPTIMUS is engineered to handle massive throughput (100,000 msg/s) with sub-millisecond latency on standard hardware.")
        ),

        React.createElement(Text, { style: styles.sectionTitle }, "02. Stack Matrix"),
        React.createElement(View, { style: { flexDirection: 'row', gap: 15 } },
            React.createElement(View, { style: [styles.panel, { flex: 1, padding: 15 }] },
                React.createElement(Text, { style: [styles.luxuryTag, { fontSize: 8 }] }, "CORE ENGINE"),
                React.createElement(Text, { style: [styles.text, { fontWeight: 700 }] }, "Rust + Tokio"),
                React.createElement(Text, { style: [styles.text, { fontSize: 10, color: 'rgba(34,34,34,0.7)' }] }, "Zero GC pauses, thread safety.")
            ),
            React.createElement(View, { style: [styles.panel, { flex: 1, padding: 15 }] },
                React.createElement(Text, { style: [styles.luxuryTag, { fontSize: 8, color: '#2363EB' }] }, "ORCHESTRATION"),
                React.createElement(Text, { style: [styles.text, { fontWeight: 700 }] }, "Python/Go Hybrid"),
                React.createElement(Text, { style: [styles.text, { fontSize: 10, color: 'rgba(34,34,34,0.7)' }] }, "FastHTML Dashboards.")
            )
        ),

        React.createElement(Text, { style: styles.footer }, "STRICTLY CONFIDENTIAL // IDE OPTIMUS PROPRIETARY")
    )
);

async function generate() {
    const outputPath = path.resolve(__dirname, '../../outputs/Nexus_Executive_V3.pdf');
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    console.log(`[*] Building PDF V3 via @react-pdf/renderer...`);
    await renderToFile(React.createElement(PdfDocument), outputPath);
    console.log(`[+] Luxury PDF Generated: ${outputPath}`);
}

generate().catch(err => {
    console.error('[-] PDF V3 Generation Failed:', err);
    process.exit(1);
});
