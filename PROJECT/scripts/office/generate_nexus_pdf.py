import os
import sys
import pdfkit

# NEXUS 2026 PDF CONVERTER (HTML-to-PDF Engine)
# Uses wkhtmltopdf for high-fidelity conversion.

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' # Common path

def convert_html_to_pdf(html_file, pdf_file):
    print(f"📄 Converting HTML to PDF: {html_file}")
    
    if not os.path.exists(html_file):
        print(f"❌ Error: HTML file not found at {html_file}")
        return False
        
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    try:
        pdfkit.from_file(html_file, pdf_file, configuration=config, options=options)
        print(f"✅ Success! PDF Generated at: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ PDF Generation Error: {e}")
        # Fallback to a simpler way if wkhtmltopdf is missing
        print("💡 Suggestion: Please install wkhtmltopdf to enable high-tier PDF generation.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default for local run
        html_src = "e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT\\outputs\\NEXUS_GRAND_VISION_v2.html"
        pdf_dst = "e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT\\outputs\\NEXUS_GRAND_VISION_v2.pdf"
    else:
        html_src = sys.argv[1]
        pdf_dst = sys.argv[2]
        
    convert_html_to_pdf(html_src, pdf_dst)
