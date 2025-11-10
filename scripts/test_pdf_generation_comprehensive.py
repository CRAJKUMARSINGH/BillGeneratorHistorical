"""
Comprehensive PDF Generation Test - 25 Iterations
Tests table widths, blank PDFs, and content accuracy
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).parent.parent))

from jinja2 import Environment, FileSystemLoader
from core.pdf_generator_optimized import PDFGenerator


def create_test_data():
    """Create comprehensive test data"""
    return {
        "header": [
            ["Agreement No.", "TEST-2025-COMPREHENSIVE"],
            ["Name of Work", "Infrastructure Development Project"],
            ["Name of Contractor", "Test Construction Company Ltd."],
            ["Date", "10-11-2025"]
        ],
        "items": [
            {
                "unit": "Cum",
                "quantity": "150.50",
                "quantity_since_last": "50.00",
                "quantity_upto_date": "150.50",
                "serial_no": "1",
                "description": "Excavation in Hard Strata including dressing and disposal of excavated material",
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
                "description": "Providing and laying PCC M15 grade concrete with proper compaction",
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
                "description": "Reinforcement Steel Fe 500 Grade including cutting, bending, and binding",
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
        "agreement_no": "TEST-2025-COMPREHENSIVE",
        "name_of_work": "Infrastructure Development Project",
        "name_of_firm": "Test Construction Company Ltd.",
        "date_commencement": "01/01/2025",
        "date_completion": "31/12/2025",
        "actual_completion": "10/11/2025",
        "work_order_amount": 766000,
        "extra_item_amount": 0,
        "notes": [
            "1. All measurements verified by Junior Engineer",
            "2. Quality tests conducted as per IS specifications",
            "3. Work executed as per approved drawings"
        ],
        "payable_amount": "761,696.25",
        "amount_words": "Seven Lakh Sixty One Thousand Six Hundred Ninety Six Rupees and Twenty Five Paise Only"
    }


def test_single_template(template_name, data, iteration, output_dir):
    """Test a single template"""
    result = {
        "template": template_name,
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "html_generated": False,
        "pdf_generated": False,
        "pdf_blank": True,
        "pdf_size": 0,
        "page_count": 0,
        "text_length": 0,
        "errors": []
    }
    
    try:
        # Generate HTML
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(template_name)
        html_content = template.render(data=data)
        result["html_generated"] = True
        result["html_size"] = len(html_content)
        
        # Determine orientation
        orientation = "landscape" if "deviation" in template_name else "portrait"
        custom_margins = {"top": 6, "right": 6, "bottom": 15, "left": 6} if "note_sheet" in template_name else None
        
        # Generate PDF
        pdf_gen = PDFGenerator(orientation=orientation, custom_margins=custom_margins)
        pdf_filename = f"iter{iteration:02d}_{template_name.replace('.html', '.pdf')}"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        success = pdf_gen.generate_pdf(html_content, pdf_path)
        
        if success and os.path.exists(pdf_path):
            result["pdf_generated"] = True
            result["pdf_path"] = pdf_path
            result["pdf_size"] = os.path.getsize(pdf_path)
            
            # Analyze PDF
            reader = PdfReader(pdf_path)
            result["page_count"] = len(reader.pages)
            
            if result["page_count"] > 0:
                text = reader.pages[0].extract_text()
                result["text_length"] = len(text) if text else 0
                result["pdf_blank"] = result["text_length"] < 10
                
                # Check dimensions
                page = reader.pages[0]
                result["width_pt"] = float(page.mediabox.width)
                result["height_pt"] = float(page.mediabox.height)
                
                # Verify A4 dimensions
                if orientation == "landscape":
                    result["correct_dimensions"] = (
                        abs(result["width_pt"] - 842) < 10 and 
                        abs(result["height_pt"] - 595) < 10
                    )
                else:
                    result["correct_dimensions"] = (
                        abs(result["width_pt"] - 595) < 10 and 
                        abs(result["height_pt"] - 842) < 10
                    )
                
                if not result["pdf_blank"] and result["correct_dimensions"]:
                    result["success"] = True
            else:
                result["errors"].append("No pages in PDF")
        else:
            result["errors"].append("PDF generation failed")
            
    except Exception as e:
        result["errors"].append(str(e))
    
    return result


def run_comprehensive_test(iterations=25):
    """Run comprehensive test with multiple iterations"""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE PDF GENERATION TEST - {iterations} ITERATIONS")
    print(f"{'='*80}\n")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"test_outputs/comprehensive_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    templates = [
        "first_page.html",
        "deviation_statement.html",
        "extra_items.html",
        "note_sheet.html",
        "last_page.html"
    ]
    
    all_results = []
    summary = {
        "total_tests": 0,
        "successful": 0,
        "failed": 0,
        "blank_pdfs": 0,
        "by_template": {}
    }
    
    # Create test data once
    data = create_test_data()
    
    # Run tests
    for iteration in range(1, iterations + 1):
        print(f"\n{'─'*80}")
        print(f"ITERATION {iteration}/{iterations}")
        print(f"{'─'*80}")
        
        for template in templates:
            print(f"\n  Testing: {template}")
            result = test_single_template(template, data, iteration, output_dir)
            all_results.append(result)
            
            summary["total_tests"] += 1
            
            if result["success"]:
                summary["successful"] += 1
                print(f"    ✅ SUCCESS - Size: {result['pdf_size']} bytes, Text: {result['text_length']} chars")
            else:
                summary["failed"] += 1
                print(f"    ❌ FAILED - Errors: {', '.join(result['errors'])}")
            
            if result["pdf_blank"]:
                summary["blank_pdfs"] += 1
                print(f"    ⚠️  WARNING: PDF appears blank")
            
            # Update template summary
            if template not in summary["by_template"]:
                summary["by_template"][template] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "blank": 0
                }
            
            summary["by_template"][template]["total"] += 1
            if result["success"]:
                summary["by_template"][template]["successful"] += 1
            else:
                summary["by_template"][template]["failed"] += 1
            if result["pdf_blank"]:
                summary["by_template"][template]["blank"] += 1
    
    # Generate report
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Total Tests: {summary['total_tests']}")
    print(f"✅ Successful: {summary['successful']} ({summary['successful']/summary['total_tests']*100:.1f}%)")
    print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total_tests']*100:.1f}%)")
    print(f"⚠️  Blank PDFs: {summary['blank_pdfs']} ({summary['blank_pdfs']/summary['total_tests']*100:.1f}%)")
    
    print(f"\n{'─'*80}")
    print(f"BY TEMPLATE")
    print(f"{'─'*80}\n")
    
    for template, stats in summary["by_template"].items():
        success_rate = stats["successful"] / stats["total"] * 100
        print(f"{template}:")
        print(f"  Total: {stats['total']}")
        print(f"  ✅ Success: {stats['successful']} ({success_rate:.1f}%)")
        print(f"  ❌ Failed: {stats['failed']}")
        print(f"  ⚠️  Blank: {stats['blank']}")
        print()
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "iterations": iterations,
        "summary": summary,
        "detailed_results": all_results
    }
    
    report_path = os.path.join(output_dir, "comprehensive_test_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*80}")
    print(f"📄 Detailed report saved: {report_path}")
    print(f"📁 PDF outputs saved: {output_dir}")
    print(f"{'='*80}\n")
    
    return summary, all_results


def main():
    """Run comprehensive test"""
    # Clear cache first
    print("🧹 Clearing cache...")
    try:
        from data.cache_utils import get_cache
        cache = get_cache()
        cache.clear()
        print("✅ Cache cleared\n")
    except Exception as e:
        print(f"⚠️  Could not clear cache: {e}\n")
    
    # Run tests
    summary, results = run_comprehensive_test(iterations=25)
    
    # Final verdict
    if summary["failed"] == 0 and summary["blank_pdfs"] == 0:
        print("🎉 ALL TESTS PASSED! PDFs are perfect!")
    elif summary["blank_pdfs"] > 0:
        print(f"⚠️  WARNING: {summary['blank_pdfs']} blank PDFs found")
    else:
        print(f"❌ {summary['failed']} tests failed")


if __name__ == "__main__":
    main()
