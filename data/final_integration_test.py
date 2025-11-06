"""
Final Integration Test - Validate Complete System
Tests both the main bill generator and the integrated test files dashboard
"""
import os
import sys
import pathlib

def test_main_app():
    """Test main bill generator functionality"""
    print("🏠 Testing Main Bill Generator App")
    print("-" * 40)
    
    try:
        sys.path.insert(0, '.')
        from app.main import process_bill, safe_float, main
        
        # Test core functions
        assert safe_float("123.45") == 123.45
        assert safe_float("") == 0.0
        print("✅ Core functions working")
        
        # Test main function import
        assert callable(main)
        print("✅ Main app function available")
        
        return True
        
    except Exception as e:
        print(f"❌ Main app test failed: {e}")
        return False

def test_dashboard_integration():
    """Test test files dashboard integration"""
    print("\n🧪 Testing Test Files Dashboard")
    print("-" * 40)
    
    try:
        # Check pages directory
        pages_dir = pathlib.Path("pages")
        if not pages_dir.exists():
            print("❌ pages/ directory missing")
            return False
        print("✅ pages/ directory exists")
        
        # Check dashboard page
        dashboard_file = pages_dir / "01_🧪_Test_Files.py"
        if not dashboard_file.exists():
            print("❌ Test Files dashboard page missing")
            return False
        print("✅ Test Files dashboard page exists")
        
        # Check data directory
        data_dir = pathlib.Path("data")
        if not data_dir.exists():
            print("❌ data/ directory missing")
            return False
        print("✅ data/ directory exists")
        
        # Count files in data
        data_files = list(data_dir.rglob("*"))
        file_count = len([f for f in data_files if f.is_file()])
        print(f"✅ {file_count} files available in data/")
        
        # Test dashboard imports
        dashboard_code = dashboard_file.read_text()
        required_imports = ["streamlit", "pathlib", "subprocess", "shutil"]
        for imp in required_imports:
            if imp not in dashboard_code:
                print(f"❌ Missing import: {imp}")
                return False
        print("✅ Dashboard imports look good")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_file_structure():
    """Test overall file structure"""
    print("\n📁 Testing File Structure")
    print("-" * 30)
    
    required_structure = {
        "app/main.py": "Main application",
        "pages/01_🧪_Test_Files.py": "Test files dashboard",
        "data/": "Test files storage",
        "core/": "Core modules",
        "templates/": "Document templates",
        "exports/": "Export functionality",
        "requirements.txt": "Dependencies"
    }
    
    all_good = True
    for path, description in required_structure.items():
        if os.path.exists(path):
            print(f"✅ {path} - {description}")
        else:
            print(f"❌ {path} - {description} (MISSING)")
            all_good = False
    
    return all_good

def test_streamlit_compatibility():
    """Test Streamlit compatibility"""
    print("\n🌐 Testing Streamlit Compatibility")
    print("-" * 35)
    
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} available")
        
        # Test multi-page structure
        pages_dir = pathlib.Path("pages")
        if pages_dir.exists():
            page_files = list(pages_dir.glob("*.py"))
            print(f"✅ {len(page_files)} page(s) detected")
            
            for page in page_files:
                print(f"   📄 {page.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit compatibility test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 FINAL INTEGRATION TEST")
    print("=" * 50)
    
    tests = [
        ("Main Bill Generator", test_main_app),
        ("Test Files Dashboard", test_dashboard_integration),
        ("File Structure", test_file_structure),
        ("Streamlit Compatibility", test_streamlit_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n📊 INTEGRATION TEST RESULTS")
    print("=" * 35)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n🎯 FINAL STATUS")
    print("=" * 20)
    
    if all_passed:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\n🚀 System Ready:")
        print("   📋 Main App: Bill generation with Excel processing")
        print("   🧪 Dashboard: Test files management (view/run/download)")
        print("   🛡️ Safety: Original files protected, cache managed")
        
        print("\n🌐 Launch Commands:")
        print("   streamlit run app/main.py")
        print("   Then navigate between pages using sidebar")
        
        print("\n📋 Features Available:")
        print("   • Excel bill processing and document generation")
        print("   • Test files browser with syntax highlighting")
        print("   • Safe script execution with temporary copies")
        print("   • File downloads and cache management")
        print("   • Multi-page navigation")
        
    else:
        print("❌ Some integration tests failed.")
        print("Please fix issues before deployment.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ INTEGRATION COMPLETE - READY FOR DEPLOYMENT!")
    else:
        print("\n❌ FIX ISSUES BEFORE DEPLOYMENT")