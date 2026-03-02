import sys
import os
from fpdf import FPDF

class NexusPersonaPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'B', 8)
            self.set_text_color(150)
            self.cell(0, 10, 'NEXUS OPERATOR PROFILE // PERSONAL CAPABILITIES', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150)
        self.cell(0, 10, f'LEVERAGING ARTIFICIAL INTELLIGENCE // PAGE {self.page_no()}', 0, 0, 'C')

def create_persona_pdf():
    pdf = NexusPersonaPDF()
    pdf.set_margins(20, 20, 20)
    
    # PAGE 1: COVER
    pdf.add_page()
    
    # Operator Concept Image
    img_path = r'C:\Users\MAC\.gemini\antigravity\brain\858d0bd1-44f8-418a-847c-07d05808974d\nexus_operator_concept_1772198207106.png'
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210)
    
    pdf.set_y(160)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(255) # White for cover
    pdf.cell(0, 20, 'THE NEXUS OPERATOR', 0, 1, 'L')
    pdf.set_font('helvetica', '', 14)
    pdf.cell(0, 10, 'AUGMENTED INTELLIGENCE & RAPID SOLVING', 0, 1, 'L')
    
    pdf.set_y(250)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 10, 'OPERATIONAL CAPABILITIES PROFILE // 2026', 0, 1, 'L')

    # PAGE 2: VALUE PROPOSITION
    pdf.add_page()
    pdf.set_text_color(15, 23, 42) # Dark Slate
    
    pdf.set_font('helvetica', 'B', 24)
    pdf.cell(0, 20, 'Value Proposition', 0, 1, 'L')
    
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 8, (
        "This profile represents a professional integrated with a high-performance "
        "AI Agent Ecosystem (Nexus Prime). This synergy enables the solving of "
        "complex technical and strategic tasks at speeds unattainable by traditional "
        "methods."
    ))
    pdf.ln(10)

    # SEC 2: CAPABILITIES
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 12, 'CORE COMPETENCIES', 0, 1, 'L')
    pdf.ln(2)
    
    capabilities = [
        ["Rapid Prototyping", "Deploying Rust, Python, and Go systems in minutes."],
        ["Architecture Design", "Bayesian tech selection for optimal cost/performance."],
        ["System Optimization", "Aggressive resource management for hardware constraints."],
        ["Automated Workflows", "Using agentic logic to eliminate manual overhead."]
    ]
    
    for title, desc in capabilities:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, f"{title}:", 0, 1)
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 6, f"{desc}")
        pdf.ln(4)

    pdf.ln(10)
    
    # SEC 3: THE NEXUS EDGE
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 12, 'THE NEXUS EDGE', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(50, 10, ' COMPONENT', 1, 0, 'L', True)
    pdf.cell(0, 10, ' OPERATIONAL IMPACT', 1, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 9)
    edge = [
        ["AI Agent (Jules)", "Async code synthesis and background task execution."],
        ["Omni-Dashboard", "Real-time visibility into complex project health."],
        ["Turbo-Kernel", "100k msg/s throughput for data-heavy workloads."],
        ["Skills Protocol", "Extensible library of 800+ specialized automations."]
    ]
    for comp, impact in edge:
        pdf.cell(50, 10, f" {comp}", 1, 0)
        pdf.cell(0, 10, f" {impact}", 1, 1)

    # FINAL STATEMENT
    pdf.ln(20)
    pdf.set_font('helvetica', 'I', 11)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 7, (
        "\"The problem is not the problem. The problem is your attitude about the problem, "
        "and the tools you use to solve it.\""
    ), 0, 'C')

    output_path = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs\Nexus_Operator_Profile.pdf'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"OPERATOR_PROFILE_GENERATED: {output_path}")

if __name__ == "__main__":
    create_persona_pdf()
