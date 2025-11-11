"""
Interactive Bill Generation - Asks user for previous bill information
"""
import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.computations.bill_processor import process_bill
from exports.renderers import generate_html

def get_user_input():
    """Get bill information from user"""
    print("\n" + "="*80)
    print("BILL GENERATION - INTERACTIVE MODE")
    print("="*80)
    
    # Ask if this is first bill or running bill
    print("\n📋 BILL TYPE:")
    print("   1. First Bill (No previous payment)")
    print("   2. Running Bill (Has previous payment)")
    
    while True:
        bill_type = input("\nSelect bill type (1 or 2): ").strip()
        if bill_type in ['1', '2']:
            break
        print("❌ Invalid input. Please enter 1 or 2.")
    
    is_first_bill = (bill_type == '1')
    previous_bill_amount = 0
    
    if not is_first_bill:
        print("\n💰 PREVIOUS BILL INFORMATION:")
        print("   Enter the total amount paid in the previous bill")
        
        while True:
            try:
                amount_input = input("\nPrevious bill amount (in Rupees): ").strip().replace(',', '')
                previous_bill_amount = float(amount_input)
                if previous_bill_amount >= 0:
                    break
                print("❌ Amount cannot be negative. Please try again.")
            except ValueError:
                print("❌ Invalid amount. Please enter a number (e.g., 200000 or 2,00,000)")
    
    # Ask for premium details
    print("\n📊 PREMIUM INFORMATION:")
    
    while True:
        try:
            premium_input = input("Enter premium percentage (e.g., 5 for 5%): ").strip()
            premium_percent = float(premium_input)
            if 0 <= premium_percent <= 100:
                break
            print("❌ Premium must be between 0 and 100. Please try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    print("\n   Premium type:")
    print("   1. Above (Add to amount)")
    print("   2. Below (Deduct from amount)")
    
    while True:
        premium_type_input = input("\nSelect premium type (1 or 2): ").strip()
        if premium_type_input in ['1', '2']:
            premium_type = 'above' if premium_type_input == '1' else 'below'
            break
        print("❌ Invalid input. Please enter 1 or 2.")
    
    return {
        'is_first_bill': is_first_bill,
        'previous_bill_amount': previous_bill_amount,
        'premium_percent': premium_percent,
        'premium_type': premium_type
    }

def main():
    """Main function to run interactive bill generation"""
    
    # Check if test Excel file exists
    excel_path = "test_outputs/test_with_extra_items.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"\n❌ Error: Test Excel file not found at {excel_path}")
        print("   Please run 'python run_test_with_extra_items.py' first to create the test file.")
        return
    
    # Get user input
    user_input = get_user_input()
    
    # Display summary
    print("\n" + "="*80)
    print("BILL GENERATION SUMMARY")
    print("="*80)
    print(f"Bill Type: {'First Bill' if user_input['is_first_bill'] else 'Running Bill'}")
    if not user_input['is_first_bill']:
        print(f"Previous Bill Amount: ₹{user_input['previous_bill_amount']:,.2f}")
    print(f"Premium: {user_input['premium_percent']}% {user_input['premium_type']}")
    print("="*80)
    
    # Confirm
    confirm = input("\nProceed with bill generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Bill generation cancelled.")
        return
    
    # Load Excel file
    print("\n📂 Loading Excel file...")
    xl_file = pd.ExcelFile(excel_path)
    ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
    ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
    ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
    print("✅ Excel file loaded successfully")
    
    # Process bill
    print("\n⚙️  Processing bill...")
    first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
        ws_wo, ws_bq, ws_extra, 
        user_input['premium_percent'], 
        user_input['premium_type'],
        user_input['previous_bill_amount']
    )
    print("✅ Bill processing completed")
    
    # Display financial summary
    print("\n" + "="*80)
    print("💰 FINANCIAL SUMMARY")
    print("="*80)
    print(f"Grand Total: ₹{first_page_data['totals']['grand_total']:,.2f}")
    print(f"Premium ({user_input['premium_percent']}% {user_input['premium_type']}): ₹{first_page_data['totals']['premium']['amount']:,.2f}")
    print(f"Payable Amount: ₹{first_page_data['totals']['payable']:,.2f}")
    
    if not user_input['is_first_bill']:
        print(f"Less Previous Bill: ₹{first_page_data['totals']['last_bill_amount']:,.2f}")
        print(f"Net Payable Amount: ₹{first_page_data['totals']['net_payable']:,.2f}")
    
    print("="*80)
    
    # Generate HTML outputs
    print("\n📄 Generating HTML outputs...")
    template_dir = "templates"
    output_dir = "test_outputs"
    
    html_files = []
    
    # 1. First Page
    print("  1. Generating first_page.html...")
    html_path = generate_html("first_page", first_page_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # 2. Deviation Statement
    print("  2. Generating deviation_statement.html...")
    html_path = generate_html("deviation_statement", deviation_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # 3. Extra Items
    print("  3. Generating extra_items.html...")
    html_path = generate_html("extra_items", extra_items_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # 4. Note Sheet
    print("  4. Generating note_sheet.html...")
    html_path = generate_html("note_sheet", note_sheet_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # 5. Certificate II
    print("  5. Generating certificate_ii.html...")
    cert_ii_data = {
        'measurement_officer': 'Junior Engineer',
        'measurement_date': '01/03/2025',
        'measurement_book_page': '04-20',
        'measurement_book_no': '887',
        'officer_name': 'Name of Officer',
        'officer_designation': 'Assistant Engineer',
        'bill_date': '__/__/____',
        'authorising_officer_name': 'Name of Authorising Officer',
        'authorising_officer_designation': 'Executive Engineer',
        'authorisation_date': '__/__/____'
    }
    html_path = generate_html("certificate_ii", cert_ii_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # 6. Certificate III
    print("  6. Generating certificate_iii.html...")
    cert_iii_data = first_page_data.copy()
    cert_iii_data['payable_words'] = last_page_data.get('amount_words', 'Zero')
    html_path = generate_html("certificate_iii", cert_iii_data, template_dir, output_dir)
    html_files.append(html_path)
    print(f"     ✅ {html_path}")
    
    # Success message
    print("\n" + "="*80)
    print("✅ ALL HTML FILES GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"\n📁 Output Location: {os.path.abspath(output_dir)}")
    print(f"\n📄 Generated HTML Files:")
    for i, html_file in enumerate(html_files, 1):
        if os.path.exists(html_file):
            print(f"   {i}. {os.path.basename(html_file)}")
    
    print("\n🌐 Open first_page.html in your browser to view the bill!")
    
    # Ask if user wants to open the file
    open_file = input("\nOpen first_page.html now? (y/n): ").strip().lower()
    if open_file == 'y':
        import subprocess
        subprocess.run(['start', html_files[0]], shell=True)
        print("✅ Opening file in browser...")
    
    print("\n" + "="*80)
    print("Thank you for using the Bill Generation System!")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Bill generation cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
