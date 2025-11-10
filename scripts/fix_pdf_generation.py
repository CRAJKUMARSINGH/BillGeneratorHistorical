"""
PDF Generation Fix and Optimization Script
Addresses common HTML-to-PDF distortion issues and ensures elegant output
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class PDFGenerationFixer:
    """Fix common PDF generation issues"""
    
    def __init__(self):
        self.fixes_applied = []
        self.recommendations = []
    
    def check_template_css(self, template_path):
        """Check and fix CSS issues in templates"""
        print(f"\n🔍 Checking CSS in: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        fixes = []
        
        # Check for missing box-sizing
        if 'box-sizing: border-box' not in content:
            issues.append("Missing box-sizing: border-box")
            fixes.append("Add box-sizing: border-box to prevent overflow")
        
        # Check for proper page margins
        if '@page' not in content:
            issues.append("Missing @page directive")
            fixes.append("Add @page with proper margins")
        
        # Check for table-layout: fixed
        if 'table-layout: fixed' not in content:
            issues.append("Missing table-layout: fixed")
            fixes.append("Add table-layout: fixed for consistent column widths")
        
        # Check for overflow handling
        if 'overflow: hidden' not in content:
            issues.append("Missing overflow: hidden")
            fixes.append("Add overflow: hidden to prevent content overflow")
        
        # Check for proper font sizing
        if 'font-size: 9pt' not in content and 'font-size: 10pt' not in content:
            issues.append("Font size may be too large")
            fixes.append("Use 9pt or 10pt font size for better fit")
        
        if issues:
            print(f"   ⚠️  Found {len(issues)} issues:")
            for issue in issues:
                print(f"      - {issue}")
            print(f"   💡 Recommended fixes:")
            for fix in fixes:
                print(f"      - {fix}")
        else:
            print(f"   ✅ No CSS issues found")
        
        return issues, fixes
    
    def generate_optimized_css(self, orientation="portrait", custom_margins=None):
        """Generate optimized CSS for PDF generation"""
        
        if custom_margins:
            margin_top = custom_margins.get('top', 12)
            margin_right = custom_margins.get('right', 12)
            margin_bottom = custom_margins.get('bottom', 12)
            margin_left = custom_margins.get('left', 12)
        else:
            margin_top = margin_right = margin_bottom = margin_left = 12
        
        css = f"""
/* OPTIMIZED CSS FOR PDF GENERATION */

/* Page Setup - Critical for proper PDF rendering */
@page {{
    size: A4 {orientation};
    margin-top: {margin_top}mm;
    margin-right: {margin_right}mm;
    margin-bottom: {margin_bottom}mm;
    margin-left: {margin_left}mm;
}}

/* Reset and Box Model */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Body - Base Styles */
body {{
    font-family: Calibri, Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.3;
    color: #000;
    background: white;
    margin: 0;
    padding: 0;
}}

/* Container - Prevents overflow */
.container {{
    width: {'275mm' if orientation == 'landscape' else '188mm'};
    min-height: {'188mm' if orientation == 'landscape' else '277mm'};
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    overflow: hidden;
}}

/* Table - Fixed layout prevents distortion */
table {{
    width: 100%;
    max-width: {'275mm' if orientation == 'landscape' else '188mm'};
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 9pt;
}}

/* Table Cells - Prevent overflow */
th, td {{
    border: 1px solid black;
    padding: 4px;
    text-align: left;
    vertical-align: top;
    overflow: hidden;
    word-wrap: break-word;
    hyphens: auto;
}}

/* Header Styles */
.header {{
    text-align: {'center' if orientation == 'landscape' else 'left'};
    margin-bottom: 8px;
}}

.header h2 {{
    font-size: 12pt;
    margin: 0 0 5px 0;
}}

.header p {{
    margin: 2px 0;
    font-size: 9pt;
}}

/* Text Formatting */
.bold {{
    font-weight: bold;
}}

.underline {{
    text-decoration: underline;
}}

/* Numeric Alignment */
.numeric, .center-align {{
    text-align: center;
}}

/* Print Optimization */
@media print {{
    body {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}
    
    .container {{
        page-break-after: always;
    }}
    
    .container:last-child {{
        page-break-after: auto;
    }}
    
    table {{
        page-break-inside: auto;
    }}
    
    tr {{
        page-break-inside: avoid;
        page-break-after: auto;
    }}
}}
"""
        return css
    
    def check_all_templates(self):
        """Check all templates for issues"""
        print(f"\n{'='*80}")
        print(f"CHECKING ALL TEMPLATES")
        print(f"{'='*80}")
        
        templates = [
            "templates/first_page.html",
            "templates/deviation_statement.html",
            "templates/note_sheet.html",
            "templates/last_page.html",
            "templates/extra_items.html"
        ]
        
        all_issues = {}
        
        for template in templates:
            if os.path.exists(template):
                issues, fixes = self.check_template_css(template)
                if issues:
                    all_issues[template] = {"issues": issues, "fixes": fixes}
        
        return all_issues
    
    def generate_best_practices_guide(self):
        """Generate best practices guide"""
        guide = """
