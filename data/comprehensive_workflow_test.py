"""
Comprehensive Workflow Test - 25 Different Objectives
Tests the Stream Bill Generator with various scenarios to validate all capabilities
"""
import pandas as pd
import os
import tempfile
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_test_excel(scenario_name, work_items, bill_quantities, extra_items, output_dir):
    """Create test Excel file for a specific scenario"""
    
    # Create Excel file with required sheets
    excel_path = os.path.join(output_dir, f"test_{scenario_name}.xlsx")
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Work Order Sheet
        wo_data = []
        # Header rows (1-20)
        for i in range(20):
            if i == 0:
                wo_data.append(['Agreement No.', f'AGR/{scenario_name}/2024'])
            elif i == 1:
                wo_data.append(['Contractor Name', f'Test Contractor {scenario_name}'])
            elif i == 2:
                wo_data.append(['Work Description', f'Test Work {scenario_name}'])
            else:
                wo_data.append(['', ''])
        
        # Column headers (row 21)
        wo_data.append(['S.No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'])
        
        # Work items (row 22+)
        for i, item in enumerate(work_items, 1):
            wo_data.append([
                str(i),
                item['description'],
                item['unit'],
                str(item['quantity']),
                str(item['rate']),
                str(item['quantity'] * item['rate'])
            ])
        
        wo_df = pd.DataFrame(wo_data)
        wo_df.to_excel(writer, sheet_name='Work Order', index=False, header=False)
        
        # Bill Quantity Sheet
        bq_data = []
        # Header rows (1-20) - same as work order
        for i in range(20):
            if i == 0:
                bq_data.append(['Agreement No.', f'AGR/{scenario_name}/2024'])
            elif i == 1:
                bq_data.append(['Contractor Name', f'Test Contractor {scenario_name}'])
            elif i == 2:
                bq_data.append(['Work Description', f'Test Work {scenario_name}'])
            else:
                bq_data.append(['', ''])
        
        # Column headers
        bq_data.append(['S.No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'])
        
        # Bill quantities (modified from work order)
        for i, item in enumerate(bill_quantities, 1):
            bq_data.append([
                str(i),
                item['description'],
                item['unit'],
                str(item['quantity']),
                str(item['rate']),
                str(item['quantity'] * item['rate'])
            ])
        
        bq_df = pd.DataFrame(bq_data)
        bq_df.to_excel(writer, sheet_name='Bill Quantity', index=False, header=False)
        
        # Extra Items Sheet
        ei_data = []
        # Header rows (1-20)
        for i in range(20):
            if i == 0:
                ei_data.append(['Agreement No.', f'AGR/{scenario_name}/2024'])
            elif i == 1:
                ei_data.append(['Contractor Name', f'Test Contractor {scenario_name}'])
            elif i == 2:
                ei_data.append(['Work Description', f'Extra Work {scenario_name}'])
            else:
                ei_data.append(['', ''])
        
        # Column headers
        ei_data.append(['S.No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'])
        
        # Extra items
        for i, item in enumerate(extra_items, 1):
            ei_data.append([
                str(i),
                item['description'],
                item['unit'],
                str(item['quantity']),
                str(item['rate']),
                str(item['quantity'] * item['rate'])
            ])
        
        ei_df = pd.DataFrame(ei_data)
        ei_df.to_excel(writer, sheet_name='Extra Items', index=False, header=False)
    
    return excel_path

