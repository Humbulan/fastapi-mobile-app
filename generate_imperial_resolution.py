from fpdf import FPDF

class ImperialPDF(FPDF):
    def header(self):
        # Professional Blue Accent
        self.set_fill_color(20, 50, 100)
        self.rect(0, 0, 210, 35, 'F')
        
        # Company Name in White
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD', 0, 1, 'C')
        
        # Registration & ORCID in White
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Registration No: 2024/626727/07 | Technical Authority: ORCID 0009-0000-9572-4545', 0, 1, 'C')
        self.ln(10)

pdf = ImperialPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.set_text_color(0, 0, 0)
pdf.ln(15)

# Document Title
pdf.cell(0, 12, 'CERTIFIED MEMBERS RESOLUTION & SIGNATORY AUTHORITY', 'B', 1, 'C')
pdf.ln(10)

# Body Content
pdf.set_font('Arial', '', 11)
content = (
    "In accordance with the Companies Act of South Africa, it is hereby formally resolved "
    "by the Board of Directors of HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD that:\n\n"
    "1. The Company shall establish a corporate investment and trading facility with EasyEquities.\n\n"
    "2. HUMBULANI MUDAU, in his capacity as CEO and sole Director, is hereby appointed as "
    "the Authorized Representative. He is granted full power of attorney to execute all "
    "agreements, including the election of Scrip Dividends for the Scancom PLC (MTN Ghana) "
    "holdings and the settlement of SADC Corridor trade revenue.\n\n"
    "3. This resolution is effective immediately for the scheduled April 10, 2026, capital rebase."
)
pdf.multi_cell(0, 8, content)

# Official Signature Section
pdf.ln(25)
pdf.set_font('Arial', 'B', 11)
pdf.cell(100, 10, '__________________________', 0, 0, 'L')
pdf.cell(0, 10, 'Date: 31 March 2026', 0, 1, 'R')
pdf.cell(100, 10, 'HUMBULANI MUDAU', 0, 0, 'L')
pdf.set_font('Arial', 'I', 10)
pdf.cell(0, 10, 'Thohoyandou, Limpopo', 0, 1, 'R')
pdf.set_font('Arial', 'B', 10)
pdf.cell(100, 10, 'Chief Executive Officer', 0, 1, 'L')

pdf.output('Imperial_Omega_Resolution_2026.pdf')
