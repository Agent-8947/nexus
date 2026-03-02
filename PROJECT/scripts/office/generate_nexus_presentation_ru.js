const React = require('react');
const { PDFDownloadLink, Document, Page, Text, View, StyleSheet, Image, Font, Canvas, Svg, Path, Rect, Circle, G, Link } = require('@react-pdf/renderer');
const fs = require('fs');
const path = require('path');

// Register Cyrillic-support font (Roboto)
Font.register({
    family: 'Roboto',
    fonts: [
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-regular-webfont.ttf' },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf', fontWeight: 'bold' },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-italic-webfont.ttf', fontStyle: 'italic' },
    ],
});

// Styles for "Dieter Rams / Rational Layout" (Braun Manual Aesthetics)
const styles = StyleSheet.create({
    page: {
        padding: 60, // Generous margins
        backgroundColor: '#F2F2F2', // braun.bg
        color: '#222222', // braun.text
        fontFamily: 'Roboto',
    },
    // Top Info Bar
    topBar: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        borderBottomWidth: 0.5,
        borderBottomColor: '#222222',
        paddingBottom: 10,
        marginBottom: 80,
    },
    labelTiny: {
        fontSize: 6,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: 2,
    },
    // Main Content Layout (Grid-based)
    mainTitle: {
        fontSize: 48,
        fontWeight: 'bold',
        lineHeight: 1,
        letterSpacing: -2,
        marginBottom: 60,
    },
    contentGrid: {
        flexDirection: 'row',
        gap: 40,
    },
    leftCol: {
        flex: 1,
    },
    rightCol: {
        flex: 1.5,
    },
    sectionLabel: {
        fontSize: 7,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: 3,
        marginBottom: 20,
    },
    subTitle: {
        fontSize: 16,
        lineHeight: 1.4,
        color: 'rgba(34, 34, 34, 0.8)',
    },
    // Module Components
    module: {
        marginBottom: 50,
        borderTopWidth: 0.5,
        borderTopColor: '#222222',
        paddingTop: 15,
    },
    moduleNum: {
        fontSize: 8,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    moduleTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 15,
    },
    moduleText: {
        fontSize: 10,
        lineHeight: 1.6,
        color: 'rgba(34, 34, 34, 0.7)',
    },
    caseStudy: {
        marginTop: 20,
        backgroundColor: '#E8E8E8', // braun.panel
        padding: 20,
    },
    caseLabel: {
        fontSize: 6,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        color: '#FF5E00', // braun.orange (minimal use)
        marginBottom: 8,
    },
    caseText: {
        fontSize: 9,
        lineHeight: 1.4,
        fontWeight: 'medium',
    },
    // Footer System
    footer: {
        marginTop: 'auto',
        borderTopWidth: 0.5,
        borderTopColor: '#222222',
        paddingTop: 10,
        flexDirection: 'row',
        justifyContent: 'space-between',
    }
});

const ModuleItem = ({ num, title, desc, practice }) => (
    React.createElement(View, { style: styles.module },
        React.createElement(Text, { style: styles.moduleNum }, num),
        React.createElement(Text, { style: styles.moduleTitle }, title),
        React.createElement(Text, { style: styles.moduleText }, desc),
        React.createElement(View, { style: styles.caseStudy },
            React.createElement(Text, { style: styles.caseLabel }, "FUNCTIONAL_INSTANCE"),
            React.createElement(Text, { style: styles.caseText }, practice)
        )
    )
);

const NexusPresentation = () => React.createElement(Document, {
    title: "NEXUS - Dieter Rams Rationality",
    author: "NEXUS AI | ARCHITECT OF SENSES",
},
    // Page 1: Principles & Core
    React.createElement(Page, { size: "A4", style: styles.page },
        React.createElement(View, { style: styles.topBar },
            React.createElement(Text, { style: styles.labelTiny }, "NEXUS_SYSTEM_DOC // V1.0"),
            React.createElement(Text, { style: styles.labelTiny }, "REF: 1965-GRID-A")
        ),

        React.createElement(Text, { style: styles.mainTitle }, "NEXUS:\nОБЪЕКТИВНАЯ\nРЕАЛЬНОСТЬ."),

        React.createElement(View, { style: styles.contentGrid },
            React.createElement(View, { style: styles.leftCol },
                React.createElement(Text, { style: styles.sectionLabel }, "ВВЕДЕНИЕ"),
                React.createElement(Text, { style: styles.subTitle },
                    "Дисциплина формы как отражение дисциплины кода. Мы создаем инструменты, которые не мешают думать."
                )
            ),
            React.createElement(View, { style: styles.rightCol },
                React.createElement(ModuleItem, {
                    num: "01",
                    title: "Рациональный Кодинг",
                    desc: "Отсутствие визуального и логического шума. Код должен быть прозрачен и понятен так же, как хороший промышленный дизайн.",
                    practice: "Кейс: Сборка систем мониторинга через Named Pipes. Прямая линия данных без лишних абстракций."
                })
            )
        ),

        React.createElement(View, { style: styles.footer },
            React.createElement(Text, { style: styles.labelTiny }, "NEXUS PRIME"),
            React.createElement(Text, { style: styles.labelTiny }, "STRATEG_01")
        )
    ),

    // Page 2: Analytical Depth
    React.createElement(Page, { size: "A4", style: styles.page },
        React.createElement(View, { style: styles.topBar },
            React.createElement(Text, { style: styles.labelTiny }, "NEXUS_SYSTEM_DOC // V1.0"),
            React.createElement(Text, { style: styles.labelTiny }, "REF: 1965-GRID-B")
        ),

        React.createElement(View, { style: styles.contentGrid },
            React.createElement(View, { style: styles.leftCol },
                React.createElement(View, { style: { marginTop: 100 } },
                    React.createElement(Text, { style: styles.sectionLabel }, "МЕТОДОЛОГИЯ"),
                    React.createElement(Text, { style: [styles.moduleText, { color: '#000', fontSize: 12 }] },
                        "«Хороший дизайн — это как можно меньше дизайна». В NEXUS это означает минимальный путь от запроса к исполнению."
                    )
                )
            ),
            React.createElement(View, { style: styles.rightCol },
                React.createElement(ModuleItem, {
                    num: "02",
                    title: "Аналитическое Стекло",
                    desc: "Прозрачность рыночных сред. Парсинг и структурирование данных как инженерная задача.",
                    practice: "Кейс: Автономный аудит конкурентов. Данные подаются в чистом виде, готовые к анализу."
                }),
                React.createElement(ModuleItem, {
                    num: "03",
                    title: "Архитектура Знаний",
                    desc: "Трансформация хаоса в систему. ADR и логгирование каждого архитектурного решения.",
                    practice: "Кейс: Ведение PROGRESS_LOG.md как истории развития продукта, где каждый шаг обоснован."
                })
            )
        ),

        React.createElement(View, { style: styles.footer },
            React.createElement(Text, { style: styles.labelTiny }, "PAGE 02"),
            React.createElement(Text, { style: styles.labelTiny }, "NEXUS PRIME // 2026")
        )
    )
);

// Generation Script
const renderPdf = async () => {
    const ReactPDF = require('@react-pdf/renderer');
    const path = require('path');
    const outputPath = path.join(__dirname, '../../outputs/Nexus_Rams_Rational_RU.pdf');

    try {
        console.log('Generating Dieter Rams Rational Manual...');
        await ReactPDF.render(React.createElement(NexusPresentation), outputPath);
        console.log(`Successfully generated: ${outputPath}`);
    } catch (error) {
        console.error('Generation Failed:', error);
    }
};

renderPdf();
