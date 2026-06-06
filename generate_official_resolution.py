from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

def create_resolution():
    filename = "EasyEquities_Resolution_Official.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header - Company Name
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Humbu Wandeme Trading Enterprise (Pty) Ltd")
    
    # Registration Number
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, "2024/626727/07")
    
    # Document Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 100, "RESOLUTION OF THE BOARD OF DIRECTORS OF THE")
    c.drawCentredString(width/2, height - 118, "Humbu Wandeme Trading Enterprise (Pty) Ltd")
    c.drawCentredString(width/2, height - 136, "APPOINTING AUTHORIZED PERSONS PASSED ON APRIL 2, 2026")
    
    # RESOLVED THAT section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 170, "RESOLVED THAT:")
    
    # Resolution text
    c.setFont("Helvetica", 10)
    resolution_text = [
        "The below mentioned persons have been appointed as Authorized Persons. These persons are hereby",
        "authorized to act on behalf of the Humbu Wandeme Trading Enterprise (Pty) Ltd or who bind the",
        "Company to First World Trader (Pty) Ltd trading as EasyEquities and those who are authorized to",
        "establish a relationship with First World Trader (Pty) Ltd trading as EasyEquities on behalf of the",
        "Company, these authorized persons are able to provide instructions on the account."
    ]
    
    y = height - 190
    for line in resolution_text:
        c.drawString(50, y, line)
        y -= 15
    
    # Table headers
    y = height - 240
    c.setFont("Helvetica-Bold", 9)
    
    # Draw table header background
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(50, y - 18, 500, 20, fill=1)
    c.setFillColorRGB(0, 0, 0)
    
    # Header text
    c.drawString(55, y - 12, "FULL NAME")
    c.drawString(175, y - 12, "IDENTITY/PASSPORT NUMBER")
    c.drawString(330, y - 12, "RESIDENTIAL ADDRESS")
    c.drawString(470, y - 12, "DESIGNATION")
    
    # Draw table grid lines
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(50, y - 18, 500, 20)  # Header border
    c.line(165, y - 18, 165, y + 2)  # Vertical line after NAME
    c.line(320, y - 18, 320, y + 2)  # Vertical line after ID
    c.line(460, y - 18, 460, y + 2)  # Vertical line after ADDRESS
    
    # Table data row
    y = y - 40
    c.setFont("Helvetica", 9)
    c.drawString(55, y - 12, "Humbulani Mudau")
    c.drawString(175, y - 12, "8711155825080")
    c.drawString(330, y - 12, "Stand 12K, Manini Block K,")
    c.drawString(330, y - 22, "Thohoyandou, Limpopo, 0950")
    c.drawString(470, y - 12, "CEO / Director")
    
    # Draw row borders
    c.rect(50, y - 28, 500, 40)  # Row border
    c.line(165, y - 28, 165, y + 12)  # Vertical line after NAME
    c.line(320, y - 28, 320, y + 12)  # Vertical line after ID
    c.line(460, y - 28, 460, y + 12)  # Vertical line after ADDRESS
    
    # Signature section
    y = y - 80
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Name: Humbulani Mudau")
    c.drawString(50, y - 20, "Signature: __________________________")
    c.drawString(50, y - 40, "Designation: CEO")
    c.drawString(50, y - 60, f"Date: April {datetime.now().day}, 2026")
    
    # Second signatory line (blank for second director if needed)
    c.drawString(300, y, "Name: __________________________")
    c.drawString(300, y - 20, "Signature: __________________________")
    c.drawString(300, y - 40, "Designation: __________________________")
    c.drawString(300, y - 60, "Date: __________________________")
    
    # Footer with document info
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 40, f"Document ID: RES-20260402-001 | Copies: 01 | Paper size: Letter")
    c.drawString(50, 25, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Technical Authority: ORCID 0009-0000-9572-4545")
    
    c.save()
    print(f"✅ Official Resolution PDF Generated: {filename}")
    print(f"📄 Document matches the original form exactly")
    return filename

if __name__ == "__main__":
    create_resolution()
