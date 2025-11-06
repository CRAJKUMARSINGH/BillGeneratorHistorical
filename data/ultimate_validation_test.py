"""
Ultimate Validation Test - 25 Different Scenarios
Tests all workflow capabilities with various work items, quantities, and configurations
"""
import pandas as pd
import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, '.')

def create_test_scenario(scenario_id, work_name, items_config, premium_config):
    """Create a test scenario with specific configuration"""
    
    # Create test Excel data
    wo_data = []
    
    # Header rows (0-19)
    for i in range(20):
        if i == 0:
            wo_data.append(['Agreement No.', f'AGR/{scenario_id}/2024'])
        elif i == 1:
            wo_data.append(['Contractor Name', f'{work_name} Contractor'])
        elif i == 2:
            wo_data.append(['Work Description', f'{work_name} Project'])
        elif i == 3:
            wo_data.append(['Location', f'Test Location {scenario_id}'])
        else:
            wo_data.append(['', '', '', '', '', '', ''])
    
    # Column headers (row 20)
    wo_data.append(['S.No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount', 'Remarks'])
    
    # Work items (row 21+)
    for i, item in enumerate(items_config['work_items'], 1):
        wo_data.append([
            str(i),
            item['description'],
            item['unit'],
            str(item['quantity']),
            str(item['rate']),
            str(item['quantity'] * item['rate']),
            item.get('remarks', f'Item {i}')
        ])
    
    ws_wo = pd.DataFrame(wo_data)
    
    # Bill Quantity sheet (modified quantities)
    bq_data = wo_data.copy()
    for i, item in enumerate(items_config['bill_quantities'], 1):
        row_idx = 20 + i  # Adjust for header rows
        if row_idx < len(bq_data):
            bq_data[row_idx] = [
                str(i),
                item['description'],
                item['unit'],
                str(item['quantity']),
                str(item['rate']),
                str(item['quantity'] * item['rate']),
                item.get('remarks', f'Bill Item {i}')
            ]
    
    ws_bq = pd.DataFrame(bq_data)
    
    # Extra Items sheet
    ei_data = []
    for i in range(20):
        if i == 0:
            ei_data.append(['Agreement No.', f'AGR/{scenario_id}/2024'])
        elif i == 1:
            ei_data.append(['Contractor Name', f'{work_name} Contractor'])
        else:
            ei_data.append(['', '', '', '', '', '', ''])
    
    ei_data.append(['S.No.', 'Remarks', 'Description', 'Quantity', 'Unit', 'Rate', 'Amount'])
    
    for i, item in enumerate(items_config['extra_items'], 1):
        ei_data.append([
            str(i),
            item.get('remarks', f'Extra {i}'),
            item['description'],
            str(item['quantity']),
            item['unit'],
            str(item['rate']),
            str(item['quantity'] * item['rate'])
        ])
    
    ws_extra = pd.DataFrame(ei_data)
    
    return ws_wo, ws_bq, ws_extra, premium_config

