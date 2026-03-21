import sys
import os
from docx2pdf import convert

def convert_to_pdf(input_docx, output_pdf):
    try:
        print(f"Converting {input_docx} to PDF...")
        # Note: This requires Microsoft Word installed on Windows
        convert(input_docx, output_pdf)
        print(f"PDF_GENERATED: {output_pdf}")
    except Exception as e:
        print(f"ERROR: Failed to convert to PDF. Ensure MS Word is installed. Detail: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_file = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs\Architecture_Report_Nexus.docx'
    output_file = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs\Architecture_Report_Nexus.pdf'
    
    if os.path.exists(input_file):
        convert_to_pdf(input_file, output_file)
    else:
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)
