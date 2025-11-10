"""
Master Update Script - Apply PDF fixes to all Stream Bill apps
Updates templates, CSS, and adds diagnostic tools to all apps
"""

import os
import shutil
from pathlib import Path

# List of all Stream Bill apps
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

# Current (master) app with all fixes
MASTER_APP = r"C:\Users\Rajkumar\Stream-Bill-App_Main"

# Files to copy
FILES_TO_COPY = {
    "templates": [
        "first_page.html",
        "deviation_statement.html",
        "extra_items.html",
        "note_sheet.html",
        "last_page.html"
    ],
    "scripts": [
        "diagnose_pdf_issues.py",
        "compare_html_pdf.py",
        "test_pdf_generation_comprehensive.py"
    ],
    "docs": [
        "PDF_MASTER_GUIDE.md"
    ],
    "core": [
        "pdf_generator_optimized.py"
    ]
}


def update_single_app(app_path, app_name):
    """Update a single app with all fixes"""
    print(f"\n{'='*80}")
    print(f"UPDATING: {app_name}")
    print(f"Path: {app_path}")
    print(f"{'='*80}\n")
    
    if not os.path.exists(app_path):
        print(f"❌ App not found: {app_path}")
        return False
    
    results = {
        "app": app_name,
        "path": app_path,
        "templates_updated": 0,
        "scripts_added": 0,
        "docs_added": 0,
        "core_updated": 0,
        "errors": []
    }
    
    # Update templates
    print("📄 Updating templates...")
    templates_dir = os.path.join(app_path, "templates")
    if os.path.exists(templates_dir):
        for template in FILES_TO_COPY["templates"]:
            src = os.path.join(MASTER_APP, "templates", template)
            dst = os.path.join(templates_dir, template)
            
            if os.path.exists(src):
                try:
                    # Backup original
                    if os.path.exists(dst):
                        backup = dst + ".backup"
                        shutil.copy2(dst, backup)
                        print(f"  📦 Backed up: {template}")
                    
                    # Copy new version
                    shutil.copy2(src, dst)
                    results["templates_updated"] += 1
                    print(f"  ✅ Updated: {template}")
                except Exception as e:
                    results["errors"].append(f"Template {template}: {str(e)}")
                    print(f"  ❌ Error: {template} - {str(e)}")
            else:
                print(f"  ⚠️  Source not found: {template}")
    else:
        print(f"  ⚠️  Templates directory not found")
        results["errors"].append("Templates directory not found")
    
    # Add/update scripts
    print("\n🔧 Adding diagnostic scripts...")
    scripts_dir = os.path.join(app_path, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    for script in FILES_TO_COPY["scripts"]:
        src = os.path.join(MASTER_APP, "scripts", script)
        dst = os.path.join(scripts_dir, script)
        
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                results["scripts_added"] += 1
                print(f"  ✅ Added: {script}")
            except Exception as e:
                results["errors"].append(f"Script {script}: {str(e)}")
                print(f"  ❌ Error: {script} - {str(e)}")
        else:
            print(f"  ⚠️  Source not found: {script}")
    
    # Add documentation
    print("\n📚 Adding documentation...")
    for doc in FILES_TO_COPY["docs"]:
        src = os.path.join(MASTER_APP, doc)
        dst = os.path.join(app_path, doc)
        
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                results["docs_added"] += 1
                print(f"  ✅ Added: {doc}")
            except Exception as e:
                results["errors"].append(f"Doc {doc}: {str(e)}")
                print(f"  ❌ Error: {doc} - {str(e)}")
    
    # Update core PDF generator
    print("\n⚙️  Updating core PDF generator...")
    core_dir = os.path.join(app_path, "core")
    if os.path.exists(core_dir):
        for core_file in FILES_TO_COPY["core"]:
            src = os.path.join(MASTER_APP, "core", core_file)
            dst = os.path.join(core_dir, core_file)
            
            if os.path.exists(src):
                try:
                    # Backup original
                    if os.path.exists(dst):
                        backup = dst + ".backup"
                        shutil.copy2(dst, backup)
                        print(f"  📦 Backed up: {core_file}")
                    
                    # Copy new version
                    shutil.copy2(src, dst)
                    results["core_updated"] += 1
                    print(f"  ✅ Updated: {core_file}")
                except Exception as e:
                    results["errors"].append(f"Core {core_file}: {str(e)}")
                    print(f"  ❌ Error: {core_file} - {str(e)}")
    else:
        print(f"  ⚠️  Core directory not found")
    
    # Summary
    print(f"\n{'─'*80}")
    print(f"SUMMARY FOR {app_name}:")
    print(f"  ✅ Templates updated: {results['templates_updated']}")
    print(f"  ✅ Scripts added: {results['scripts_added']}")
    print(f"  ✅ Docs added: {results['docs_added']}")
    print(f"  ✅ Core updated: {results['core_updated']}")
    if results["errors"]:
        print(f"  ❌ Errors: {len(results['errors'])}")
        for error in results["errors"]:
            print(f"     - {error}")
    print(f"{'─'*80}")
    
    return results


def main():
    """Update all apps"""
    print(f"\n{'#'*80}")
    print(f"# MASTER UPDATE SCRIPT - UPDATING ALL STREAM BILL APPS")
    print(f"# Source: {MASTER_APP}")
    print(f"# Apps to update: {len(APPS)}")
    print(f"{'#'*80}\n")
    
    all_results = []
    
    for app_path in APPS:
        app_name = os.path.basename(app_path)
        
        # Skip master app
        if app_path == MASTER_APP:
            print(f"\n⏭️  Skipping master app: {app_name}")
            continue
        
        result = update_single_app(app_path, app_name)
        if result:
            all_results.append(result)
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"FINAL SUMMARY - ALL APPS")
    print(f"{'='*80}\n")
    
    total_templates = sum(r["templates_updated"] for r in all_results)
    total_scripts = sum(r["scripts_added"] for r in all_results)
    total_docs = sum(r["docs_added"] for r in all_results)
    total_core = sum(r["core_updated"] for r in all_results)
    total_errors = sum(len(r["errors"]) for r in all_results)
    
    print(f"Apps Updated: {len(all_results)}")
    print(f"✅ Total Templates Updated: {total_templates}")
    print(f"✅ Total Scripts Added: {total_scripts}")
    print(f"✅ Total Docs Added: {total_docs}")
    print(f"✅ Total Core Files Updated: {total_core}")
    print(f"❌ Total Errors: {total_errors}")
    
    print(f"\n{'─'*80}")
    print(f"BY APP:")
    print(f"{'─'*80}\n")
    
    for result in all_results:
        status = "✅ SUCCESS" if len(result["errors"]) == 0 else "⚠️  WITH ERRORS"
        print(f"{status} - {result['app']}")
        print(f"  Templates: {result['templates_updated']}, Scripts: {result['scripts_added']}, "
              f"Docs: {result['docs_added']}, Core: {result['core_updated']}")
        if result["errors"]:
            print(f"  Errors: {len(result['errors'])}")
    
    print(f"\n{'='*80}")
    print(f"✅ ALL APPS UPDATED!")
    print(f"{'='*80}\n")
    
    print("📋 Next steps for each app:")
    print("  1. cd to app directory")
    print("  2. Run: python scripts/test_pdf_generation_comprehensive.py")
    print("  3. Verify: Check test_outputs/comprehensive_*/comprehensive_test_report.json")
    print("  4. Review: PDF_MASTER_GUIDE.md for details")


if __name__ == "__main__":
    main()