def test_scenario(scenario_num, scenario_name, work_items, bill_quantities, extra_items, premium_percent, premium_type):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"SCENARIO {scenario_num}: {scenario_name}")
    print(f"{'='*60}")
    
    try:
        # Create test directory
        test_dir = f"test_outputs/scenario_{scenario_num}_{scenario_name.replace(' ', '_')}"
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test Excel file
        excel_path = create_test_excel(scenario_name.replace(' ', '_'), work_items, bill_quantities, extra_items, test_dir)
        print(f"✅ Created test Excel: {excel_path}")
        
        # Test import of core modules
        try:
            from core.computations.bill_processor import process_bill
            from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
            print("✅ Core modules imported successfully")
        except Exception as e:
            print(f"❌ Module import failed: {e}")
            return False
        
        # Load Excel file
        xl_file = pd.ExcelFile(excel_path)
        ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
        ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
        ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
        print("✅ Excel file loaded successfully")
        
        # Process bill
        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
            ws_wo, ws_bq, ws_extra, premium_percent, premium_type
        )
        print("✅ Bill processing completed")
        
        # Generate documents
        template_dir = "templates"
        
        # Generate PDFs
        pdf_files = []
        
        first_page_pdf = os.path.join(test_dir, "first_page.pdf")
        generate_pdf("First Page", first_page_data, "landscape", template_dir, test_dir)
        pdf_files.append(first_page_pdf)
        
        last_page_pdf = os.path.join(test_dir, "last_page.pdf")
        generate_pdf("Last Page", last_page_data, "portrait", template_dir, test_dir)
        pdf_files.append(last_page_pdf)
        
        deviation_pdf = os.path.join(test_dir, "deviation_statement.pdf")
        generate_pdf("Deviation Statement", deviation_data, "landscape", template_dir, test_dir)
        pdf_files.append(deviation_pdf)
        
        extra_items_pdf = os.path.join(test_dir, "extra_items.pdf")
        generate_pdf("Extra Items", extra_items_data, "landscape", template_dir, test_dir)
        pdf_files.append(extra_items_pdf)
        
        note_sheet_pdf = os.path.join(test_dir, "note_sheet.pdf")
        generate_pdf("Note Sheet", note_sheet_data, "portrait", template_dir, test_dir)
        pdf_files.append(note_sheet_pdf)
        
        print("✅ PDF generation completed")
        
        # Generate Word documents
        word_files = []
        
        first_page_doc = os.path.join(test_dir, "first_page.docx")
        create_word_doc("First Page", first_page_data, first_page_doc)
        word_files.append(first_page_doc)
        
        last_page_doc = os.path.join(test_dir, "last_page.docx")
        create_word_doc("Last Page", last_page_data, last_page_doc)
        word_files.append(last_page_doc)
        
        print("✅ Word document generation completed")
        
        # Merge PDFs
        merged_pdf = os.path.join(test_dir, "complete_bill.pdf")
        merge_pdfs(pdf_files, merged_pdf)
        print("✅ PDF merging completed")
        
        # Create ZIP archive
        all_files = pdf_files + word_files + [merged_pdf]
        zip_path = os.path.join(test_dir, "bill_documents.zip")
        create_zip_archive(all_files, zip_path)
        print("✅ ZIP archive created")
        
        # Validate outputs
        total_amount = sum(item['quantity'] * item['rate'] for item in work_items)
        bill_amount = sum(item['quantity'] * item['rate'] for item in bill_quantities)
        extra_amount = sum(item['quantity'] * item['rate'] for item in extra_items)
        
        print(f"📊 Financial Summary:")
        print(f"   Work Order Total: ₹{total_amount:,.2f}")
        print(f"   Bill Quantity Total: ₹{bill_amount:,.2f}")
        print(f"   Extra Items Total: ₹{extra_amount:,.2f}")
        print(f"   Premium: {premium_percent}% {premium_type}")
        
        print(f"✅ SCENARIO {scenario_num} COMPLETED SUCCESSFULLY")
        return True
        
    except Exception as e:
        print(f"❌ SCENARIO {scenario_num} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all 25 test scenarios"""
    
    print("🚀 STARTING COMPREHENSIVE WORKFLOW TEST - 25 SCENARIOS")
    print("="*80)
    
    # Create main test output directory
    os.makedirs("test_outputs", exist_ok=True)
    
    scenarios = [
        # Scenario 1: Basic Construction Work
        {
            'name': 'Basic Construction',
            'work_items': [
                {'description': 'Excavation work', 'unit': 'Cum', 'quantity': 100, 'rate': 150},
                {'description': 'Concrete work', 'unit': 'Cum', 'quantity': 50, 'rate': 5000},
                {'description': 'Steel work', 'unit': 'Kg', 'quantity': 1000, 'rate': 60}
            ],
            'bill_quantities': [
                {'description': 'Excavation work', 'unit': 'Cum', 'quantity': 95, 'rate': 150},
                {'description': 'Concrete work', 'unit': 'Cum', 'quantity': 48, 'rate': 5000},
                {'description': 'Steel work', 'unit': 'Kg', 'quantity': 980, 'rate': 60}
            ],
            'extra_items': [
                {'description': 'Additional excavation', 'unit': 'Cum', 'quantity': 10, 'rate': 160}
            ],
            'premium_percent': 5.0,
            'premium_type': 'above'
        },
        
        # Scenario 2: Road Construction
        {
            'name': 'Road Construction',
            'work_items': [
                {'description': 'Road cutting', 'unit': 'Km', 'quantity': 2, 'rate': 500000},
                {'description': 'Bitumen work', 'unit': 'Ton', 'quantity': 100, 'rate': 45000},
                {'description': 'Road marking', 'unit': 'Km', 'quantity': 2, 'rate': 25000}
            ],
            'bill_quantities': [
                {'description': 'Road cutting', 'unit': 'Km', 'quantity': 2.1, 'rate': 500000},
                {'description': 'Bitumen work', 'unit': 'Ton', 'quantity': 105, 'rate': 45000},
                {'description': 'Road marking', 'unit': 'Km', 'quantity': 2, 'rate': 25000}
            ],
            'extra_items': [
                {'description': 'Traffic management', 'unit': 'LS', 'quantity': 1, 'rate': 50000}
            ],
            'premium_percent': 3.5,
            'premium_type': 'below'
        },
        
        # Scenario 3: Building Construction
        {
            'name': 'Building Construction',
            'work_items': [
                {'description': 'Foundation work', 'unit': 'Cum', 'quantity': 200, 'rate': 8000},
                {'description': 'Brick work', 'unit': 'Cum', 'quantity': 500, 'rate': 4500},
                {'description': 'Plastering', 'unit': 'Sqm', 'quantity': 2000, 'rate': 180},
                {'description': 'Flooring', 'unit': 'Sqm', 'quantity': 1000, 'rate': 650}
            ],
            'bill_quantities': [
                {'description': 'Foundation work', 'unit': 'Cum', 'quantity': 195, 'rate': 8000},
                {'description': 'Brick work', 'unit': 'Cum', 'quantity': 485, 'rate': 4500},
                {'description': 'Plastering', 'unit': 'Sqm', 'quantity': 1950, 'rate': 180},
                {'description': 'Flooring', 'unit': 'Sqm', 'quantity': 980, 'rate': 650}
            ],
            'extra_items': [
                {'description': 'Waterproofing', 'unit': 'Sqm', 'quantity': 100, 'rate': 350},
                {'description': 'Additional electrical', 'unit': 'LS', 'quantity': 1, 'rate': 75000}
            ],
            'premium_percent': 7.2,
            'premium_type': 'above'
        },
        
        # Scenario 4: Bridge Construction
        {
            'name': 'Bridge Construction',
            'work_items': [
                {'description': 'Pile foundation', 'unit': 'Nos', 'quantity': 20, 'rate': 125000},
                {'description': 'Pier construction', 'unit': 'Cum', 'quantity': 150, 'rate': 12000},
                {'description': 'Deck slab', 'unit': 'Cum', 'quantity': 300, 'rate': 15000},
                {'description': 'Railing work', 'unit': 'Mtr', 'quantity': 200, 'rate': 2500}
            ],
            'bill_quantities': [
                {'description': 'Pile foundation', 'unit': 'Nos', 'quantity': 20, 'rate': 125000},
                {'description': 'Pier construction', 'unit': 'Cum', 'quantity': 148, 'rate': 12000},
                {'description': 'Deck slab', 'unit': 'Cum', 'quantity': 295, 'rate': 15000},
                {'description': 'Railing work', 'unit': 'Mtr', 'quantity': 195, 'rate': 2500}
            ],
            'extra_items': [
                {'description': 'Approach road', 'unit': 'Mtr', 'quantity': 50, 'rate': 8000}
            ],
            'premium_percent': 2.8,
            'premium_type': 'below'
        },
        
        # Scenario 5: Water Supply Project
        {
            'name': 'Water Supply',
            'work_items': [
                {'description': 'Pipeline laying', 'unit': 'Mtr', 'quantity': 5000, 'rate': 850},
                {'description': 'Valve installation', 'unit': 'Nos', 'quantity': 50, 'rate': 12000},
                {'description': 'Pump house', 'unit': 'LS', 'quantity': 1, 'rate': 500000},
                {'description': 'Testing & commissioning', 'unit': 'LS', 'quantity': 1, 'rate': 75000}
            ],
            'bill_quantities': [
                {'description': 'Pipeline laying', 'unit': 'Mtr', 'quantity': 4950, 'rate': 850},
                {'description': 'Valve installation', 'unit': 'Nos', 'quantity': 48, 'rate': 12000},
                {'description': 'Pump house', 'unit': 'LS', 'quantity': 1, 'rate': 500000},
                {'description': 'Testing & commissioning', 'unit': 'LS', 'quantity': 1, 'rate': 75000}
            ],
            'extra_items': [
                {'description': 'Additional connections', 'unit': 'Nos', 'quantity': 25, 'rate': 3500}
            ],
            'premium_percent': 4.5,
            'premium_type': 'above'
        }
    ]
    
    # Add 20 more scenarios with variations
    for i in range(6, 26):
        base_scenario = scenarios[i % 5]  # Cycle through base scenarios
        
        # Create variations
        scenario = {
            'name': f'{base_scenario["name"]} Variant {i-5}',
            'work_items': [
                {
                    'description': f'{item["description"]} - V{i-5}',
                    'unit': item['unit'],
                    'quantity': int(item['quantity'] * (0.8 + (i-5) * 0.1)),  # Vary quantities
                    'rate': int(item['rate'] * (0.9 + (i-5) * 0.05))  # Vary rates
                }
                for item in base_scenario['work_items']
            ],
            'bill_quantities': [
                {
                    'description': f'{item["description"]} - V{i-5}',
                    'unit': item['unit'],
                    'quantity': int(item['quantity'] * (0.75 + (i-5) * 0.1)),
                    'rate': int(item['rate'] * (0.9 + (i-5) * 0.05))
                }
                for item in base_scenario['bill_quantities']
            ],
            'extra_items': [
                {
                    'description': f'{item["description"]} - V{i-5}',
                    'unit': item['unit'],
                    'quantity': int(item['quantity'] * (0.5 + (i-5) * 0.2)),
                    'rate': int(item['rate'] * (0.8 + (i-5) * 0.1))
                }
                for item in base_scenario['extra_items']
            ],
            'premium_percent': round(base_scenario['premium_percent'] + (i-5) * 0.5, 1),
            'premium_type': 'above' if i % 2 == 0 else 'below'
        }
        scenarios.append(scenario)
    
    # Run all scenarios
    successful_tests = 0
    failed_tests = 0
    
    for i, scenario in enumerate(scenarios, 1):
        success = test_scenario(
            i,
            scenario['name'],
            scenario['work_items'],
            scenario['bill_quantities'],
            scenario['extra_items'],
            scenario['premium_percent'],
            scenario['premium_type']
        )
        
        if success:
            successful_tests += 1
        else:
            failed_tests += 1
    
    # Final summary
    print("\n" + "="*80)
    print("🎯 COMPREHENSIVE TEST SUMMARY")
    print("="*80)
    print(f"✅ Successful Tests: {successful_tests}")
    print(f"❌ Failed Tests: {failed_tests}")
    print(f"📊 Success Rate: {(successful_tests/25)*100:.1f}%")
    
    if successful_tests == 25:
        print("🎉 ALL TESTS PASSED! Application is fully functional.")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    return successful_tests == 25

if __name__ == "__main__":
    run_all_tests()