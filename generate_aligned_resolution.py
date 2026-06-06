from fpdf import FPDF

class ImperialPDF(FPDF):
    def header(self):
        # Header matching 119131.jpg
        self.set_font('Arial', 'B', 12)
        self.set_text_color(20, 50, 100)
        self.cell(0, 8, 'HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 4, 'Registration No: 2024/626727/07', 0, 1, 'C')
        self.cell(0, 4, 'Technical Authority: ORCID 0009-0000-9572-4545', 0, 1, 'C')
        self.cell(0, 4, 'Email: humbulani@humbu.store | Address: Thohoyandou, Limpopo, 0950', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(20, 50, 100)
        self.line(10, 38, 200, 38)

pdf = ImperialPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 11)
pdf.ln(15)

# Blue Title Box
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, 'CERTIFIED EXTRACT: MEMBERS RESOLUTION & AUTHORITY TO ACT', 0, 1, 'C', fill=True)
pdf.ln(5)

# ALIGNED DATE: 31 MARCH 2026
pdf.set_font('Arial', 'B', 9)
pdf.set_text_color(20, 50, 100)
pdf.cell(0, 10, 'Date of Resolution: 31 March 2026', 0, 1, 'L')
pdf.ln(2)

pdf.set_font('Arial', '', 9)
pdf.set_text_color(0, 0, 0)
intro = "It is hereby resolved that HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD shall undertake the following actions as of the resolution date stated above:"
pdf.multi_cell(0, 5, intro)
pdf.ln(3)

bullets = [
    "Open a business investment account with EasyEquities (account type: Business Investment Account);",
    "Nominate HUMBULANI MUDAU, in his capacity as CEO and sole Director, as the Authorized Signatory and Representative for all transactions and administrative actions related to this account;",
    "Authorize the representative to manage the SADC Corridor revenue settlements and the Scrip Dividend election for the Scancom PLC (MTN Ghana) position scheduled for April 10, 2026."
]

for bullet in bullets:
    pdf.cell(10)
    pdf.cell(5, 5, chr(149))
    pdf.multi_cell(0, 5, bullet)
    pdf.ln(2)

pdf.set_font('Arial', 'B', 9)
pdf.set_text_color(20, 50, 100)
pdf.cell(0, 5, 'Authority Granted:', 0, 1, 'L')
pdf.ln(1)
pdf.set_font('Arial', '', 9)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 5, "This authority is granted in accordance with the Memorandum of Incorporation filed with the CIPC on 08 October 2024. All signatures below confirm the validity of this appointment as of 31 March 2026.")

# Signature Box
pdf.ln(15)
pdf.rect(20, pdf.get_y(), 170, 40)
pdf.ln(10)
pdf.cell(25)
pdf.cell(60, 5, '__________________________', 0, 0, 'C')
pdf.cell(15)
pdf.cell(60, 5, '__________________________', 0, 1, 'C')

pdf.set_font('Arial', 'B', 8)
pdf.cell(25)
pdf.cell(60, 5, 'HUMBULANI MUDAU', 0, 0, 'C')
pdf.cell(15)
# SIGNATURE DATE: 31 MARCH 2026
pdf.cell(60, 5, '31/03/2026', 0, 1, 'C')

pdf.set_font('Arial', 'I', 7)
pdf.cell(25)
pdf.cell(60, 5, 'CEO / Director', 0, 0, 'C')
pdf.cell(15)
pdf.cell(60, 5, 'Date', 0, 1, 'C')

pdf.output('Imperial_Resolution_Aligned_31March.pdf')
