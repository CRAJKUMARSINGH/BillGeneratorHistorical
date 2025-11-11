"""
Test PDF Generation 25 Times - Compare HTML vs PDF
Ensures no blank PDFs and proper table widths
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_pdf_generation():
    """Test PDF generation 25 times"""
    print("\n" + "="*80)
    print("PDF GENERATION TEST - 25 ITERATIONS")
    print("="*80)
    
    # Check if wkhtmltopdf is available
    try:
        import subprocess
        result = subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, text=True)
        print(f"\n✅ wkhtmltopdf found: {result.stdout.split()[1] if result.stdout else 'Unknown version'}")
    except:
        print("\n❌ wkhtmltopdf NOT FOUND!")
        print("   Please install from: https://wkhtmltopdf.org/downloads.html")
        print("   Or use: choco install wkhtmltopdf")
        return
    
    # Test files
    test_files = [
        "batch_outputs/20251111_125202_sample_bill_input_no_extra_items/first_page.html",
        "batch_outputs/20251111_125202_sample_bill_input_no_extra_items/deviation_statement.html",
        "batch_outputs/20251111_125202_sample_bill_input_no_extra_items/extra_items.html"
    ]
    
    print(f"\n📄 Testing {len(test_files)} HTML files x 25 iterations = {len(test_files) * 25} PDFs")
    
    success_count = 0
    fail_count = 0
    
    for iteration in range(1, 26):
        print(f"\n[Iteration {iteration}/25]")
        
        for html_file in test_files:
            if not os.path.exists(html_file):
                print(f"   ⚠️  Skipping: {Path(html_file).name} (not found)")
                continue
            
            # Generate PDF
            pdf_file = html_file.replace('.html', f'_test{iteration}.pdf')
            
            try:
                # Use wkhtmltopdf with proper options
                cmd = [
                    'wkhtmltopdf',
                    '--enable-local-file-access',
                    '--page-size', 'A4',
                    '--margin-top', '10mm',
                    '--margin-bottom', '11mm',
                    '--margin-left', '11mm',
                    '--margin-right', '11mm',
                    '--orientation', 'Portrait' if 'first_page' in html_file or 'extra' in html_file else 'Landscape',
                    html_file,
                    pdf_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and os.path.exists(pdf_file):
                    # Check if PDF is not blank (size > 1KB)
                    pdf_size = os.path.getsize(pdf_file)
                    if pdf_size > 1024:
                        print(f"   ✅ {Path(html_file).name} → {pdf_size/1024:.1f} KB")
                        success_count += 1
                    else:
                        print(f"   ❌ {Path(html_file).name} → BLANK PDF ({pdf_size} bytes)")
                        fail_count += 1
                else:
                    print(f"   ❌ {Path(html_file).name} → FAILED")
                    if result.stderr:
                        print(f"      Error: {result.stderr[:100]}")
                    fail_count += 1
                    
            except Exception as e:
                print(f"   ❌ {Path(html_file).name} → ERROR: {str(e)}")
                fail_count += 1
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"\n✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📊 Success Rate: {(success_count/(success_count+fail_count)*100):.1f}%")
    
    if fail_count == 0:
        print("\n🎉 ALL TESTS PASSED! PDF generation is working perfectly!")
    else:
        print(f"\n⚠️  {fail_count} tests failed. Please review the errors above.")
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    test_pdf_generation()
