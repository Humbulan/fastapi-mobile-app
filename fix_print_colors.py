import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the existing printCertificate function
match = re.search(r'function\s+printCertificate\s*\(\)\s*{', content)
if not match:
    print("❌ Could not find printCertificate function.")
    exit(1)
start = match.start()
# Find the matching closing brace
brace_count = 0
i = start
while i < len(content):
    if content[i] == '{':
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break
    i += 1
if brace_count != 0:
    print("❌ Unbalanced braces.")
    exit(1)

# Extract the current function body
func_body = content[start:end]

# Modify the print styles to force background colors
# Look for the @media print section inside the CSS
# We'll replace the .cert style to include color-adjust properties
# Also add them to body and .cert

new_css = '''
                        @media print {
                            body { padding:0; background:#0f1214 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            .cert { border:1px solid #00ff78; padding:10px 15px; background:#0f1214 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            .name { font-size:22px; }
                            .details { font-size:11px; }
                            .nexus { font-size:16px; }
                            .cert-title { font-size:14px; }
                            .course { font-size:13px; }
                        }'''

# Replace the old @media print block with the new one
# We'll find the existing @media print inside the function and replace it
import re as regex
func_body_updated = regex.sub(r'@media print\s*\{[^}]*\}', new_css, func_body, flags=regex.DOTALL)

if func_body_updated == func_body:
    # If not found, we'll manually insert it after the style block
    # But we can safely assume it's there, so we'll try a broader approach
    # Actually we can just replace the whole function body with a new one that includes the fix.
    # Simpler: we can rewrite the function completely with the fixed CSS.
    # Let's do that instead.

    # New function definition with fixed CSS
    new_func = '''        function printCertificate() {
            const name = document.getElementById('certificateName').textContent || "Student";
            const date = document.getElementById('certificateDate').textContent || new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const printWindow = window.open('', '_blank', 'width=800,height=600');
            if (!printWindow) {
                alert('Please allow pop-ups to print the certificate.');
                return;
            }
            printWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Humbu Nexus Certificate</title>
                    <style>
                        * { margin:0; padding:0; box-sizing:border-box; }
                        body { background:#0f1214; display:flex; justify-content:center; align-items:center; min-height:100vh; font-family:'Courier New', monospace; color:#fff; padding:10px; }
                        .cert { background:#0f1214; border:2px solid #00ff78; padding:15px 20px; max-width:750px; width:100%; border-radius:6px; text-align:center; }
                        .header { display:flex; justify-content:space-between; font-size:10px; color:#00ff78; border-bottom:1px solid #283237; padding-bottom:5px; margin-bottom:10px; text-transform:uppercase; }
                        .nexus { color:#00ff78; font-size:18px; letter-spacing:3px; }
                        .cert-title { font-size:16px; border-bottom:1px solid #283237; padding-bottom:6px; margin-bottom:10px; }
                        .sub { color:#aab9c3; font-size:12px; margin:4px 0; }
                        .name { font-size:26px; font-weight:bold; text-transform:uppercase; margin:8px 0; }
                        .course { color:#00ff78; font-size:14px; font-weight:bold; margin:6px 0; }
                        .details { text-align:left; max-width:400px; margin:8px auto; color:#d0dbe3; font-size:12px; line-height:1.6; padding-left:15px; list-style:none; }
                        .details li::before { content:"• "; color:#00ff78; }
                        .presented { font-size:12px; color:#82919b; margin:6px 0; }
                        .date { font-size:10px; color:#00ff78; margin-top:6px; }
                        .footer { margin-top:12px; border-top:1px solid #283237; padding-top:8px; font-size:10px; color:#6a7a85; }
                        @media print {
                            body { padding:0; background:#0f1214 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            .cert { border:1px solid #00ff78; padding:10px 15px; background:#0f1214 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            .name { font-size:22px; }
                            .details { font-size:11px; }
                            .nexus { font-size:16px; }
                            .cert-title { font-size:14px; }
                            .course { font-size:13px; }
                        }
                    </style>
                </head>
                <body>
                    <div class="cert">
                        <div class="header"><span>Save as PDF</span><span>Copies: 01</span><span>Paper size: Letter</span></div>
                        <div class="nexus">⚡ HUMBU COMMUNITY NEXUS ⚡</div>
                        <div class="cert-title">CERTIFICATE OF COMPLETION</div>
                        <div class="sub">This sovereign credential explicitly verifies that terminal operator:</div>
                        <div class="name">${name}</div>
                        <div class="sub">has successfully mastered the intensive 60‑day technical curriculum:</div>
                        <div class="course">ACADEMIC SERIES VOL. 1: LOW‑LEVEL SYSTEMS & PYTHON AUTOMATION</div>
                        <ul class="details">
                            <li>Local Linux Terminal Orchestration &amp; Environment Sanitization</li>
                            <li>Advanced Network Reconnaissance, Scanning &amp; Protocol Auditing</li>
                            <li>Sovereign Python Engine Development &amp; Socket Automation</li>
                        </ul>
                        <div class="presented">Presented by: <strong>Humbu Wandeme Trading Enterprise</strong></div>
                        <div class="date">${date}</div>
                        <div class="footer">Issued by: Humbulani Mudau, CEO &amp; Director</div>
                    </div>
                    <script>
                        window.onload = function() {
                            setTimeout(function() { window.print(); }, 300);
                        };
                    <\/script>
                </body>
                </html>
            `);
            printWindow.document.close();
        }'''

    # Replace the whole function
    content = content[:start] + new_func + content[end:]
else:
    # If we found and replaced the print block, we still need to replace the function with the updated body
    content = content[:start] + func_body_updated + content[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated printCertificate with forced background colors in print CSS.")
