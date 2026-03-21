const fs = require('fs');
const path = require('path');
const React = require('react');
const { Document, Page, Text, View, StyleSheet, Font, renderToFile } = require('@react-pdf/renderer');

Font.register({
    family: 'Roboto',
    fonts: [
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-regular-webfont.ttf' },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf', fontWeight: 'bold' },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf', fontWeight: 700 },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-regular-webfont.ttf', fontWeight: 500 },
    ]
});

// Минималистичная рациональная цветовая схема (светлая)
const C = {
    bg: '#FFFFFF',
    text: '#111111',
    textDim: '#555555',
    textMuted: '#999999',
    border: '#EAEAEA',
    borderDark: '#111111'
};

const s = StyleSheet.create({
    page: { padding: 40, backgroundColor: C.bg, color: C.text, fontFamily: 'Roboto', position: 'relative' },
    coverPage: { display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%', paddingLeft: 20 },

    // Типографика
    tag: { fontSize: 9, fontWeight: 700, color: C.textMuted, textTransform: 'uppercase', letterSpacing: 3, marginBottom: 24 },
    h1: { fontSize: 32, fontWeight: 700, color: C.text, letterSpacing: -0.5, textTransform: 'uppercase', marginBottom: 12 },
    h2: { fontSize: 12, fontWeight: 400, color: C.textDim, marginBottom: 8, lineHeight: 1.5 },
    sectionTitle: { fontSize: 14, fontWeight: 700, color: C.text, letterSpacing: 0.5, textTransform: 'uppercase', marginTop: 32, marginBottom: 16 },
    subTitle: { fontSize: 11, fontWeight: 700, color: C.text, marginBottom: 12, marginTop: 20, letterSpacing: 0.5 },
    text: { fontSize: 10, lineHeight: 1.6, color: C.textDim, marginBottom: 8 },

    indicator: { width: 30, height: 2, backgroundColor: C.text, marginVertical: 32 },

    // Таблицы (строгие, без заливки)
    table: { marginBottom: 16, borderTopWidth: 1, borderTopColor: C.borderDark },
    tableHeader: { flexDirection: 'row', paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: C.borderDark },
    tableRow: { flexDirection: 'row', paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: C.border },
    headerCell: { fontSize: 8, fontWeight: 700, textTransform: 'uppercase', color: C.textMuted },
    cell: { fontSize: 9.5, color: C.text, lineHeight: 1.5, paddingRight: 8 },

    // Блоки
    codeBlock: { backgroundColor: '#FAFAFA', padding: 16, marginBottom: 16, borderWidth: 1, borderColor: C.border },
    codeText: { fontSize: 8.5, fontFamily: 'Roboto', color: C.textDim, lineHeight: 1.6 },
    warningBlock: { padding: 16, marginBottom: 16, borderLeftWidth: 2, borderLeftColor: C.text, backgroundColor: '#FAFAFA' },

    // Списки
    dotRow: { flexDirection: 'row', marginBottom: 8, paddingLeft: 4 },
    dot: { fontSize: 10, color: C.textMuted, marginRight: 12 },
    dotText: { fontSize: 10, color: C.text, lineHeight: 1.6, flex: 1 },

    // Футер
    footer: { position: 'absolute', bottom: 30, left: 40, right: 40, flexDirection: 'row', justifyContent: 'space-between', borderTopWidth: 1, borderTopColor: C.border, paddingTop: 12 },
    footerText: { fontSize: 7, color: C.textMuted, textTransform: 'uppercase', letterSpacing: 1 },
});

const el = React.createElement;
const Footer = ({ num }) => el(View, { style: s.footer, fixed: true },
    el(Text, { style: s.footerText }, 'PRINTSERVER AUTOMATION // PREFLIGHT STACK'),
    el(Text, { style: s.footerText }, `${num} / 08`)
);
const Dot = ({ text }) => el(View, { style: s.dotRow },
    el(Text, { style: s.dot }, '—'),
    el(Text, { style: s.dotText }, text)
);
const TableRow = ({ cells, widths, isHeader }) => {
    const rowStyle = isHeader ? s.tableHeader : s.tableRow;
    const cellStyle = isHeader ? s.headerCell : s.cell;
    return el(View, { style: rowStyle },
        ...cells.map((c, i) => el(Text, { key: i, style: [cellStyle, { width: widths[i] }] }, c))
    );
};

const PdfDocument = () => el(Document, { title: 'PrintServer Automation', author: 'NEXUS' },

    // PAGE 1: COVER
    el(Page, { size: 'A4', style: [s.page, s.coverPage] },
        el(Text, { style: s.tag }, 'NEXUS ARCHITECTURE'),
        el(Text, { style: s.h1 }, 'PRINTSERVER'),
        el(Text, { style: s.h1 }, 'PREFLIGHT STACK'),
        el(View, { style: s.indicator }),
        el(Text, { style: s.h2 }, 'Справочник технологического стека предпечатной подготовки.'),
        el(Text, { style: [s.h2, { marginTop: 20 }] }, 'Версия: 1.0 (PROD)'),
        el(Text, { style: s.h2 }, 'Среда: NVIDIA RTX 5060 / 64 GB RAM / CUDA 12+'),
        el(Footer, { num: '01' })
    ),

    // PAGE 2: VALIDATION & GRAPHICS
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '01. Валидация и анализ файлов'),
        el(Text, { style: s.text }, 'Определение физических характеристик, метаданных и формата.'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '15%', '45%', '15%'], cells: ['Инструмент', 'Версия', 'Назначение', 'Среда'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['PyMuPDF (fitz)', '1.25+', 'PDF: размеры, шрифты, spot colors', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['PyPDFium2', 'Latest', 'Быстрое извлечение данных', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['pikepdf', 'Latest', 'Низкоуровневый PDF, ICC профили', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['Ghostscript', '10.x', 'Глубокая валидация, flattening', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['Pillow (PIL)', '11.x', 'EXIF/DPI (TIFF, JPG, PNG)', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['python-magic', 'Latest', 'MIME-тип (защита от spoofing)', 'CPU'] }),
        ),

        el(Text, { style: s.sectionTitle }, '02. Обработка тяжёлой графики'),
        el(Text, { style: s.text }, 'Потоковая обработка файлов 100 MB – 5+ GB.'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '15%', '45%', '15%'], cells: ['Инструмент', 'Версия', 'Назначение', 'Среда'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['libvips (pyvips)', '8.16+', 'Потоковая работа без RAM', 'CPU'] }),
            el(TableRow, { widths: ['25%', '15%', '45%', '15%'], cells: ['OpenCV', '4.10+', 'Edge detection, контуры', 'CUDA'] }),
        ),
        el(View, { style: s.warningBlock },
            el(Text, { style: [s.cell, { fontWeight: 700 }] }, 'ПРОИЗВОДИТЕЛЬНОСТЬ (Баннер 5м / 2.1 GB)'),
            el(Text, { style: s.text }, 'Pillow: ~8 GB RAM / 45 сек (OOM при множестве)\nlibvips: ~150 MB RAM / 8 сек (Стабильно)')
        ),
        el(Footer, { num: '02' })
    ),

    // PAGE 3: COLOR & VECTORIZATION
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '03. Управление цветом (ICC)'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['30%', '70%'], cells: ['Библиотека', 'Назначение'] }),
            el(TableRow, { widths: ['30%', '70%'], cells: ['LittleCMS', 'RGB→CMYK. Relative Colorimetric Intent'] }),
            el(TableRow, { widths: ['30%', '70%'], cells: ['libvips icc_transform', 'Потоковая конвертация ICC. Embedded profiles'] }),
            el(TableRow, { widths: ['30%', '70%'], cells: ['Ghostscript CMYK', 'CMYK Conversion. Spot Colors, DeviceN'] }),
        ),

        el(Text, { style: s.sectionTitle }, '04. Векторизация (Raster→Vector)'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['20%', '15%', '45%', '20%'], cells: ['Модель', 'Тип', 'Ключевая особенность', 'Вывод'] }),
            el(TableRow, { widths: ['20%', '15%', '45%', '20%'], cells: ['VTracer', 'Base', 'O(n) алгоритм, полноцвет', 'Color SVG'] }),
            el(TableRow, { widths: ['20%', '15%', '45%', '20%'], cells: ['Potrace', 'Classic', 'Mono Bitmap → SVG, Bezier', 'Mono SVG'] }),
            el(TableRow, { widths: ['20%', '15%', '45%', '20%'], cells: ['StarVector', 'AI 8B', 'SVG как код. SOTA качество', 'AI SVG'] }),
            el(TableRow, { widths: ['20%', '15%', '45%', '20%'], cells: ['CairoSVG', 'Convert', 'SVG → PDF/PNG', 'PDF/PNG'] }),
        ),
        el(Text, { style: s.subTitle }, 'Стратегия маршрутизации'),
        el(Dot, { text: 'Логотип (1-5 цветов): VTracer или Potrace (максимальная скорость).' }),
        el(Dot, { text: 'Сложная иллюстрация: VTracer (баланс качества и размера).' }),
        el(Dot, { text: 'Premium-заказ: StarVector (требует 16GB VRAM, нейро-трейсинг).' }),

        el(Footer, { num: '03' })
    ),

    // PAGE 4: AI BG
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '05. AI: Удаление фона'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '40%', '35%'], cells: ['Инструмент', 'Назначение', 'Среда'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['rembg (isnet)', 'Удаление сложного фона', 'CUDA (onnxruntime)'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['Pillow flood-fill', 'Простой однотонный фон', 'CPU (< 1 сек)'] }),
        ),

        el(Text, { style: s.sectionTitle }, '06. AI: Супер-разрешение'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '20%', '55%'], cells: ['Нейросеть', '×', 'Специфика (CUDA)'] }),
            el(TableRow, { widths: ['25%', '20%', '55%'], cells: ['Real-ESRGAN x4+', '×4', 'Фото, общие текстуры. Очень быстрая'] }),
            el(TableRow, { widths: ['25%', '20%', '55%'], cells: ['Real-ESRGAN anime', '×4', 'Векторные иллюстрации, графика'] }),
            el(TableRow, { widths: ['25%', '20%', '55%'], cells: ['SwinIR', '×2 / ×4', 'Фоны, сцены, точность деталей'] }),
            el(TableRow, { widths: ['25%', '20%', '55%'], cells: ['HAT', '×2 / ×4', 'SOTA PSNR. Максимальное качество'] }),
        ),
        el(Text, { style: s.subTitle }, 'Маршрутизация'),
        el(Dot, { text: '≥ 150 DPI: Пропустить.' }),
        el(Dot, { text: '100 — 149 DPI: SwinIR ×2.' }),
        el(Dot, { text: '72 — 99 DPI: Real-ESRGAN ×4.' }),
        el(Dot, { text: '< 72 DPI: Брак (Отклонено).' }),
        el(View, { style: s.warningBlock },
            el(Text, { style: [s.cell, { fontWeight: 700 }] }, 'GPU VRAM LIMIT'),
            el(Text, { style: s.text }, 'Использование "tiling" обязательно для исходников > 4000x4000px. Выполнение только в 1 поток.')
        ),
        el(Footer, { num: '04' })
    ),

    // PAGE 5: GEOMETRY
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '07. Управление геометрией'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '75%'], cells: ['Функция', 'Инструменты'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['Bleeds 3мм', 'libvips (EXTEND_MIRROR / EXTEND_BACKGROUND)'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['Авто-кромка', 'OpenCV Canny Edge Detection'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['Авто-выпрямление', 'OpenCV HoughLines (< 5° deskew)'] }),
        ),

        el(Text, { style: s.sectionTitle }, '08. Компоновка рулона (Nesting)'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '35%', '40%'], cells: ['Библиотека', 'Алгоритм', 'Возможности'] }),
            el(TableRow, { widths: ['25%', '35%', '40%'], cells: ['rectpack', '2D Bin Packing', 'Ротация 90°, группировка'] }),
            el(TableRow, { widths: ['25%', '35%', '40%'], cells: ['hyperpack', 'Strip Packing', 'Высокая скорость (50+ эл-тов)'] }),
            el(TableRow, { widths: ['25%', '35%', '40%'], cells: ['libvips', 'Холст', 'Потоковая сборка полотна'] }),
            el(TableRow, { widths: ['25%', '35%', '40%'], cells: ['ReportLab', 'Метки', 'Векторные метки реза (crop marks)'] }),
        ),
        el(Footer, { num: '05' })
    ),

    // PAGE 6: PDF FINALIZE
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '09. Служебная графика'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '75%'], cells: ['Модуль', 'Особенности'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['segno', 'QR-коды (ISO 18004). Вывод: SVG/PDF. Без зависимостей'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['python-barcode', 'Штрих-коды (Code128). Вывод: SVG/PNG'] }),
        ),

        el(Text, { style: s.sectionTitle }, '10. Финализация PDF/X'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '75%'], cells: ['Модуль', 'Операции'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['pikepdf', 'Линеаризация, font subsetting, оптимизация структуры'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['Ghostscript', 'Flattening прозрачностей, проверка PDF/X'] }),
            el(TableRow, { widths: ['25%', '75%'], cells: ['OCRmyPDF', 'Текстовый слой (Tesseract)'] }),
        ),
        el(Footer, { num: '06' })
    ),

    // PAGE 7: RISKS & DEPS
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '11. Контроль рисков (Adversarial)'),
        el(View, { style: s.table },
            el(TableRow, { isHeader: true, widths: ['25%', '40%', '35%'], cells: ['Риск', 'Сценарий', 'Митигация'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['OOM GPU', '8k AI Upscale', 'Tiling + 1-поточность'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['Лицензия AGPL', 'Ghostscript', 'Вызов как CLI subprocess'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['Pantone', 'Искажение', 'Relative Colorimetric / Alert'] }),
            el(TableRow, { widths: ['25%', '40%', '35%'], cells: ['Текст на вылетах', 'Обрезка', 'Определение Canny Edge / Фоновый Padding'] }),
        ),

        el(Text, { style: s.sectionTitle }, '12. Стек пакетов'),
        el(View, { style: s.codeBlock },
            el(Text, { style: s.codeText },
                '[Python]\n' +
                'PyMuPDF>=1.25.0       pikepdf>=9.0\n' +
                'pyvips>=2.2.3         vtracer>=0.6.12\n' +
                'rembg[gpu]>=2.0.60    torch>=2.5.0\n' +
                'realesrgan>=0.3.0     rectpack>=0.2.2\n' +
                'reportlab>=4.2        segno>=1.6.0\n\n' +
                '[System]\n' +
                'ghostscript >= 10.0   libvips >= 8.16\n' +
                'CUDA Toolkit 12+'
            )
        ),
        el(Footer, { num: '07' })
    ),

    // PAGE 8: PIPELINE
    el(Page, { size: 'A4', style: s.page },
        el(Text, { style: s.sectionTitle }, '13. Архитектура конвейера'),

        el(View, { style: [s.codeBlock, { backgroundColor: C.bg, borderColor: C.bg, padding: 0 }] },
            el(Text, { style: s.subTitle }, '01 / ВХОД'),
            el(Dot, { text: 'Валидация magic bytes.' }),
            el(Dot, { text: 'Извлечение метаданных PDF.' }),

            el(Text, { style: s.subTitle }, '02 / АНАЛИЗ'),
            el(Dot, { text: 'Проверка геометрии (мм) и плотности (DPI).' }),
            el(Dot, { text: 'Трассировка логотипов.' }),

            el(Text, { style: s.subTitle }, '03 / AI GPU'),
            el(Dot, { text: 'Удаление фона и мусора.' }),
            el(Dot, { text: 'Upscaling до 300 DPI.' }),

            el(Text, { style: s.subTitle }, '04 / СБОРКА'),
            el(Dot, { text: 'Применение ICC профилей → CMYK.' }),
            el(Dot, { text: 'Генерация вылетов.' }),
            el(Dot, { text: 'Бинарная упаковка на рулон.' }),

            el(Text, { style: s.subTitle }, '05 / ФИНАЛ'),
            el(Dot, { text: 'Генерация сервисных кодов.' }),
            el(Dot, { text: 'Линеаризация и проверка PDF/X.' }),
        ),

        el(Footer, { num: '08' })
    ),
);

// ═══════════════════════════════════════════
async function generate() {
    const outputPath = path.resolve(__dirname, '../../outputs/PrintServer_Preflight_Stack.pdf');
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    console.log('[*] Building Minimalist Rational PDF via @react-pdf/renderer...');
    const start = Date.now();
    await renderToFile(React.createElement(PdfDocument), outputPath);
    const elapsed = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`[+] PDF Generated in ${elapsed}s: ${outputPath}`);
}

generate().catch(err => {
    console.error('[-] PDF Generation Failed:', err);
    process.exit(1);
});
