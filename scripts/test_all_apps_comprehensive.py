"""
Comprehensive Test for ALL Stream Bill Apps
Tests all apps, compares HTML vs PDF, ensures no blank outputs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from jinja2 import Environment, FileSystemLoader

# All apps to test
APPS = [
    r"C:\Users\Rajkumar\Stream-Bill-App_Main",
    r"C:\Users\Rajkumar\Stream-Bill-FIRST-ONE",
    r"C:\Users\Rajkumar\Stream-Bill-Generator-SAPNA",
    r"C:\Users\Rajkumar\Stream-Bill-INIT-PY",
    r"C:\Users\Rajkumar\Stream-Bill-generator-main",
    r"C:\Users\Rajkumar\Stream-Bill-generator-main2",
    r"C:\Users\Rajkumar\Streamlit_Bill_Historical",
    r"C:\Users\Rajkumar\Streamlit_Bill_New"
]

# Templates to test
TEMPLATES = [
    "first_page.html",
    "deviation_statement.html",
    "extra_items.html",
    "note_sheet.html",
    "last_page.html"
]


def create_comprehensive_test_data():
    """Create comprehensive test data with all fields"""
    return {
        "header": [
            ["Agreement No.", "COMPREHENSIVE-TEST-2025"],
            ["Name of Work", "Complete Infrastructure Development Project"],
            ["Name of Contractor", "Test Construction Company Limited"],
            ["Date", "10-11-2025"]
        ],
        "items": [
            {
                "unit": "Cum",
                "quantity": "150.50",
                "quantity_since_last": "50.00",
                "quantity_upto_date": "150.50",
                "serial_no": "1",
                "description": "Excavation in Hard Strata including dressing and disposal of excavated material with proper safety measures",
                "rate": "850.00",
                "amount": "127,925.00",
                "amount_previous": "42,500.00",
                "remark": "As per specification",
                "bold": False,
                "underline": False,
                "is_divider": False,
                "qty_wo": "160.00",
                "amt_wo": "136,000.00",
                "qty_bill": "150.50",
                "amt_bill": "127,925.00",
                "excess_qty": "0.00",
                "excess_amt": "0.00",
                "saving_qty": "9.50",
                "saving_amt": "8,075.00"
            },
            {
                "unit": "Sqm",
                "quantity": "200.00",
                "quantity_since_last": "100.00",
                "quantity_upto_date": "200.00",
                "serial_no": "2",
                "description": "Providing and laying PCC M15 grade concrete with proper compaction and curing",
                "rate": "1,200.00",
                "amount": "240,000.00",
                "amount_previous": "120,000.00",
                "remark": "Quality checked",
                "bold": False,
                "underline": False,
                "is_divider": False,
                "qty_wo": "200.00",
                "amt_wo": "240,000.00",
                "qty_bill": "200.00",
                "amt_bill": "240,000.00",
                "excess_qty": "0.00",
                "excess_amt": "0.00",
                "saving_qty": "0.00",
                "saving_amt": "0.00"
            },
            {
                "unit": "MT",
                "quantity": "5.50",
                "quantity_since_last": "2.50",
                "quantity_upto_date": "5.50",
                "serial_no": "3",
                "description": "Reinforcement Steel Fe 500 Grade including cutting, bending, binding and placing in position",
                "rate": "65,000.00",
                "amount": "357,500.00",
                "amount_previous": "162,500.00",
                "remark": "ISI marked",
                "bold": False,
                "underline": False,
                "is_divider": False,
                "qty_wo": "6.00",
                "amt_wo": "390,000.00",
                "qty_bill": "5.50",
                "amt_bill": "357,500.00",
                "excess_qty": "0.00",
                "excess_amt": "0.00",
                "saving_qty": "0.50",
                "saving_amt": "32,500.00"
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
            "work_order_total": "766,000.00",
            "executed_total": "725,425.00",
            "overall_excess": "0.00",
            "overall_saving": "40,575.00",
            "premium": {"percent": 0.05},
            "tender_premium_f": "38,300.00",
            "tender_premium_h": "36,271.25",
            "tender_premium_j": "0.00",
            "tender_premium_l": "2,028.75",
            "grand_total_f": "804,300.00",
            "grand_total_h": "761,696.25",
            "grand_total_j": "0.00",
            "grand_total_l": "42,603.75",
            "net_difference": -40575.00
        },
        "agreement_no": "COMPREHENSIVE-TEST-2025",
        "name_of_work": "Complete Infrastructure Development Project",
        "name_of_firm": "Test Construction Company Limited",
        "date_commencement": "01/01/2025",
        "date_completion": "31/12/2025",
        "actual_completion": "10/11/2025",
        "work_order_amount": 766000,
        "extra_item_amount": 0,
        "notes": [
            "1. All measurements verified by Junior Engineer on 05/11/2025",
            "2. Quality tests conducted as per IS specifications",
            "3. Work executed as per approved drawings and specifications",
            "4. No deviation from original work order",
            "5. Contractor has maintained satisfactory progress throughout"
        ],
        "payable_amount": "761,696.25",
        "amount_words": "Seven Lakh Sixty One Thousand Six Hundred Ninety Six Rupees and Twenty Five Paise Only"
    }


def test_app_template(app_path, app_name, template_name, data, output_dir):
    """Test a single template in a single app"""
    result = {
        "app": app_name,
        "template": template_name,
        "timestamp": datetime.now().isoformat(),
        "html_generated": False,
        "html_size": 0,
        "pdf_generated": False,
        "pdf_size": 0,
        "pdf_blank": True,
        "page_count": 0,
        "text_length": 0,
        "correct_dimensions": False,
        "errors": []
    }
    
    try:
        # Check if templates directory exists
        templates_dir = os.path.join(app_path, "templates")
        if not os.path.exists(templates_dir):
            result["errors"].append("Templates directory not found")
            return result
        
        # Check if template exists
        template_path = os.path.join(templates_dir, template_name)
        if not os.path.exists(template_path):
            result["errors"].append(f"Template not found: {template_name}")
            return result
        
        # Generate HTML
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template(template_name)
        html_content = template.render(data=data)
        result["html_generated"] = True
        result["html_size"] = len(html_content)
        
        # Save HTML for comparison
        html_filename = f"{app_name}_{template_name}"
        html_path = os.path.join(output_dir, "html", html_filename)
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        result["html_path"] = html_path
        
        # Generate PDF
        try:
            # Import PDF generator from the app
            sys.path.insert(0, app_path)
            from core.pdf_generator_optimized import PDFGenerator
            
            # Determine orientation
            orientation = "landscape" if "deviation" in template_name else "portrait"
            custom_margins = {"top": 6, "right": 6, "bottom": 15, "left": 6} if "note_sheet" in template_name else None
            
            pdf_gen = PDFGenerator(orientation=orientation, custom_margins=custom_margins)
            pdf_filename = f"{app_name}_{template_name.replace('.html', '.pdf')}"
            pdf_path = os.path.join(output_dir, "pdf", pdf_filename)
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            
            success = pdf_gen.generate_pdf(html_content, pdf_path)
            
            if success and os.path.exists(pdf_path):
                result["pdf_generated"] = True
                result["pdf_size"] = os.path.getsize(pdf_path)
                result["pdf_path"] = pdf_path
                
                # Analyze PDF
                reader = PdfReader(pdf_path)
                result["page_count"] = len(reader.pages)
                
                if result["page_count"] > 0:
                    text = reader.pages[0].extract_text()
                    result["text_length"] = len(text) if text else 0
                    result["pdf_blank"] = result["text_length"] < 10
                    
                    # Check dimensions
                    page = reader.pages[0]
                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)
                    result["width_pt"] = width
                    result["height_pt"] = height
                    
                    # Verify A4 dimensions
                    if orientation == "landscape":
                        result["correct_dimensions"] = (abs(width - 842) < 10 and abs(height - 595) < 10)
                    else:
                        result["correct_dimensions"] = (abs(width - 595) < 10 and abs(height - 842) < 10)
                    
                    if result["pdf_blank"]:
                        result["errors"].append("PDF appears blank (text < 10 chars)")
                    if not result["correct_dimensions"]:
                        result["errors"].append(f"Incorrect dimensions: {width}x{height}")
                else:
                    result["errors"].append("No pages in PDF")
            else:
                result["errors"].append("PDF generation failed")
                
        except Exception as e:
            result["errors"].append(f"PDF generation error: {str(e)}")
            
    except Exception as e:
        result["errors"].append(f"Template rendering error: {str(e)}")
    
    return result


def test_all_apps():
    """Test all apps with all templates"""
    print(f"\n{'='*100}")
    print(f"{'COMPREHENSIVE TEST - ALL APPS':^100}")
    print(f"{'='*100}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"test_outputs/all_apps_test_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    data = create_comprehensive_test_data()
    all_results = []
    
    summary = {
        "total_tests": 0,
        "successful": 0,
        "failed": 0,
        "blank_pdfs": 0,
        "html_generated": 0,
        "pdf_generated": 0,
        "by_app": {},
        "by_template": {}
    }
    
    # Test each app
    for app_path in APPS:
        app_name = os.path.basename(app_path)
        
        if not os.path.exists(app_path):
            print(f"⚠️  Skipping {app_name} - not found")
            continue
        
        print(f"\n{'─'*100}")
        print(f"Testing: {app_name}")
        print(f"{'─'*100}")
        
        summary["by_app"][app_name] = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "blank": 0
        }
        
        # Test each template
        for template_name in TEMPLATES:
            print(f"\n  📄 {template_name}...", end=" ")
            
            result = test_app_template(app_path, app_name, template_name, data, output_dir)
            all_results.append(result)
            
            summary["total_tests"] += 1
            summary["by_app"][app_name]["total"] += 1
            
            if template_name not in summary["by_template"]:
                summary["by_template"][template_name] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "blank": 0
                }
            summary["by_template"][template_name]["total"] += 1
            
            # Evaluate result
            if result["html_generated"]:
                summary["html_generated"] += 1
            
            if result["pdf_generated"]:
                summary["pdf_generated"] += 1
            
            if result["pdf_blank"]:
                summary["blank_pdfs"] += 1
                summary["by_app"][app_name]["blank"] += 1
                summary["by_template"][template_name]["blank"] += 1
            
            if len(result["errors"]) == 0 and not result["pdf_blank"] and result["correct_dimensions"]:
                summary["successful"] += 1
                summary["by_app"][app_name]["successful"] += 1
                summary["by_template"][template_name]["successful"] += 1
                print(f"✅ OK (HTML: {result['html_size']} chars, PDF: {result['pdf_size']} bytes, Text: {result['text_length']} chars)")
            else:
                summary["failed"] += 1
                summary["by_app"][app_name]["failed"] += 1
                summary["by_template"][template_name]["failed"] += 1
                print(f"❌ FAILED")
                for error in result["errors"]:
                    print(f"     - {error}")
    
    # Generate summary report
    print(f"\n{'='*100}")
    print(f"{'SUMMARY REPORT':^100}")
    print(f"{'='*100}\n")
    
    print(f"Total Tests: {summary['total_tests']}")
    print(f"✅ Successful: {summary['successful']} ({summary['successful']/summary['total_tests']*100:.1f}%)")
    print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total_tests']*100:.1f}%)")
    print(f"⚠️  Blank PDFs: {summary['blank_pdfs']} ({summary['blank_pdfs']/summary['total_tests']*100:.1f}%)")
    print(f"📄 HTML Generated: {summary['html_generated']}/{summary['total_tests']}")
    print(f"📑 PDF Generated: {summary['pdf_generated']}/{summary['total_tests']}")
    
    # By app
    print(f"\n{'─'*100}")
    print(f"BY APP")
    print(f"{'─'*100}\n")
    
    for app_name, stats in summary["by_app"].items():
        success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
        status = "✅" if stats["failed"] == 0 and stats["blank"] == 0 else "❌"
        print(f"{status} {app_name}")
        print(f"   Total: {stats['total']}, Success: {stats['successful']} ({success_rate:.1f}%), Failed: {stats['failed']}, Blank: {stats['blank']}")
    
    # By template
    print(f"\n{'─'*100}")
    print(f"BY TEMPLATE")
    print(f"{'─'*100}\n")
    
    for template_name, stats in summary["by_template"].items():
        success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
        status = "✅" if stats["failed"] == 0 and stats["blank"] == 0 else "❌"
        print(f"{status} {template_name}")
        print(f"   Total: {stats['total']}, Success: {stats['successful']} ({success_rate:.1f}%), Failed: {stats['failed']}, Blank: {stats['blank']}")
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "detailed_results": all_results
    }
    
    report_path = os.path.join(output_dir, "all_apps_test_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*100}")
    print(f"📄 Detailed report: {report_path}")
    print(f"📁 HTML files: {os.path.join(output_dir, 'html')}")
    print(f"📁 PDF files: {os.path.join(output_dir, 'pdf')}")
    print(f"{'='*100}\n")
    
    # Final verdict
    if summary["blank_pdfs"] > 0:
        print(f"⚠️  WARNING: {summary['blank_pdfs']} BLANK PDFs FOUND!")
        print(f"   Check the report for details.")
    elif summary["failed"] > 0:
        print(f"⚠️  WARNING: {summary['failed']} TESTS FAILED!")
        print(f"   Check the report for details.")
    else:
        print(f"🎉 ALL TESTS PASSED! NO BLANK PDFs!")
    
    return summary, all_results


def main():
    """Run comprehensive test on all apps"""
    print(f"\n{'#'*100}")
    print(f"{'COMPREHENSIVE TEST - ALL STREAM BILL APPS':^100}")
    print(f"{'Testing all apps with all templates':^100}")
    print(f"{'Comparing HTML vs PDF, ensuring no blank outputs':^100}")
    print(f"{'#'*100}\n")
    
    summary, results = test_all_apps()
    
    print(f"\n{'='*100}")
    print(f"TEST COMPLETE!")
    print(f"{'='*100}\n")


if __name__ == "__main__":
    main()
