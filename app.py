"""
Stream-Bill-App_Main - Streamlit Application
Professional Bill Generation with Batch Processing
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import zipfile
import tempfile

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.computations.bill_processor import process_bill
from exports.renderers import generate_html

def generate_pdf_from_html(html_path, pdf_path):
    """Generate PDF from HTML using wkhtmltopdf"""
    try:
        # Determine orientation
        orientation = "Landscape" if "deviation" in str(html_path) else "Portrait"
        
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--page-size', 'A4',
            '--margin-top', '10mm',
            '--margin-bottom', '10mm',
            '--margin-left', '10mm',
            '--margin-right', '10mm',
            '--orientation', orientation,
            '--disable-smart-shrinking',
            '--zoom', '1.0',
            '--dpi', '96',
            str(html_path),
            str(pdf_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0 and os.path.exists(pdf_path)
    except:
        return False

def create_zip_file(files, zip_path):
    """Create ZIP file from list of files"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
    return zip_path

def process_batch_files(excel_files):
    """Process multiple Excel files in batch"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_base_dir = Path("batch_outputs")
    output_base_dir.mkdir(exist_ok=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, excel_file in enumerate(excel_files):
        progress = (i + 1) / len(excel_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1}/{len(excel_files)}: {excel_file.name}")
        
        try:
            # Load Excel
            xl_file = pd.ExcelFile(excel_file)
            ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
            ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
            ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
            
            # Process bill
            premium_percent = 5.0
            premium_type = "above"
            
            first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
                ws_wo, ws_bq, ws_extra, premium_percent, premium_type, 0
            )
            
            # Create output directory
            safe_name = "".join(c if c.isalnum() else "_" for c in excel_file.stem).lower()
            file_output_dir = output_base_dir / f"{timestamp}_{safe_name}"
            file_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate HTML files
            template_dir = "templates"
            html_files = []
            
            for template_name, data in [
                ("first_page", first_page_data),
                ("deviation_statement", deviation_data),
                ("extra_items", extra_items_data),
                ("note_sheet", note_sheet_data),
                ("certificate_ii", {"measurement_officer": "Junior Engineer", "measurement_date": datetime.now().strftime('%d/%m/%Y')}),
                ("certificate_iii", first_page_data)
            ]:
                html_path = generate_html(template_name, data, template_dir, str(file_output_dir))
                if os.path.exists(html_path):
                    html_files.append(Path(html_path).name)
            
            results.append({
                'filename': excel_file.name,
                'status': 'SUCCESS',
                'files': len(html_files),
                'output_dir': file_output_dir.name
            })
            
        except Exception as e:
            results.append({
                'filename': excel_file.name,
                'status': 'FAILED',
                'error': str(e)
            })
    
    # Show results
    progress_bar.empty()
    status_text.empty()
    
    st.success(f"✅ Batch processing complete! Processed {len(excel_files)} files")
    
    # Results table
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    fail_count = len(results) - success_count
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Files", len(results))
    with col2:
        st.metric("Successful", success_count)
    with col3:
        st.metric("Failed", fail_count)
    
    # Detailed results
    with st.expander("📊 Detailed Results"):
        for result in results:
            if result['status'] == 'SUCCESS':
                st.success(f"✅ {result['filename']} - {result['files']} HTML files generated")
                st.caption(f"Output: {result['output_dir']}")
            else:
                st.error(f"❌ {result['filename']} - {result.get('error', 'Unknown error')}")
    
    st.info(f"📁 All outputs saved in: batch_outputs/{timestamp}_*")
    
    # Generate PDFs and create master ZIP
    if success_count > 0:
        st.subheader("📥 Download All Batch Results")
        
        with st.spinner("Generating PDFs for all files..."):
            all_pdf_files = []
            
            for result in results:
                if result['status'] == 'SUCCESS':
                    result_dir = output_base_dir / result['output_dir']
                    html_files = list(result_dir.glob("*.html"))
                    
                    for html_path in html_files:
                        pdf_path = html_path.with_suffix('.pdf')
                        if generate_pdf_from_html(html_path, pdf_path):
                            all_pdf_files.append(pdf_path)
            
            if all_pdf_files:
                st.success(f"✅ Generated {len(all_pdf_files)} PDF files across all batches!")
                
                # Create master ZIP
                master_zip_filename = f"batch_all_bills_{timestamp}.zip"
                master_zip_path = output_base_dir / master_zip_filename
                
                with zipfile.ZipFile(master_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for pdf_file in all_pdf_files:
                        # Include folder name in ZIP structure
                        arcname = f"{pdf_file.parent.name}/{pdf_file.name}"
                        zipf.write(pdf_file, arcname)
                
                # Download button for master ZIP
                with open(master_zip_path, 'rb') as f:
                    st.download_button(
                        label=f"⬇️ Download All Bills (ZIP - {len(all_pdf_files)} PDFs)",
                        data=f.read(),
                        file_name=master_zip_filename,
                        mime="application/zip",
                        use_container_width=True,
                        type="primary"
                    )
            else:
                st.warning("⚠️ PDF generation failed. Please check if wkhtmltopdf is installed.")
                st.info("HTML files are still available in the batch_outputs folder.")

def main():
    st.set_page_config(
        page_title="Bill Generator Pro",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Professional Bill Generator")
    st.markdown("Generate contractor bills, deviation statements, and all required documents")
    
    # Sidebar for mode selection
    st.sidebar.title("⚙️ Options")
    mode = st.sidebar.radio(
        "Select Mode",
        ["Single File Upload", "Test Run (Sample Files)", "Batch Process All Files"],
        help="Choose mode: Upload file, test with samples, or batch process all"
    )
    
    if mode == "Test Run (Sample Files)":
        st.header("🧪 Test Run with Sample Files")
        st.markdown("Test the system using sample files from `test_input_files` folder")
        
        # Check if test_input_files exists
        test_input_dir = Path("test_input_files")
        if not test_input_dir.exists():
            st.error("❌ test_input_files folder not found!")
            return
        
        # Get available files
        excel_files = list(test_input_dir.glob("*.xlsx"))
        
        if not excel_files:
            st.warning("⚠️ No Excel files found in test_input_files folder")
            return
        
        st.success(f"✅ Found {len(excel_files)} sample files")
        
        # File selector
        selected_file = st.selectbox(
            "Select a sample file to test",
            excel_files,
            format_func=lambda x: x.name
        )
        
        # Settings
        col1, col2 = st.columns(2)
        with col1:
            premium_percent = st.number_input("Premium %", value=5.0, min_value=0.0, max_value=100.0, step=0.1)
        with col2:
            premium_type = st.radio("Premium Type", ["above", "below"], horizontal=True)
        
        # Process button
        if st.button("🚀 Process Selected File", type="primary", use_container_width=True):
            with st.spinner(f"Processing {selected_file.name}..."):
                try:
                    # Load Excel
                    xl_file = pd.ExcelFile(selected_file)
                    ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
                    ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
                    ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
                    
                    # Process bill
                    first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
                        ws_wo, ws_bq, ws_extra, premium_percent, premium_type, 0
                    )
                    
                    # Create output directory
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = Path("test_outputs") / f"test_run_{timestamp}"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Generate HTML files
                    template_dir = "templates"
                    html_files = []
                    
                    for template_name, data in [
                        ("first_page", first_page_data),
                        ("deviation_statement", deviation_data),
                        ("extra_items", extra_items_data),
                        ("note_sheet", note_sheet_data),
                    ]:
                        html_path = generate_html(template_name, data, template_dir, str(output_dir))
                        if os.path.exists(html_path):
                            html_files.append(Path(html_path).name)
                    
                    st.success(f"✅ Generated {len(html_files)} HTML files!")
                    
                    # Show results
                    st.subheader("📊 Financial Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Grand Total", f"₹{first_page_data['totals']['grand_total']:,.2f}")
                    with col2:
                        st.metric("Premium", f"₹{first_page_data['totals']['premium']['amount']:,.2f}")
                    with col3:
                        st.metric("Payable", f"₹{first_page_data['totals']['payable']:,.2f}")
                    
                    # Deviation summary
                    st.subheader("📈 Deviation Summary")
                    summary = deviation_data["summary"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Net Difference", f"₹{summary['net_difference']:,.2f}", 
                                 delta="Saving" if summary['is_saving'] else "Excess")
                    with col2:
                        st.metric("Percentage Deviation", f"{summary['percentage_deviation']:.2f}%")
                    
                    # Generated files
                    with st.expander("📄 Generated Files"):
                        st.info(f"Output folder: {output_dir}")
                        for file in html_files:
                            st.write(f"✅ {file}")
                    
                    # Generate PDFs
                    st.subheader("📥 Download Options")
                    
                    with st.spinner("Generating PDFs..."):
                        pdf_files = []
                        for html_file in html_files:
                            html_path = output_dir / html_file
                            pdf_file = html_file.replace('.html', '.pdf')
                            pdf_path = output_dir / pdf_file
                            
                            if generate_pdf_from_html(html_path, pdf_path):
                                pdf_files.append(pdf_path)
                        
                        if pdf_files:
                            st.success(f"✅ Generated {len(pdf_files)} PDF files!")
                            
                            # Create ZIP file
                            zip_filename = f"bill_documents_{timestamp}.zip"
                            zip_path = output_dir / zip_filename
                            create_zip_file(pdf_files, zip_path)
                            
                            # Download buttons
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Download individual PDFs
                                st.markdown("**📄 Individual PDFs:**")
                                for pdf_file in pdf_files:
                                    with open(pdf_file, 'rb') as f:
                                        st.download_button(
                                            label=f"⬇️ {pdf_file.name}",
                                            data=f.read(),
                                            file_name=pdf_file.name,
                                            mime="application/pdf",
                                            use_container_width=True
                                        )
                            
                            with col2:
                                # Download ZIP
                                st.markdown("**📦 All Documents (ZIP):**")
                                with open(zip_path, 'rb') as f:
                                    st.download_button(
                                        label=f"⬇️ Download All PDFs (ZIP)",
                                        data=f.read(),
                                        file_name=zip_filename,
                                        mime="application/zip",
                                        use_container_width=True
                                    )
                        else:
                            st.warning("⚠️ PDF generation failed. Please check if wkhtmltopdf is installed.")
                            st.info("HTML files are still available in the output folder.")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())
        
        return
    
    if mode == "Batch Process All Files":
        st.header("🔄 Batch Process All Files")
        st.markdown("Process all Excel files from `test_input_files` folder and generate HTML outputs")
        
        # Check if test_input_files exists
        test_input_dir = Path("test_input_files")
        if not test_input_dir.exists():
            st.error("❌ test_input_files folder not found!")
            return
        
        # Count files
        excel_files = list(test_input_dir.glob("*.xlsx"))
        st.info(f"📂 Found {len(excel_files)} Excel files in test_input_files folder")
        
        # Show file list
        if excel_files:
            with st.expander("📋 Files to Process"):
                for i, f in enumerate(excel_files, 1):
                    st.write(f"{i}. {f.name}")
        
        # Batch process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Batch Processing", type="primary", use_container_width=True):
                process_batch_files(excel_files)
        
        return
    
    # Single File Upload Mode
    st.header("📤 Upload Your Excel File")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload your bill data in Excel format with Work Order, Bill Quantity, and Extra Items sheets"
    )
    
    if uploaded_file is not None:
        try:
            # Settings
            col1, col2 = st.columns(2)
            with col1:
                premium_percent = st.number_input("Premium %", value=5.0, min_value=0.0, max_value=100.0, step=0.1)
            with col2:
                premium_type = st.radio("Premium Type", ["above", "below"], horizontal=True)
            
            # Process button
            if st.button("🚀 Generate Bill Documents", type="primary", use_container_width=True):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        # Load Excel
                        xl_file = pd.ExcelFile(uploaded_file)
                        ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
                        ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
                        ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
                        
                        # Process bill
                        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
                            ws_wo, ws_bq, ws_extra, premium_percent, premium_type, 0
                        )
                        
                        # Create output directory
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_name = "".join(c if c.isalnum() else "_" for c in uploaded_file.name.replace('.xlsx', '').replace('.xls', '')).lower()
                        output_dir = Path("uploaded_outputs") / f"upload_{safe_name}_{timestamp}"
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Generate HTML files
                        template_dir = "templates"
                        html_files = []
                        
                        for template_name, data in [
                            ("first_page", first_page_data),
                            ("deviation_statement", deviation_data),
                            ("extra_items", extra_items_data),
                            ("note_sheet", note_sheet_data),
                        ]:
                            html_path = generate_html(template_name, data, template_dir, str(output_dir))
                            if os.path.exists(html_path):
                                html_files.append(Path(html_path).name)
                        
                        st.success(f"✅ Generated {len(html_files)} HTML files!")
                        
                        # Show results
                        st.subheader("📊 Financial Summary")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Grand Total", f"₹{first_page_data['totals']['grand_total']:,.2f}")
                        with col2:
                            st.metric("Premium", f"₹{first_page_data['totals']['premium']['amount']:,.2f}")
                        with col3:
                            st.metric("Payable", f"₹{first_page_data['totals']['payable']:,.2f}")
                        
                        # Deviation summary
                        st.subheader("📈 Deviation Summary")
                        summary = deviation_data["summary"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Net Difference", f"₹{summary['net_difference']:,.2f}", 
                                     delta="Saving" if summary['is_saving'] else "Excess")
                        with col2:
                            st.metric("Percentage Deviation", f"{summary['percentage_deviation']:.2f}%")
                        
                        # Generate PDFs
                        st.subheader("📥 Download Options")
                        
                        with st.spinner("Generating PDFs..."):
                            pdf_files = []
                            for html_file in html_files:
                                html_path = output_dir / html_file
                                pdf_file = html_file.replace('.html', '.pdf')
                                pdf_path = output_dir / pdf_file
                                
                                if generate_pdf_from_html(html_path, pdf_path):
                                    pdf_files.append(pdf_path)
                            
                            if pdf_files:
                                st.success(f"✅ Generated {len(pdf_files)} PDF files!")
                                
                                # Create ZIP file
                                zip_filename = f"bill_documents_{safe_name}_{timestamp}.zip"
                                zip_path = output_dir / zip_filename
                                create_zip_file(pdf_files, zip_path)
                                
                                # Download buttons
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Download individual PDFs
                                    st.markdown("**📄 Individual PDFs:**")
                                    for pdf_file in pdf_files:
                                        with open(pdf_file, 'rb') as f:
                                            st.download_button(
                                                label=f"⬇️ {pdf_file.name}",
                                                data=f.read(),
                                                file_name=pdf_file.name,
                                                mime="application/pdf",
                                                use_container_width=True
                                            )
                                
                                with col2:
                                    # Download ZIP
                                    st.markdown("**📦 All Documents (ZIP):**")
                                    with open(zip_path, 'rb') as f:
                                        st.download_button(
                                            label=f"⬇️ Download All PDFs (ZIP)",
                                            data=f.read(),
                                            file_name=zip_filename,
                                            mime="application/zip",
                                            use_container_width=True
                                        )
                            else:
                                st.warning("⚠️ PDF generation failed. Please check if wkhtmltopdf is installed.")
                                st.info("HTML files are still available in the output folder.")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        with st.expander("Error Details"):
                            st.code(traceback.format_exc())
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    
    # Instructions
    with st.expander("📋 Instructions"):
        st.markdown("""
        1. **Upload Excel File**: Choose your bill data file (.xlsx or .xls)
        2. **Preview Data**: Review your uploaded data
        3. **Process**: The app will show basic information about your file
        
        **Supported formats:**
        - Excel files (.xlsx, .xls)
        - CSV files (coming soon)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Stream-Bill-App_Main - Professional Bill Generation System*")

if __name__ == "__main__":
    main()