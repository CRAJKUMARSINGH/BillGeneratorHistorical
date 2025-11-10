"""
HTML to PDF Visual Comparison Tool
Generates side-by-side comparison of HTML templates and their PDF outputs
"""

import os
import sys
from pathlib import Path
from pypdf import PdfReader
from jinja2 import Environment, FileSystemLoader
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.pdf_generator_optimized import PDFGenerator


def create_sample_data():
    """Create comprehensive sample data for all templates"""
    return {
        "header": [
            ["Agreement No.", "TEST-2025-001"],
            ["Name of Work", "Construction of Road Bridge"],
            ["Name of Contractor", "ABC Construction Ltd."],
            ["Date", "10-11-2025"]
        ],
        "items": [
            {
                "unit": "Cum",
                "quantity": "150.50",
                "quantity_since_last": "50.00",
                "quantity_upto_date": "150.50",
                "serial_no": "1",
                "description": "Excavation in Hard Strata including dressing and disposal",
                "rate": "850.00",
                "amount": "127,925.00",
                "amount_previous": "42,500.00",
                "remark": "As per specification",
                "bold": False,
                "underline": False,
                "is_divider": False
            },
            {
                "unit": "Sqm",
                "quantity": "200.00",
                "quantity_since_last": "100.00",
                "quantity_upto_date": "200.00",
                "serial_no": "2",
                "description": "Providing and laying PCC M15 grade",
                "rate": "1,200.00",
                "amount": "240,000.00",
                "amount_previous": "120,000.00",
                "remark": "Quality checked",
                "bold": False,
                "underline": False,
                "is_divider": False
            },
            {
                "unit": "MT",
                "quantity": "5.50",
                "quantity_since_last": "2.50",
                "quantity_upto_date": "5.50",
                "serial_no": "3",
                "description": "Reinforcement Steel Fe 500 Grade including cutting, bending",
                "rate": "65,000.00",
                "amount": "357,500.00",
                "amount_previous": "162,500.00",
                "remark": "ISI marked",
                "bold": False,
                "underline": False,
                "is_divider": False
            }
        ],
        "totals": {
            "grand_total": "725,425.00",
            "premium": {
                "percent": 0.05,
                "amount": "36,271.25"
            },
            "payable": "761,696.25",
            "extra_items_sum": 0
        },
        "summary": {
            "work_order_total": "800,000.00",
            "executed_total": "761,696.25",
            "overall_excess": "0.00",
            "overall_saving": "38,303.75",
            "premium": {"percent": 0.05},
            "tender_premium_f": "40,000.00",
            "tender_premium_h": "38,084.81",
            "tender_premium_j": "0.00",
            "tender_premium_l": "1,915.19",
            "grand_total_f": "840,000.00",
            "grand_total_h": "799,781.06",
            "grand_total_j": "0.00",
            "grand_total_l": "40,218.94",
            "net_difference": -38303.75
        },
        "agreement_no": "TEST-2025-001",
        "name_of_work": "Construction of Road Bridge over River XYZ",
        "name_of_firm": "ABC Construction Ltd.",
        "date_commencement": "01/01/2025",
        "date_completion": "31/12/2025",
        "actual_completion": "15/11/2025",
        "work_order_amount": 800000,
        "extra_item_amount": 0,
        "notes": [
            "1. All measurements have been verified by Junior Engineer on 05/11/2025",
            "2. Quality tests conducted as per IS specifications",
            "3. Work executed as per approved drawings",
            "4. No deviation from original specifications",
            "5. Contractor has maintained satisfactory progress"
        ],
        "payable_amount": "761,696.25",
        "amount_words": "Seven Lakh Sixty One Thousand Six Hundred Ninety Six Rupees and Twenty Five Paise Only"
    }


def generate_html_preview(template_name, data, output_dir="test_outputs/html_previews"):
    """Generate HTML preview file"""
    os.makedirs(output_dir, exist_ok=True)
    
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    html_content = template.render(data=data)
    
    html_path = os.path.join(output_dir, template_name)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_path, html_content


