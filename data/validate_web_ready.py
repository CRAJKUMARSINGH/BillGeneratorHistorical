"""
Validate that the web application is ready for deployment
"""
import sys
import os
import subprocess
import time

def test_app_functionality():
    """Test core app functionality"""
    print("🧪 Testing Core Functionality")
    print("-" * 30)
    
    try:
        sys.path.insert(0, '.')
        
        # Test imports
        from app.main import process_bill, safe_float, number_to_words
        print("✅ Core functions imported")
        
        # Test safe_float
        assert safe_float("123.45") == 123.45
        assert safe_float("") == 0.0
        assert safe_float(None) == 0.0
        print("✅ safe_float working")
        
        # Test number_to_words
        result = number_to_words(1234)
        print(f"✅ number_to_words(1234) = {result}")
        
        # Test pandas
        import pandas as pd
        test_df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        assert len(test_df) == 2
        print("✅ Pandas working")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_streamlit_import():
    """Test Streamlit import"""
    print("\n🌐 Testing Streamlit")
    print("-" * 20)
    
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} imported")
        return True
    except Exception as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def test_app_structure():
    """Test app file structure"""
    print("\n📁 Testing File Structure")
    print("-" * 25)
    
    required_files = [
        'app/main.py',
        'requirements.txt',
        '🚀_LAUNCH_APP.bat'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 WEB APPLICATION VALIDATION")
    print("=" * 40)
    
    tests = [
        ("Core Functionality", test_app_functionality),
        ("Streamlit Import", test_streamlit_import),
        ("File Structure", test_app_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n📊 TEST RESULTS")
    print("=" * 20)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n🎯 FINAL RESULT")
    print("=" * 15)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 Ready to run web application:")
        print("   Method 1: streamlit run app/main.py")
        print("   Method 2: 🚀_LAUNCH_APP.bat")
        print("   Method 3: python -m streamlit run app/main.py --server.port 8503")
        print("\n🌐 The app will be available at:")
        print("   http://localhost:8501 (default)")
        print("   http://localhost:8503 (custom port)")
        
        print("\n📋 For Streamlit Cloud deployment:")
        print("   Set main file path to: app/main.py")
        
    else:
        print("❌ Some tests failed. Please fix issues before running.")
    
    return all_passed

if __name__ == "__main__":
    main()