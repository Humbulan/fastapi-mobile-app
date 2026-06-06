from fpdf import FPDF
import datetime

class ProfessionalPDF(FPDF):
    def header(self):
        # Add a subtle background color for header
        self.set_fill_color(245, 245, 245)
        self.rect(0, 0, 210, 45, 'F')
        
        # COMPANY LETTERHEAD SECTION
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, 'HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD', 0, 1, 'C')
        
        self.set_font('Arial', '', 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 5, 'Registration No: 2024/626727/07', 0, 1, 'C')
        self.cell(0, 5, 'Technical Authority: ORCID 0009-0000-9572-4545', 0, 1, 'C')
        self.cell(0, 5, 'Email: humbulani@humbu.store | Address: Thohoyandou, Limpopo, 0950', 0, 1, 'C')
        
        # Decorative line
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(15, 48, 195, 48)
        self.ln(8)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Document ID: RES-{datetime.date.today().strftime("%Y%m")}-001', 0, 0, 'L')
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

# Create PDF
pdf = ProfessionalPDF()
pdf.add_page()

# Document Title with border
pdf.set_font('Arial', 'B', 14)
pdf.set_text_color(0, 51, 102)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 12, 'CERTIFIED EXTRACT: MEMBERS RESOLUTION & AUTHORITY TO ACT', 0, 1, 'C', True)
pdf.ln(8)

# Body content
pdf.set_font('Arial', '', 11)
pdf.set_text_color(0, 0, 0)

# Date
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, f'Date of Resolution: {datetime.date.today().strftime("%d %B %Y")}', 0, 1, 'L')
pdf.ln(5)

# Main resolution text
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 8, 'It is hereby resolved that HUMBU WANDEME TRADING ENTERPRISE (PTY) LTD (hereinafter referred to as "the Company") shall undertake the following actions:')
pdf.ln(3)

# Bullet points (using hyphen instead of bullet to avoid Unicode issues)
pdf.set_font('Arial', '', 11)
bullet_texts = [
    'Open a business investment account with EasyEquities (account type: Business Investment Account);',
    'Nominate HUMBULANI MUDAU, in his capacity as CEO and sole Director, as the Authorized Signatory and Representative for all transactions and administrative actions related to this account;',
    'Authorize the aforementioned representative to manage the SADC Corridor revenue settlements scheduled for April 10, 2026, including but not limited to the election of Scrip Dividends for the Scancom PLC (MTN Ghana) position.'
]

for bullet in bullet_texts:
    pdf.set_x(20)
    pdf.cell(5, 8, '-', 0, 0, 'L')
    pdf.multi_cell(0, 8, bullet)
    pdf.ln(2)

# Authority clause
pdf.ln(5)
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Authority Granted:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 8, 'This resolution serves as the official authorization for the above-named representative to act on behalf of the Company. The authority granted herein shall remain in full force and effect until revoked in writing by a subsequent resolution of the Company\'s members.')

# Signature block
pdf.ln(15)

# Add a box for signatures
pdf.set_draw_color(200, 200, 200)
pdf.set_fill_color(250, 250, 250)
pdf.rect(20, pdf.get_y(), 170, 60, 'D')

# Signature area
pdf.set_y(pdf.get_y() + 10)
pdf.set_font('Arial', '', 10)
pdf.cell(85, 8, '__________________________', 0, 0, 'C')
pdf.cell(85, 8, '__________________________', 0, 1, 'C')
pdf.cell(85, 6, 'Signature', 0, 0, 'C')
pdf.cell(85, 6, 'Date', 0, 1, 'C')
pdf.ln(5)
pdf.cell(85, 8, 'HUMBULANI MUDAU', 0, 0, 'C')
pdf.cell(85, 8, f'{datetime.date.today().strftime("%d/%m/%Y")}', 0, 1, 'C')
pdf.cell(85, 6, 'CEO / Director', 0, 0, 'C')
pdf.cell(85, 6, '', 0, 1, 'C')

# Certification statement
pdf.ln(8)
pdf.set_font('Arial', 'I', 9)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'I, the undersigned, certify that I am duly authorized to execute this resolution on behalf of the Company.', 0, 1, 'C')
pdf.cell(0, 6, 'This resolution was duly adopted by the members of the Company.', 0, 1, 'C')

# Verification code
pdf.ln(5)
pdf.set_font('Arial', 'B', 8)
pdf.set_text_color(150, 150, 150)
pdf.cell(0, 6, 'Digitally generated document - Verification Code: ' + datetime.date.today().strftime("%Y%m%d") + '-HWT001', 0, 1, 'C')

# Output PDF
pdf.output('Resolution_Humbu_Wandeme_Professional.pdf')
print("✅ Professional PDF Generated: Resolution_Humbu_Wandeme_Professional.pdf")
print("📄 Document includes: Company letterhead, resolution details, signature blocks, and verification code")
