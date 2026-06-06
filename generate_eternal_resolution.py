from fpdf import FPDF

class ImperialOmegaPDF(FPDF):
    def header(self):
        # 1. THE ETERNAL BUSINESS LOGO (Top Left)
        self.set_fill_color(20, 50, 100) # Imperial Blue
        self.rect(10, 10, 20, 20, 'F')
        self.set_font('Arial', 'B', 12)
        self.set_text_color(255, 255, 255)
        self.text(12, 22, 'HW') # Logo Initials
        
        # 2. CORPORATE HEADER (Top Right)
        self.set_text_color(20, 50, 100)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 5, 'HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD', 0, 1, 'R')
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Global Infrastructure & SADC Corridor Logistics', 0, 1, 'R')
        
        # 3. LEGAL IDENTITY LINE
        self.ln(5)
        self.set_draw_color(20, 50, 100)
        self.set_line_width(0.5)
        self.line(10, 35, 200, 35)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Generated via Imperial Omega Systems | Technical Authority: ORCID 0009-0000-9572-4545', 0, 0, 'C')

pdf = ImperialOmegaPDF()
pdf.add_page()

# LEGAL SPECIFICATIONS SECTION
pdf.set_font('Arial', 'B', 10)
pdf.set_text_color(0, 0, 0)
pdf.cell(40, 7, 'Entity Type:', 0, 0)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 7, 'Private Company (Pty) Ltd', 0, 1)

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Registration No:', 0, 0)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 7, '2024/626727/07 (Incorporated 08 October 2024)', 0, 1)

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Jurisdiction:', 0, 0)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 7, 'Republic of South Africa (CIPC/SARS Compliant)', 0, 1)
pdf.ln(5)

# TITLE BOX
pdf.set_fill_color(240, 245, 255)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 12, 'CERTIFIED EXTRACT: MEMBERS RESOLUTION & AUTHORITY TO ACT', 1, 1, 'C', fill=True)
pdf.ln(8)

# ALIGNED DATE
pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 10, 'Resolution Effective Date: 31 March 2026', 0, 1, 'L')

# FORMAL BODY
pdf.set_font('Arial', '', 10)
body_text = (
    "In accordance with the Memorandum of Incorporation (MOI) and the Companies Act 71 of 2008, "
    "it is hereby resolved that the Board of Directors authorizes the following corporate actions:"
)
pdf.multi_cell(0, 6, body_text)
pdf.ln(4)

# THE YESTERDAY BULLETS (Restored & Improved)
bullets = [
    "The establishment of a primary corporate investment account with EasyEquities for the management of international equity and SADC regional assets.",
    "The nomination of HUMBULANI MUDAU, in his capacity as Chief Executive Officer and Sole Director, as the Principal Authorized Signatory for all fiscal and administrative mandates.",
    "Full authority is granted to execute the Scrip Dividend Election for Scancom PLC (MTN Ghana) and the processing of SADC Corridor trade revenue settlements scheduled for 10 April 2026."
]

for b in bullets:
    pdf.cell(8)
    pdf.cell(5, 6, '-', 0, 0)
    pdf.multi_cell(0, 6, b)
    pdf.ln(2)

# SIGNATURE BLOCK
pdf.ln(15)
pdf.set_draw_color(20, 50, 100)
pdf.rect(15, pdf.get_y(), 180, 45) # Professional Border
pdf.ln(10)
pdf.cell(20)
pdf.cell(65, 10, '__________________________', 0, 0, 'C')
pdf.cell(30)
pdf.cell(65, 10, '__________________________', 0, 1, 'C')

pdf.set_font('Arial', 'B', 9)
pdf.cell(20)
pdf.cell(65, 5, 'HUMBULANI MUDAU', 0, 0, 'C')
pdf.cell(30)
pdf.cell(65, 5, '31/03/2026', 0, 1, 'C')

pdf.set_font('Arial', 'I', 8)
pdf.cell(20)
pdf.cell(65, 5, 'CEO & Directorial Authority', 0, 0, 'C')
pdf.cell(30)
pdf.cell(65, 5, 'Authorized Execution Date', 0, 1, 'C')

pdf.output('Imperial_Omega_Standard_Resolution.pdf')
print("✅ Enhanced resolution generated: Imperial_Omega_Standard_Resolution.pdf")
