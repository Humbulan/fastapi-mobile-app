from fpdf import FPDF

class ImperialPDF(FPDF):
    def header(self):
        self.set_fill_color(20, 50, 100)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Reg No: 2024/626727/07 (Inc. 08 Oct 2024) | ORCID: 0009-0000-9572-4545', 0, 1, 'C')
        self.ln(10)

pdf = ImperialPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.set_text_color(0, 0, 0)
pdf.ln(15)
pdf.cell(0, 12, 'CERTIFIED MEMBERS RESOLUTION & AUTHORITY TO ACT', 'B', 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', '', 11)
content = (
    "It is hereby resolved by the Board of Directors that the Company shall establish a "
    "corporate investment facility with EasyEquities. HUMBULANI MUDAU, as CEO and sole Director, "
    "is authorized to manage the Scancom PLC (MTN Ghana) scrip dividend election and SADC "
    "corridor revenue settlements scheduled for April 10, 2026.\n\n"
    "This authority is granted in accordance with the Memorandum of Incorporation filed "
    "with the CIPC on 08 October 2024."
)
pdf.multi_cell(0, 8, content)
pdf.ln(25)
pdf.set_font('Arial', 'B', 11)
pdf.cell(100, 10, '__________________________', 0, 0, 'L')
pdf.cell(0, 10, 'Date: 01 April 2026', 0, 1, 'R')
pdf.cell(100, 10, 'HUMBULANI MUDAU (CEO)', 0, 1, 'L')
pdf.output('Final_Humbu_Wandeme_Resolution.pdf')
