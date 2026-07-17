import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

def download_font():
    # Using a reliable direct Google Fonts production mirror
    font_url = "https://fonts.gstatic.com/s/ubuntumono/v15/KFOjCn_WD_-9unN_6x7b_g785Iv_Z_p72A.ttf"
    font_path = "UbuntuMono-Bold.ttf"
    if not os.path.exists(font_path):
        print("[+] Fetching professional terminal font from stable mirror...")
        try:
            # Set a standard User-Agent header so the request isn't blocked
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(font_url, font_path)
        except Exception as e:
            print(f"[!] Mirror download failed: {e}. Falling back to default font layout.")
            return None
    return font_path

def generate_test_certificate(student_name, certificate_id):
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), color=(15, 18, 20))
    draw = ImageDraw.Draw(image)
    
    font_path = download_font()
    
    # Font setup with safety fallback
    if font_path and os.path.exists(font_path):
        font_header = ImageFont.truetype(font_path, 54)
        font_title = ImageFont.truetype(font_path, 76)
        font_name = ImageFont.truetype(font_path, 84)
        font_body = ImageFont.truetype(font_path, 34)
        font_footer = ImageFont.truetype(font_path, 28)
    else:
        # Emergency backup font loader built into Pillow
        print("[-] Using system default fonts layout.")
        font_header = font_title = font_name = font_body = font_footer = ImageFont.load_default()
    
    border_color = (0, 255, 120)
    draw.rectangle([40, 40, width - 40, height - 40], outline=border_color, width=4)
    draw.rectangle([50, 50, width - 50, height - 50], outline=(40, 50, 55), width=2)
    
    draw.text((960, 150), "HUMBU COMMUNITY NEXUS", fill=(255, 255, 255), font=font_header, anchor="mm")
    draw.text((960, 240), "CERTIFICATE OF COMPLETION", fill=border_color, font=font_title, anchor="mm")
    
    draw.text((960, 380), "This sovereign credential explicitly verifies that terminal operator:", fill=(170, 185, 195), font=font_body, anchor="mm")
    
    draw.text((960, 490), student_name.upper(), fill=(255, 255, 255), font=font_name, anchor="mm")
    
    competency_text = (
        "has successfully completed the intensive 60-day technical curriculum\n"
        "ACADEMIC SERIES VOL. 1: LOW-LEVEL SYSTEMS & PYTHON AUTOMATION\n\n"
        "Demonstrating verified terminal proficiency in:\n"
        "• Local Linux Terminal Orchestration & Environment Sanitization\n"
        "• Advanced Network Reconnaissance, Scanning & Protocol Auditing\n"
        "• Sovereign Python Engine Development & Socket Automation"
    )
    draw.text((960, 680), competency_text, fill=(180, 190, 195), font=font_body, anchor="mm", align="center")
    
    draw.line([300, 850, width - 300, 850], fill=(40, 50, 55), width=2)
    
    draw.text((350, 920), "ISSUED BY:\nHumbulani Mudau\nCEO & Director", fill=(255, 255, 255), font=font_footer)
    draw.text((350, 1000), "Humbu Wandeme Trading Enterprise", fill=border_color, font=font_footer)
    
    draw.text((1200, 920), f"VERIFICATION ID: {certificate_id}\nDATE: August 2026\nSTATUS: VERIFIED OPERATOR", fill=(130, 145, 155), font=font_footer)
    
    output_path = "nexus_test_certificate.png"
    image.save(output_path)
    print(f"\n[+] Success! Test certificate saved locally as: '{output_path}'")

if __name__ == "__main__":
    generate_test_certificate("Wandeme Ondwela", "NEXUS-2026-89A7X")
