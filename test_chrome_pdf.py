"""
Test Chrome Headless PDF Generation
"""
import subprocess
import os
from pathlib import Path

# Test HTML
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4 portrait; margin: 10mm; }
        body { font-family: Arial; font-size: 10pt; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th, td { border: 1px solid black; padding: 5px; }
        th { background-color: #2c3e50; color: white; }
    </style>
</head>
<body>
    <h1>TEST PDF - Chrome Headless</h1>
    <table>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
            <th>Column 3</th>
        </tr>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
            <td>Data 3</td>
        </tr>
    </table>
    <p>This PDF should have NO SHRINKING!</p>
</body>
</html>"""

# Save HTML
html_path = Path("test_chrome.html")
html_path.write_text(html_content, encoding='utf-8')

# Generate PDF with Chrome
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf_path = Path("test_chrome_output.pdf")

cmd = [
    chrome_exe,
    '--headless',
    '--disable-gpu',
    '--no-margins',
    '--disable-smart-shrinking',
    '--run-all-compositor-stages-before-draw',
    '--print-to-pdf=' + str(pdf_path.absolute()),
    'file:///' + str(html_path.absolute()).replace('\\', '/')
]

print("Running Chrome command:")
print(' '.join(cmd))
print()

result = subprocess.run(cmd, capture_output=True, timeout=30)

if result.returncode == 0 and pdf_path.exists():
    print(f"✅ SUCCESS! PDF generated: {pdf_path}")
    print(f"   File size: {pdf_path.stat().st_size} bytes")
else:
    print(f"❌ FAILED!")
    print(f"   Return code: {result.returncode}")
    print(f"   Stderr: {result.stderr.decode()}")
    print(f"   Stdout: {result.stdout.decode()}")

# Cleanup
if html_path.exists():
    html_path.unlink()
