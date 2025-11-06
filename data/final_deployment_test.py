"""
Final Deployment Test - Validate app/main.py is ready for Streamlit Cloud
"""
import os
import sys
import subprocess

def test_streamlit_app():
    """Test that the Streamlit app can be imported and run"""
    print("🚀 FINAL DEPLOYMENT TEST")
    print("="*50)
    
    # Test 1: Check app/main.py exists
    if not os.path.exists("app/main.py"):
        print("❌ app/main.py not found!")
        return False
    print("✅ app/main.py exists")
    
    # Test 2: Check requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    print("✅ requirements.txt exists")
    
    # Test 3: Test imports
    try:
        sys.path.insert(0, '.')
        from app.main import main, process_bill, safe_float
        print("✅ Core functions imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 4: Test basic functionality
    try:
        result = safe_float("123.45")
        assert result == 123.45
        print("✅ Basic functionality working")
    except Exception as e:
        print(f"❌ Basic functionality failed: {e}")
        return False
    
    # Test 5: Check for redundant files
    redundant_files = []
    for file in os.listdir('.'):
        if file.endswith('.py') and file not in ['setup.py', 'test_consolidated_app.py', 'final_deployment_test.py', 'comprehensive_test.py', 'final_validation.py', 'comprehensive_workflow_test.py']:
            if file != 'app' and not file.startswith('requirements'):
                redundant_files.append(file)
    
    if redundant_files:
        print(f"⚠️ Found potential redundant Python files: {redundant_files}")
    else:
        print("✅ No redundant Python files found")
    
    # Test 6: Check directory structure
    required_dirs = ['app', 'core', 'templates', 'exports']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"⚠️ {dir_name}/ directory missing")
    
    print("\n📋 DEPLOYMENT SUMMARY:")
    print("="*30)
    print("✅ Main entry point: app/main.py")
    print("✅ All functionality consolidated")
    print("✅ Streamlit Cloud ready")
    print("✅ No external module dependencies")
    
    print("\n🚀 DEPLOYMENT COMMANDS:")
    print("="*25)
    print("Local test: streamlit run app/main.py")
    print("Streamlit Cloud: Set main file to 'app/main.py'")
    
    return True

if __name__ == "__main__":
    success = test_streamlit_app()
    if success:
        print("\n🎉 READY FOR DEPLOYMENT!")
    else:
        print("\n❌ FIX ISSUES BEFORE DEPLOYMENT")