"""
Comprehensive HTML to PDF Diagnostic Tool
Compares HTML templates with generated PDFs to identify distortion issues
"""

import os
import sys
from pathlib import Path
from pypdf import PdfReader
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jinja2 import Environment, FileSystemLoader
from core.pdf_generator_optimized import PDFGenerator


class PDFDiagnostics:
    """Diagnose PDF generation issues"""
    
    def __init__(self, output_dir="All_Outputs"):
        self.output_dir = output_dir
        self.template_dir = "templates"
        self.issues = []
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "pdfs_checked": 0,
            "blank_pdfs": [],
            "distorted_pdfs": [],
            "successful_pdfs": [],
            "issues": []
        }
    
    def check_pdf_blank(self, pdf_path):
        """Check if PDF is blank or has no content"""
        try:
            reader = PdfReader(pdf_path)
            
            if len(reader.pages) == 0:
                return True, "No pages in PDF"
            
            # Check first page for text content
            first_page = reader.pages[0]
            text = first_page.extract_text()
            
            if not text or len(text.strip()) < 10:
                return True, "No text content found"
            
            return False, "PDF has content"
            
        except Exception as e:
            return True, f"Error reading PDF: {str(e)}"
    
    def check_pdf_dimensions(self, pdf_path):
        """Check if PDF has correct A4 dimensions"""
        try:
            reader = PdfReader(pdf_path)
            page = reader.pages[0]
            
            # Get page dimensions in points (1 point = 1/72 inch)
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            # A4 dimensions in points
            A4_WIDTH_PT = 595.276  # 210mm
            A4_HEIGHT_PT = 841.890  # 297mm
            
            # Check portrait
            if abs(width - A4_WIDTH_PT) < 10 and abs(height - A4_HEIGHT_PT) < 10:
                return True, "portrait", width, height
            
            # Check landscape
            if abs(width - A4_HEIGHT_PT) < 10 and abs(height - A4_WIDTH_PT) < 10:
                return True, "landscape", width, height
            
            return False, "unknown", width, height
            
        except Exception as e:
            return False, "error", 0, 0
    
    def analyze_pdf(self, pdf_path):
        """Comprehensive PDF analysis"""
        analysis = {
            "path": pdf_path,
            "filename": os.path.basename(pdf_path),
            "exists": os.path.exists(pdf_path),
            "size_bytes": 0,
            "is_blank": False,
            "blank_reason": "",
            "has_correct_dimensions": False,
            "orientation": "",
            "width_pt": 0,
            "height_pt": 0,
            "page_count": 0,
            "text_length": 0,
            "issues": []
        }
        
        if not analysis["exists"]:
            analysis["issues"].append("File does not exist")
            return analysis
        
        analysis["size_bytes"] = os.path.getsize(pdf_path)
        
        if analysis["size_bytes"] < 100:
            analysis["issues"].append("File size too small (< 100 bytes)")
            analysis["is_blank"] = True
            return analysis
        
        # Check if blank
        is_blank, blank_reason = self.check_pdf_blank(pdf_path)
        analysis["is_blank"] = is_blank
        analysis["blank_reason"] = blank_reason
        
        if is_blank:
            analysis["issues"].append(f"Blank PDF: {blank_reason}")
        
        # Check dimensions
        has_correct_dims, orientation, width, height = self.check_pdf_dimensions(pdf_path)
        analysis["has_correct_dimensions"] = has_correct_dims
        analysis["orientation"] = orientation
        analysis["width_pt"] = width
        analysis["height_pt"] = height
        
        if not has_correct_dims:
            analysis["issues"].append(f"Incorrect dimensions: {width}x{height} pt")
        
        # Get page count and text length
        try:
            reader = PdfReader(pdf_path)
            analysis["page_count"] = len(reader.pages)
            
            if analysis["page_count"] > 0:
                text = reader.pages[0].extract_text()
                analysis["text_length"] = len(text) if text else 0
        except Exception as e:
            analysis["issues"].append(f"Error reading PDF: {str(e)}")
        
        return analysis
    
    def scan_all_pdfs(self):
        """Scan all PDFs in output directory"""
        print(f"\n{'='*80}")
        print(f"SCANNING ALL PDFs IN: {self.output_dir}")
        print(f"{'='*80}\n")
        
        pdf_files = []
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        print(f"Found {len(pdf_files)} PDF files\n")
        
        for pdf_path in pdf_files:
            self.report["pdfs_checked"] += 1
            analysis = self.analyze_pdf(pdf_path)
            
            # Categorize
            if analysis["is_blank"]:
                self.report["blank_pdfs"].append(analysis)
                print(f"❌ BLANK: {analysis['filename']}")
                print(f"   Reason: {analysis['blank_reason']}")
            elif len(analysis["issues"]) > 0:
                self.report["distorted_pdfs"].append(analysis)
                print(f"⚠️  ISSUES: {analysis['filename']}")
                for issue in analysis["issues"]:
                    print(f"   - {issue}")
            else:
                self.report["successful_pdfs"].append(analysis)
                print(f"✅ OK: {analysis['filename']}")
            
            print(f"   Size: {analysis['size_bytes']} bytes | Pages: {analysis['page_count']} | Text: {analysis['text_length']} chars")
            print(f"   Dimensions: {analysis['width_pt']:.1f}x{analysis['height_pt']:.1f} pt ({analysis['orientation']})")
            print()
    
    def test_template_rendering(self):
        """Test rendering each template with sample data"""
        print(f"\n{'='*80}")
        print(f"TESTING TEMPLATE RENDERING")
        print(f"{'='*80}\n")
        
        templates = [
            "first_page.html",
            "deviation_statement.html",
            "note_sheet.html",
            "last_page.html",
            "extra_items.html"
        ]
        
        env = Environment(loader=FileSystemLoader(self.template_dir))
        
        for template_name in templates:
            try:
                template = env.get_template(template_name)
                
                # Create minimal sample data
                sample_data = {
                    "header": [["Agreement No.", "TEST-001"], ["Date", "01/01/2025"]],
                    "items": [
                        {
                            "unit": "Cum",
                            "quantity": "100",
                            "serial_no": "1",
                            "description": "Test Item",
                            "rate": "500",
                            "amount": "50000",
                            "remark": "Test"
                        }
                    ],
                    "totals": {
                        "grand_total": "50000",
                        "premium": {"percent": 0.05, "amount": "2500"},
                        "payable": "52500"
                    },
                    "summary": {
                        "work_order_total": "50000",
                        "executed_total": "52500",
                        "overall_excess": "2500",
                        "overall_saving": "0",
                        "premium": {"percent": 0.05},
                        "tender_premium_f": "2500",
                        "tender_premium_h": "2625",
                        "tender_premium_j": "125",
                        "tender_premium_l": "0",
                        "grand_total_f": "52500",
                        "grand_total_h": "55125",
                        "grand_total_j": "2625",
                        "grand_total_l": "0",
                        "net_difference": 2500
                    },
                    "agreement_no": "TEST-001",
                    "name_of_work": "Test Work",
                    "name_of_firm": "Test Firm",
                    "date_commencement": "01/01/2025",
                    "date_completion": "31/12/2025",
                    "actual_completion": "31/12/2025",
                    "work_order_amount": 50000,
                    "notes": ["Test note 1", "Test note 2"]
                }
                
                # Render template
                html_content = template.render(data=sample_data)
                
                # Check HTML length
                if len(html_content) < 100:
                    print(f"❌ {template_name}: HTML too short ({len(html_content)} chars)")
                    self.report["issues"].append({
                        "template": template_name,
                        "issue": "HTML too short",
                        "length": len(html_content)
                    })
                else:
                    print(f"✅ {template_name}: Rendered successfully ({len(html_content)} chars)")
                
                # Try to generate PDF
                test_pdf_path = f"test_outputs/test_{template_name.replace('.html', '.pdf')}"
                os.makedirs("test_outputs", exist_ok=True)
                
                # Determine orientation
                orientation = "landscape" if "deviation" in template_name else "portrait"
                
                pdf_gen = PDFGenerator(orientation=orientation)
                success = pdf_gen.generate_pdf(html_content, test_pdf_path)
                
                if success and os.path.exists(test_pdf_path):
                    analysis = self.analyze_pdf(test_pdf_path)
                    if analysis["is_blank"]:
                        print(f"   ❌ PDF is BLANK: {analysis['blank_reason']}")
                        self.report["issues"].append({
                            "template": template_name,
                            "issue": "Generated PDF is blank",
                            "reason": analysis['blank_reason']
                        })
                    else:
                        print(f"   ✅ PDF generated successfully")
                else:
                    print(f"   ❌ PDF generation failed")
                    self.report["issues"].append({
                        "template": template_name,
                        "issue": "PDF generation failed"
                    })
                
            except Exception as e:
                print(f"❌ {template_name}: Error - {str(e)}")
                self.report["issues"].append({
                    "template": template_name,
                    "issue": str(e)
                })
            
            print()
    
    def generate_report(self):
        """Generate comprehensive diagnostic report"""
        print(f"\n{'='*80}")
        print(f"DIAGNOSTIC REPORT SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Total PDFs Checked: {self.report['pdfs_checked']}")
        print(f"✅ Successful: {len(self.report['successful_pdfs'])}")
        print(f"❌ Blank PDFs: {len(self.report['blank_pdfs'])}")
        print(f"⚠️  Distorted PDFs: {len(self.report['distorted_pdfs'])}")
        print(f"🔧 Template Issues: {len(self.report['issues'])}")
        
        # Save detailed report
        report_path = "test_outputs/pdf_diagnostic_report.json"
        os.makedirs("test_outputs", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Print blank PDFs
        if self.report['blank_pdfs']:
            print(f"\n{'='*80}")
            print(f"BLANK PDFs FOUND:")
            print(f"{'='*80}\n")
            for pdf in self.report['blank_pdfs']:
                print(f"❌ {pdf['filename']}")
                print(f"   Path: {pdf['path']}")
                print(f"   Reason: {pdf['blank_reason']}")
                print()
        
        # Print template issues
        if self.report['issues']:
            print(f"\n{'='*80}")
            print(f"TEMPLATE ISSUES:")
            print(f"{'='*80}\n")
            for issue in self.report['issues']:
                print(f"⚠️  Template: {issue.get('template', 'Unknown')}")
                print(f"   Issue: {issue.get('issue', 'Unknown')}")
                if 'reason' in issue:
                    print(f"   Reason: {issue['reason']}")
                print()


def main():
    """Run comprehensive diagnostics"""
    diagnostics = PDFDiagnostics()
    
    # Scan all existing PDFs
    diagnostics.scan_all_pdfs()
    
    # Test template rendering
    diagnostics.test_template_rendering()
    
    # Generate report
    diagnostics.generate_report()


if __name__ == "__main__":
    main()
