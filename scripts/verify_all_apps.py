"""
Verify All Apps - Check that updates were applied correctly
"""

import os
import json
from datetime import datetime

APPS = [
    r"C:\Users\Rajkumar\Stream-Bill-FIRST-ONE",
    r"C:\Users\Rajkumar\Stream-Bill-Generator-SAPNA",
    r"C:\Users\Rajkumar\Stream-Bill-INIT-PY",
    r"C:\Users\Rajkumar\Stream-Bill-generator-main",
    r"C:\Users\Rajkumar\Stream-Bill-generator-main2",
    r"C:\Users\Rajkumar\Streamlit_Bill_Historical",
    r"C:\Users\Rajkumar\Streamlit_Bill_New"
]

REQUIRED_FILES = {
    "templates": [
        "first_page.html",
        "deviation_statement.html",
        "extra_items.html"
    ],
    "scripts": [
        "diagnose_pdf_issues.py",
        "compare_html_pdf.py",
        "test_pdf_generation_comprehensive.py"
    ],
    "docs": [
        "PDF_MASTER_GUIDE.md"
    ]
}


def verify_app(app_path):
    """Verify a single app"""
    app_name = os.path.basename(app_path)
    
    result = {
        "app": app_name,
        "path": app_path,
        "exists": os.path.exists(app_path),
        "templates_found": 0,
        "templates_missing": [],
        "scripts_found": 0,
        "scripts_missing": [],
        "docs_found": 0,
        "docs_missing": [],
        "status": "unknown"
    }
    
    if not result["exists"]:
        result["status"] = "not_found"
        return result
    
    # Check templates
    for template in REQUIRED_FILES["templates"]:
        path = os.path.join(app_path, "templates", template)
        if os.path.exists(path):
            result["templates_found"] += 1
        else:
            result["templates_missing"].append(template)
    
    # Check scripts
    for script in REQUIRED_FILES["scripts"]:
        path = os.path.join(app_path, "scripts", script)
        if os.path.exists(path):
            result["scripts_found"] += 1
        else:
            result["scripts_missing"].append(script)
    
    # Check docs
    for doc in REQUIRED_FILES["docs"]:
        path = os.path.join(app_path, doc)
        if os.path.exists(path):
            result["docs_found"] += 1
        else:
            result["docs_missing"].append(doc)
    
    # Determine status
    if (result["templates_found"] == len(REQUIRED_FILES["templates"]) and
        result["scripts_found"] == len(REQUIRED_FILES["scripts"]) and
        result["docs_found"] == len(REQUIRED_FILES["docs"])):
        result["status"] = "complete"
    elif (result["templates_found"] > 0 or result["scripts_found"] > 0 or result["docs_found"] > 0):
        result["status"] = "partial"
    else:
        result["status"] = "not_updated"
    
    return result


def main():
    """Verify all apps"""
    print(f"\n{'='*80}")
    print(f"VERIFICATION REPORT - ALL STREAM BILL APPS")
    print(f"{'='*80}\n")
    
    results = []
    
    for app_path in APPS:
        result = verify_app(app_path)
        results.append(result)
        
        # Print status
        if result["status"] == "complete":
            status_icon = "✅"
        elif result["status"] == "partial":
            status_icon = "⚠️ "
        else:
            status_icon = "❌"
        
        print(f"{status_icon} {result['app']}")
        print(f"   Templates: {result['templates_found']}/{len(REQUIRED_FILES['templates'])}")
        print(f"   Scripts: {result['scripts_found']}/{len(REQUIRED_FILES['scripts'])}")
        print(f"   Docs: {result['docs_found']}/{len(REQUIRED_FILES['docs'])}")
        
        if result["templates_missing"]:
            print(f"   Missing templates: {', '.join(result['templates_missing'])}")
        if result["scripts_missing"]:
            print(f"   Missing scripts: {', '.join(result['scripts_missing'])}")
        if result["docs_missing"]:
            print(f"   Missing docs: {', '.join(result['docs_missing'])}")
        print()
    
    # Summary
    complete = sum(1 for r in results if r["status"] == "complete")
    partial = sum(1 for r in results if r["status"] == "partial")
    not_updated = sum(1 for r in results if r["status"] == "not_updated")
    
    print(f"{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}\n")
    print(f"✅ Complete: {complete}/{len(APPS)}")
    print(f"⚠️  Partial: {partial}/{len(APPS)}")
    print(f"❌ Not Updated: {not_updated}/{len(APPS)}")
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_apps": len(APPS),
        "complete": complete,
        "partial": partial,
        "not_updated": not_updated,
        "details": results
    }
    
    report_path = "test_outputs/verification_report.json"
    os.makedirs("test_outputs", exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved: {report_path}")


if __name__ == "__main__":
    main()
