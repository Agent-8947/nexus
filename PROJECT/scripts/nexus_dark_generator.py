import os
from pathlib import Path
from docx import Document
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime

# --- NEXUS PREMIUM DARK STYLE CONFIG [REFINED] ---
class NexusDarkPDF(FPDF):
    def __init__(self, lang_code='EN', title="NEXUS INSTRUCTION"):
        super().__init__()
        self.lang_code = lang_code
        self.doc_title = title
        self.set_margins(30, 30, 30)
        
        # Colors (Nexus Hardened Palette)
        self.color_bg = (5, 5, 5)        # Deep Black
        self.color_text = (248, 250, 252) # White-ish
        self.color_dim = (71, 85, 105)    # Slate-500
        self.color_accent = (16, 185, 129) # Emerald Green
        self.color_border = (30, 41, 59)   # Slate-800 for dividers
        
        # Load Fonts
        font_bold = r'C:\Windows\Fonts\arialbd.ttf'
        font_regular = r'C:\Windows\Fonts\arial.ttf'
        self.add_font('NexusFont', '', font_regular)
        self.add_font('NexusFont', 'B', font_bold)
        self.use_unicode = True

    def header(self):
        # Dark Background Fill per Page
        self.set_fill_color(*self.color_bg)
        self.rect(0, 0, 210, 297, 'F')
        
        if self.page_no() == 1: return # Minimal header on cover

        self.set_y(20)
        self.set_font('NexusFont', 'B', 9)
        self.set_text_color(*self.color_text)
        self.cell(0, 5, f'NEXUS / {self.doc_title.upper()}', new_x=XPos.LMARGIN, new_y=YPos.TOP)
        
        self.set_font('NexusFont', '', 8)
        self.set_text_color(*self.color_dim)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d // %H:%M")
        self.cell(0, 5, f'CORE NODE: ACTIVE // {timestamp}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Tactical Border
        self.set_draw_color(*self.color_border)
        self.set_line_width(0.3)
        self.line(30, 30, 180, 30)
        self.ln(15)

    def footer(self):
        if self.page_no() == 1: return
        
        self.set_y(-25)
        self.set_draw_color(*self.color_border)
        self.line(30, self.get_y(), 180, self.get_y())
        
        self.ln(5)
        self.set_font('NexusFont', 'B', 8)
        self.set_text_color(*self.color_dim)
        self.cell(0, 5, 'STRICTLY CONFIDENTIAL // NEXUS PRIME OS', new_x=XPos.WCONT, new_y=YPos.TOP)
        self.cell(0, 5, f'PAGE {self.page_no()}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def draw_cover(self):
        self.add_page()
        self.set_y(100)
        
        # Large Hero Title
        self.set_font('NexusFont', 'B', 48)
        self.set_text_color(*self.color_text)
        self.cell(0, 20, "NEXUS", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Tactical Subtitle
        self.set_font('NexusFont', 'B', 14)
        self.set_text_color(*self.color_accent)
        self.cell(0, 10, f"{self.doc_title.upper()} // V6.0", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Grid Element
        self.ln(40)
        self.set_draw_color(*self.color_accent)
        self.set_line_width(0.5)
        self.line(80, self.get_y(), 130, self.get_y())
        
        self.ln(20)
        self.set_font('NexusFont', '', 10)
        self.set_text_color(*self.color_dim)
        self.cell(0, 10, "ESTABLISHED 2026 // HARDENED DOCUMENTATION", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def draw_section_label(self, num, title):
        self.ln(10)
        # Tactical Square
        self.set_fill_color(*self.color_accent)
        self.rect(30, self.get_y() + 2, 5, 5, 'F')
        
        self.set_x(40)
        self.set_font('NexusFont', 'B', 8)
        self.set_text_color(*self.color_accent)
        self.cell(0, 5, f"SECTION {num}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_x(40)
        self.set_font('NexusFont', 'B', 24)
        self.set_text_color(*self.color_text)
        self.multi_cell(0, 10, title.upper())
        self.ln(5)

    def add_block_title(self, text):
        self.ln(4)
        self.set_x(40)
        self.set_font('NexusFont', 'B', 10)
        self.set_text_color(*self.color_accent)
        self.cell(0, 8, f"// {text.upper()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_body_text(self, text):
        self.set_x(40)
        self.set_font('NexusFont', '', 11)
        self.set_text_color(*self.color_text)
        # Using multi_cell for flow
        self.multi_cell(140, 6, text, align='L')
        self.ln(3)

def process_language(lang_code):
    in_file = Path(f"INBOX/{lang_code}/NEXUS_{lang_code}_COMBINED.docx")
    out_dir = Path("PROJECT/outputs/INSTRUCTIONS")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"NEXUS_CORE_INSTRUCTION_{lang_code}.pdf"
    
    if not in_file.exists():
        print(f"[-] Missing: {in_file}")
        return

    print(f"[*] Processing Premium Dark PDF [v2] for {lang_code}...")
    doc = Document(in_file)
    
    titles = {
        'EN': 'Operational Manual',
        'RU': 'Инструкция Пользователя',
        'UA': 'Інструкція Користувача'
    }
    
    pdf = NexusDarkPDF(lang_code, titles.get(lang_code, 'Manual'))
    
    # 0. COVER
    pdf.draw_cover()
    
    # 1. CONTENT
    pdf.add_page()
    section_count = 1
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
            
        if text.startswith('--- Document:'):
            header_text = text.replace('--- Document: ', '').replace(' ---', '')
            pdf.draw_section_label(f"0{section_count}", header_text)
            section_count += 1
        elif para.style.name.startswith('Heading'):
            pdf.add_block_title(text)
        else:
            pdf.add_body_text(text)

    pdf.output(str(out_file))
    print(f"✅ Generated: {out_file}")

if __name__ == "__main__":
    for lang in ['EN', 'RU', 'UA']:
        process_language(lang)