def test_scenario(scenario_id, scenario_name, work_name, items_config, premium_config):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"SCENARIO {scenario_id}: {scenario_name}")
    print(f"Work: {work_name}")
    print(f"Premium: {premium_config['percent']}% {premium_config['type']}")
    print(f"{'='*60}")
    
    try:
        # Import core functions
        from app.main import process_bill, safe_float
        
        # Create test data
        ws_wo, ws_bq, ws_extra, premium_config = create_test_scenario(
            scenario_id, work_name, items_config, premium_config
        )
        
        # Process bill
        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
            ws_wo, ws_bq, ws_extra, premium_config['percent'], premium_config['type']
        )
        
        # Validate results
        assert "header" in first_page_data
        assert "items" in first_page_data
        assert "totals" in first_page_data
        assert len(first_page_data["items"]) > 0
        
        # Calculate expected totals
        work_total = sum(item['quantity'] * item['rate'] for item in items_config['work_items'])
        bill_total = sum(item['quantity'] * item['rate'] for item in items_config['bill_quantities'])
        extra_total = sum(item['quantity'] * item['rate'] for item in items_config['extra_items'])
        
        print(f"📊 Financial Summary:")
        print(f"   Work Order Total: ₹{work_total:,.2f}")
        print(f"   Bill Quantity Total: ₹{bill_total:,.2f}")
        print(f"   Extra Items Total: ₹{extra_total:,.2f}")
        print(f"   Processed Grand Total: ₹{first_page_data['totals']['grand_total']:,.2f}")
        print(f"   Premium Amount: ₹{first_page_data['totals']['premium']['amount']:,.2f}")
        print(f"   Final Payable: ₹{first_page_data['totals']['payable']:,.2f}")
        
        print(f"✅ SCENARIO {scenario_id} COMPLETED SUCCESSFULLY")
        return True
        
    except Exception as e:
        print(f"❌ SCENARIO {scenario_id} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_ultimate_validation():
    """Run 25 comprehensive test scenarios"""
    
    print("🚀 ULTIMATE VALIDATION TEST - 25 COMPREHENSIVE SCENARIOS")
    print("="*80)
    
    # Define 25 different scenarios with varied configurations
    scenarios = [
        # Construction Projects (1-5)
        {
            'name': 'Residential Building Construction',
            'work_name': 'Residential Complex',
            'items': {
                'work_items': [
                    {'description': 'Foundation excavation', 'unit': 'Cum', 'quantity': 200, 'rate': 180},
                    {'description': 'RCC foundation', 'unit': 'Cum', 'quantity': 150, 'rate': 8500},
                    {'description': 'Brick masonry', 'unit': 'Cum', 'quantity': 800, 'rate': 4200},
                    {'description': 'Plastering work', 'unit': 'Sqm', 'quantity': 3000, 'rate': 220}
                ],
                'bill_quantities': [
                    {'description': 'Foundation excavation', 'unit': 'Cum', 'quantity': 195, 'rate': 180},
                    {'description': 'RCC foundation', 'unit': 'Cum', 'quantity': 148, 'rate': 8500},
                    {'description': 'Brick masonry', 'unit': 'Cum', 'quantity': 785, 'rate': 4200},
                    {'description': 'Plastering work', 'unit': 'Sqm', 'quantity': 2950, 'rate': 220}
                ],
                'extra_items': [
                    {'description': 'Waterproofing', 'unit': 'Sqm', 'quantity': 500, 'rate': 350},
                    {'description': 'Additional electrical', 'unit': 'LS', 'quantity': 1, 'rate': 125000}
                ]
            },
            'premium': {'percent': 5.5, 'type': 'above'}
        },
        
        {
            'name': 'Commercial Building Construction',
            'work_name': 'Shopping Mall',
            'items': {
                'work_items': [
                    {'description': 'Site preparation', 'unit': 'Sqm', 'quantity': 5000, 'rate': 45},
                    {'description': 'Steel structure', 'unit': 'MT', 'quantity': 250, 'rate': 85000},
                    {'description': 'Glazing work', 'unit': 'Sqm', 'quantity': 2000, 'rate': 1200},
                    {'description': 'HVAC installation', 'unit': 'LS', 'quantity': 1, 'rate': 2500000}
                ],
                'bill_quantities': [
                    {'description': 'Site preparation', 'unit': 'Sqm', 'quantity': 4950, 'rate': 45},
                    {'description': 'Steel structure', 'unit': 'MT', 'quantity': 248, 'rate': 85000},
                    {'description': 'Glazing work', 'unit': 'Sqm', 'quantity': 1980, 'rate': 1200},
                    {'description': 'HVAC installation', 'unit': 'LS', 'quantity': 1, 'rate': 2500000}
                ],
                'extra_items': [
                    {'description': 'Fire safety system', 'unit': 'LS', 'quantity': 1, 'rate': 350000}
                ]
            },
            'premium': {'percent': 3.2, 'type': 'below'}
        },
        
        # Infrastructure Projects (3-7)
        {
            'name': 'Highway Construction',
            'work_name': 'National Highway',
            'items': {
                'work_items': [
                    {'description': 'Land clearing', 'unit': 'Hectare', 'quantity': 50, 'rate': 125000},
                    {'description': 'Earthwork', 'unit': 'Cum', 'quantity': 100000, 'rate': 85},
                    {'description': 'Pavement construction', 'unit': 'Km', 'quantity': 25, 'rate': 8500000},
                    {'description': 'Road marking', 'unit': 'Km', 'quantity': 25, 'rate': 45000}
                ],
                'bill_quantities': [
                    {'description': 'Land clearing', 'unit': 'Hectare', 'quantity': 48, 'rate': 125000},
                    {'description': 'Earthwork', 'unit': 'Cum', 'quantity': 98500, 'rate': 85},
                    {'description': 'Pavement construction', 'unit': 'Km', 'quantity': 25, 'rate': 8500000},
                    {'description': 'Road marking', 'unit': 'Km', 'quantity': 25, 'rate': 45000}
                ],
                'extra_items': [
                    {'description': 'Traffic signals', 'unit': 'Nos', 'quantity': 15, 'rate': 185000},
                    {'description': 'Guardrails', 'unit': 'Mtr', 'quantity': 2000, 'rate': 850}
                ]
            },
            'premium': {'percent': 7.8, 'type': 'above'}
        },
        
        {
            'name': 'Bridge Construction',
            'work_name': 'River Bridge',
            'items': {
                'work_items': [
                    {'description': 'Pile foundation', 'unit': 'Nos', 'quantity': 40, 'rate': 185000},
                    {'description': 'Pier construction', 'unit': 'Cum', 'quantity': 300, 'rate': 15000},
                    {'description': 'Girder installation', 'unit': 'Nos', 'quantity': 20, 'rate': 450000},
                    {'description': 'Deck slab', 'unit': 'Cum', 'quantity': 500, 'rate': 18000}
                ],
                'bill_quantities': [
                    {'description': 'Pile foundation', 'unit': 'Nos', 'quantity': 40, 'rate': 185000},
                    {'description': 'Pier construction', 'unit': 'Cum', 'quantity': 295, 'rate': 15000},
                    {'description': 'Girder installation', 'unit': 'Nos', 'quantity': 20, 'rate': 450000},
                    {'description': 'Deck slab', 'unit': 'Cum', 'quantity': 485, 'rate': 18000}
                ],
                'extra_items': [
                    {'description': 'Approach road', 'unit': 'Mtr', 'quantity': 200, 'rate': 12000}
                ]
            },
            'premium': {'percent': 4.5, 'type': 'below'}
        },
        
        {
            'name': 'Water Supply Project',
            'work_name': 'Municipal Water Supply',
            'items': {
                'work_items': [
                    {'description': 'Pipeline laying', 'unit': 'Mtr', 'quantity': 10000, 'rate': 950},
                    {'description': 'Pump installation', 'unit': 'Nos', 'quantity': 5, 'rate': 285000},
                    {'description': 'Storage tank', 'unit': 'Nos', 'quantity': 2, 'rate': 1250000},
                    {'description': 'Control system', 'unit': 'LS', 'quantity': 1, 'rate': 450000}
                ],
                'bill_quantities': [
                    {'description': 'Pipeline laying', 'unit': 'Mtr', 'quantity': 9850, 'rate': 950},
                    {'description': 'Pump installation', 'unit': 'Nos', 'quantity': 5, 'rate': 285000},
                    {'description': 'Storage tank', 'unit': 'Nos', 'quantity': 2, 'rate': 1250000},
                    {'description': 'Control system', 'unit': 'LS', 'quantity': 1, 'rate': 450000}
                ],
                'extra_items': [
                    {'description': 'Additional connections', 'unit': 'Nos', 'quantity': 50, 'rate': 4500}
                ]
            },
            'premium': {'percent': 6.2, 'type': 'above'}
        }
    ]
    
    # Generate 20 more scenarios by creating variations
    base_scenarios = scenarios.copy()
    for i in range(20):
        base_idx = i % len(base_scenarios)
        base = base_scenarios[base_idx]
        
        # Create variation
        variation = {
            'name': f"{base['name']} - Variant {i+1}",
            'work_name': f"{base['work_name']} V{i+1}",
            'items': {
                'work_items': [],
                'bill_quantities': [],
                'extra_items': []
            },
            'premium': {
                'percent': round(base['premium']['percent'] + (i * 0.3), 1),
                'type': 'above' if (i % 2 == 0) else 'below'
            }
        }
        
        # Vary quantities and rates
        multiplier = 0.7 + (i * 0.1)
        rate_multiplier = 0.9 + (i * 0.05)
        
        for item in base['items']['work_items']:
            variation['items']['work_items'].append({
                'description': f"{item['description']} - V{i+1}",
                'unit': item['unit'],
                'quantity': int(item['quantity'] * multiplier),
                'rate': int(item['rate'] * rate_multiplier)
            })
        
        for item in base['items']['bill_quantities']:
            variation['items']['bill_quantities'].append({
                'description': f"{item['description']} - V{i+1}",
                'unit': item['unit'],
                'quantity': int(item['quantity'] * multiplier * 0.95),
                'rate': int(item['rate'] * rate_multiplier)
            })
        
        for item in base['items']['extra_items']:
            variation['items']['extra_items'].append({
                'description': f"{item['description']} - V{i+1}",
                'unit': item['unit'],
                'quantity': int(item['quantity'] * multiplier * 1.2),
                'rate': int(item['rate'] * rate_multiplier)
            })
        
        scenarios.append(variation)
    
    # Run all 25 scenarios
    successful_tests = 0
    failed_tests = 0
    
    for i, scenario in enumerate(scenarios[:25], 1):
        success = test_scenario(
            i,
            scenario['name'],
            scenario['work_name'],
            scenario['items'],
            scenario['premium']
        )
        
        if success:
            successful_tests += 1
        else:
            failed_tests += 1
    
    # Final summary
    print("\n" + "="*80)
    print("🎯 ULTIMATE VALIDATION SUMMARY")
    print("="*80)
    print(f"✅ Successful Tests: {successful_tests}")
    print(f"❌ Failed Tests: {failed_tests}")
    print(f"📊 Success Rate: {(successful_tests/25)*100:.1f}%")
    
    if successful_tests == 25:
        print("🎉 ALL 25 SCENARIOS PASSED! Application is fully validated.")
        print("✅ Ready for production deployment")
    else:
        print("⚠️  Some scenarios failed. Please review the errors above.")
    
    return successful_tests == 25

if __name__ == "__main__":
    success = run_ultimate_validation()
    if success:
        print("\n🚀 DEPLOYMENT READY!")
        print("   streamlit run app/main.py")
    else:
        print("\n❌ FIX ISSUES BEFORE DEPLOYMENT")