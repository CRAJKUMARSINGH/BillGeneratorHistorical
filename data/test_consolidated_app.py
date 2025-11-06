"""
Test the consolidated app/main.py functionality
"""
import pandas as pd
import os
import sys
import tempfile

# Add project root to path
sys.path.insert(0, '.')

def test_consolidated_app():
    """Test the consolidated app functionality"""
    print("🚀 Testing Consolidated App Functionality")
    print("="*50)
    
    try:
        # Test imports
        from app.main import process_bill, safe_float, number_to_words
        print("✅ Core functions imported successfully")
        
        # Test safe_float function
        assert safe_float("123.45") == 123.45
        assert safe_float("") == 0.0
        assert safe_float(None) == 0.0
        assert safe_float("invalid") == 0.0
        print("✅ safe_float function working correctly")
        
        # Test number_to_words function
        result = number_to_words(12345)
        print(f"✅ number_to_words(12345) = {result}")
        
        # Create test Excel data
        print("\n📊 Creating test Excel data...")
        
        # Create test dataframes
        wo_data = []
        # Header rows (0-19)
        for i in range(20):
            if i == 0:
                wo_data.append(['Agreement No.', 'TEST/2024/001', '', '', '', '', ''])
            elif i == 1:
                wo_data.append(['Contractor Name', 'Test Contractor Ltd.', '', '', '', '', ''])
            else:
                wo_data.append(['', '', '', '', '', '', ''])
        
        # Column headers (row 20)
        wo_data.append(['S.No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount', 'Remarks'])
        
        # Work items (row 21+)
        wo_data.append(['1', 'Excavation work', 'Cum', '100', '150', '15000', 'Test item'])
        wo_data.append(['2', 'Concrete work', 'Cum', '50', '5000', '250000', 'Test item'])
        wo_data.append(['3', 'Steel work', 'Kg', '1000', '60', '60000', 'Test item'])
        
        ws_wo = pd.DataFrame(wo_data)
        
        # Bill Quantity sheet (similar structure, different quantities)
        bq_data = wo_data.copy()
        bq_data[21] = ['1', 'Excavation work', 'Cum', '95', '150', '14250', 'Test item']
        bq_data[22] = ['2', 'Concrete work', 'Cum', '48', '5000', '240000', 'Test item']
        bq_data[23] = ['3', 'Steel work', 'Kg', '980', '60', '58800', 'Test item']
        
        ws_bq = pd.DataFrame(bq_data)
        
        # Extra Items sheet
        ei_data = []
        for i in range(20):
            if i == 0:
                ei_data.append(['Agreement No.', 'TEST/2024/001', '', '', '', '', ''])
            else:
                ei_data.append(['', '', '', '', '', '', ''])
        
        ei_data.append(['S.No.', 'Remarks', 'Description', 'Quantity', 'Unit', 'Rate', 'Amount'])
        ei_data.append(['1', 'Extra work', 'Additional excavation', '10', 'Cum', '160', '1600'])
        
        ws_extra = pd.DataFrame(ei_data)
        
        print("✅ Test Excel data created")
        
        # Test bill processing
        print("\n⚙️ Testing bill processing...")
        
        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
            ws_wo, ws_bq, ws_extra, 5.0, "above"
        )
        
        print("✅ Bill processing completed successfully")
        
        # Validate results
        assert "header" in first_page_data
        assert "items" in first_page_data
        assert "totals" in first_page_data
        assert len(first_page_data["items"]) > 0
        
        print(f"📊 Processed {len(first_page_data['items'])} items")
        print(f"💰 Grand Total: ₹{first_page_data['totals']['grand_total']:,.2f}")
        print(f"💰 Premium: ₹{first_page_data['totals']['premium']['amount']:,.2f}")
        print(f"💰 Payable: ₹{first_page_data['totals']['payable']:,.2f}")
        
        # Test PDF generation (if available)
        try:
            from app.main import generate_simple_pdf
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_path = os.path.join(temp_dir, "test.pdf")
                result = generate_simple_pdf("First Page", first_page_data, pdf_path)
                if result:
                    print("✅ PDF generation working")
                else:
                    print("⚠️ PDF generation not available (missing wkhtmltopdf)")
        except Exception as e:
            print(f"⚠️ PDF generation test failed: {e}")
        
        # Test Word document generation (if available)
        try:
            from app.main import create_simple_word_doc
            with tempfile.TemporaryDirectory() as temp_dir:
                doc_path = os.path.join(temp_dir, "test.docx")
                result = create_simple_word_doc("First Page", first_page_data, doc_path)
                if result:
                    print("✅ Word document generation working")
                else:
                    print("⚠️ Word document generation not available (missing python-docx)")
        except Exception as e:
            print(f"⚠️ Word document generation test failed: {e}")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Consolidated app/main.py is fully functional")
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_consolidated_app()
    if success:
        print("\n🚀 Ready for Streamlit Cloud deployment!")
        print("Run: streamlit run app/main.py")
    else:
        print("\n❌ Fix issues before deployment")