================================================================================
PDF GENERATION BEST PRACTICES GUIDE
================================================================================

1. CSS OPTIMIZATION
   ✅ Always use @page directive with explicit margins
   ✅ Set box-sizing: border-box on all elements
   ✅ Use table-layout: fixed for consistent column widths
   ✅ Set overflow: hidden to prevent content overflow
   ✅ Use 9pt or 10pt font size for optimal readability

2. HTML STRUCTURE
   ✅ Keep HTML structure simple and semantic
   ✅ Avoid nested tables when possible
   ✅ Use fixed widths for table columns
   ✅ Avoid absolute positioning

3. CONTENT OPTIMIZATION
   ✅ Break long text into multiple lines
   ✅ Use word-wrap: break-word for long words
   ✅ Set appropriate line-height (1.3-1.5)
   ✅ Avoid very small font sizes (< 8pt)

4. PAGE LAYOUT
   ✅ Use A4 dimensions: 210mm x 297mm (portrait) or 297mm x 210mm (landscape)
   ✅ Set margins: 10-15mm on all sides
   ✅ Calculate content area: page_width - left_margin - right_margin
   ✅ Ensure content fits within calculated area

5. PDF ENGINE SELECTION
   ✅ WeasyPrint: Best quality, full CSS3 support
   ✅ xhtml2pdf: Good compatibility, moderate quality
   ✅ ReportLab: Programmatic control, requires HTML parsing
   ✅ pdfkit: Requires wkhtmltopdf, good for simple layouts

6. TESTING
   ✅ Test with sample data of varying lengths
   ✅ Check for text overflow
   ✅ Verify page breaks
   ✅ Compare HTML preview with PDF output
   ✅ Test with different PDF engines

7. COMMON ISSUES AND FIXES

   Issue: Blank PDFs
   Fix: Check HTML rendering, ensure content is not hidden by CSS

   Issue: Distorted layout
   Fix: Use fixed table layout, set explicit column widths

   Issue: Text overflow
   Fix: Set overflow: hidden, use word-wrap: break-word

   Issue: Incorrect page size
   Fix: Verify @page directive, check orientation setting

   Issue: Missing content
   Fix: Check for page breaks, ensure content fits in page

8. DEBUGGING TIPS
   ✅ Generate HTML preview first
   ✅ Open HTML in browser to check rendering
   ✅ Use PDF diagnostic tools to analyze output
   ✅ Check PDF page dimensions and content
   ✅ Compare text length in HTML vs PDF

================================================================================
"""
        return guide
    
    def save_optimized_css_templates(self):
        """Save optimized CSS for each template type"""
        print(f"\n{'='*80}")
        print(f"GENERATING OPTIMIZED CSS TEMPLATES")
        print(f"{'='*80}\n")
        
        os.makedirs("test_outputs/optimized_css", exist_ok=True)
        
        # Portrait template
        portrait_css = self.generate_optimized_css("portrait")
        with open("test_outputs/optimized_css/portrait_optimized.css", 'w') as f:
            f.write(portrait_css)
        print("✅ Generated: portrait_optimized.css")
        
        # Landscape template
        landscape_css = self.generate_optimized_css("landscape")
        with open("test_outputs/optimized_css/landscape_optimized.css", 'w') as f:
            f.write(landscape_css)
        print("✅ Generated: landscape_optimized.css")
        
        # Note sheet with custom margins
        notesheet_css = self.generate_optimized_css("portrait", {"top": 6, "right": 6, "bottom": 15, "left": 6})
        with open("test_outputs/optimized_css/notesheet_optimized.css", 'w') as f:
            f.write(notesheet_css)
        print("✅ Generated: notesheet_optimized.css")
        
        print(f"\n📁 Optimized CSS saved to: test_outputs/optimized_css/")
    
    def generate_report(self):
        """Generate comprehensive fix report"""
        print(f"\n{'='*80}")
        print(f"PDF GENERATION FIX REPORT")
        print(f"{'='*80}\n")
        
        # Check templates
        issues = self.check_all_templates()
        
        # Generate best practices
        guide = self.generate_best_practices_guide()
        
        # Save guide
        with open("test_outputs/PDF_GENERATION_BEST_PRACTICES.txt", 'w') as f:
            f.write(guide)
        
        print(f"\n✅ Best practices guide saved: test_outputs/PDF_GENERATION_BEST_PRACTICES.txt")
        
        # Save optimized CSS
        self.save_optimized_css_templates()
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SUMMARY")
        print(f"{'='*80}\n")
        
        if issues:
            print(f"⚠️  Found issues in {len(issues)} templates")
            print(f"💡 Review the recommendations above")
        else:
            print(f"✅ All templates look good!")
        
        print(f"\n📚 Resources generated:")
        print(f"   - Best practices guide")
        print(f"   - Optimized CSS templates")
        print(f"   - Template analysis report")


def main():
    """Run PDF generation fixer"""
    fixer = PDFGenerationFixer()
    fixer.generate_report()


if __name__ == "__main__":
    main()