def generate_pdf_from_html(html_content, template_name, output_dir="test_outputs/pdf_outputs"):
    """Generate PDF from HTML content"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine orientation
    orientation = "landscape" if "deviation" in template_name else "portrait"
    
    # Special margins for note sheet
    custom_margins = None
    if "note_sheet" in template_name:
        custom_margins = {"top": 6, "right": 6, "bottom": 15, "left": 6}
    
    pdf_gen = PDFGenerator(orientation=orientation, custom_margins=custom_margins)
    pdf_path = os.path.join(output_dir, template_name.replace('.html', '.pdf'))
    
    success = pdf_gen.generate_pdf(html_content, pdf_path)
    
    return pdf_path if success else None


def analyze_pdf_content(pdf_path):
    """Extract and analyze PDF content"""
    try:
        reader = PdfReader(pdf_path)
        analysis = {
            "page_count": len(reader.pages),
            "pages": []
        }
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            analysis["pages"].append({
                "page_num": i + 1,
                "text_length": len(text) if text else 0,
                "text_preview": text[:500] if text else "",
                "width": float(page.mediabox.width),
                "height": float(page.mediabox.height)
            })
        
        return analysis
    except Exception as e:
        return {"error": str(e)}


def compare_html_pdf(template_name):
    """Compare HTML and PDF for a specific template"""
    print(f"\n{'='*80}")
    print(f"COMPARING: {template_name}")
    print(f"{'='*80}\n")
    
    # Generate sample data
    data = create_sample_data()
    
    # Generate HTML
    print("📄 Generating HTML preview...")
    html_path, html_content = generate_html_preview(template_name, data)
    print(f"   ✅ HTML saved: {html_path}")
    print(f"   📏 HTML size: {len(html_content)} characters")
    
    # Generate PDF
    print("\n📑 Generating PDF...")
    pdf_path = generate_pdf_from_html(html_content, template_name)
    
    if pdf_path and os.path.exists(pdf_path):
        print(f"   ✅ PDF saved: {pdf_path}")
        print(f"   📏 PDF size: {os.path.getsize(pdf_path)} bytes")
        
        # Analyze PDF
        print("\n🔍 Analyzing PDF content...")
        analysis = analyze_pdf_content(pdf_path)
        
        if "error" in analysis:
            print(f"   ❌ Error: {analysis['error']}")
        else:
            print(f"   📄 Pages: {analysis['page_count']}")
            for page_info in analysis["pages"]:
                print(f"   📄 Page {page_info['page_num']}:")
                print(f"      - Dimensions: {page_info['width']:.1f} x {page_info['height']:.1f} pt")
                print(f"      - Text length: {page_info['text_length']} characters")
                if page_info['text_length'] == 0:
                    print(f"      ⚠️  WARNING: No text extracted from this page!")
                else:
                    print(f"      ✅ Text preview: {page_info['text_preview'][:100]}...")
        
        return {
            "template": template_name,
            "html_path": html_path,
            "html_size": len(html_content),
            "pdf_path": pdf_path,
            "pdf_size": os.path.getsize(pdf_path),
            "pdf_analysis": analysis,
            "status": "success"
        }
    else:
        print(f"   ❌ PDF generation failed!")
        return {
            "template": template_name,
            "html_path": html_path,
            "html_size": len(html_content),
            "status": "failed"
        }


def main():
    """Run comprehensive HTML-PDF comparison"""
    print(f"\n{'#'*80}")
    print(f"# HTML TO PDF COMPARISON TOOL")
    print(f"{'#'*80}\n")
    
    templates = [
        "first_page.html",
        "deviation_statement.html",
        "note_sheet.html",
        "last_page.html",
        "extra_items.html"
    ]
    
    results = []
    
    for template in templates:
        try:
            result = compare_html_pdf(template)
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error processing {template}: {str(e)}")
            results.append({
                "template": template,
                "status": "error",
                "error": str(e)
            })
    
    # Generate summary report
    print(f"\n{'='*80}")
    print(f"SUMMARY REPORT")
    print(f"{'='*80}\n")
    
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "failed"]
    errors = [r for r in results if r.get("status") == "error"]
    
    print(f"✅ Successful: {len(successful)}/{len(templates)}")
    print(f"❌ Failed: {len(failed)}/{len(templates)}")
    print(f"⚠️  Errors: {len(errors)}/{len(templates)}")
    
    if failed:
        print(f"\n❌ Failed templates:")
        for r in failed:
            print(f"   - {r['template']}")
    
    if errors:
        print(f"\n⚠️  Error templates:")
        for r in errors:
            print(f"   - {r['template']}: {r.get('error', 'Unknown error')}")
    
    # Save detailed report
    report_path = "test_outputs/html_pdf_comparison_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved: {report_path}")
    print(f"\n✅ HTML previews: test_outputs/html_previews/")
    print(f"✅ PDF outputs: test_outputs/pdf_outputs/")


if __name__ == "__main__":
    main()
