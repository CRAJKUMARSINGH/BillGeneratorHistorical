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
    """Generate PDF from HTML using Chrome Headless (NO SHRINKING!)"""
    import shutil
    
    # Try Chrome first (BEST - No shrinking!)
    chrome_paths = [
        'chromium',              # Streamlit Cloud (Linux)
        'chromium-browser',      # Ubuntu/Debian
        'google-chrome',         # Google Chrome on Linux
        'chrome',                # Generic
        '/usr/bin/chromium',     # Streamlit Cloud path
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # Windows
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    chrome_exe = None
    for path in chrome_paths:
        found = shutil.which(path) if not os.path.isabs(path) else path
        if found and os.path.exists(found):
            chrome_exe = found
            break
    
    if chrome_exe:
        try:
            # CHROME HEADLESS - PERFECT PDF GENERATION (NO SHRINKING, NO HEADERS/FOOTERS!)
            cmd = [
                chrome_exe,
                '--headless',
                '--disable-gpu',
                '--no-margins',
                '--disable-smart-shrinking',
                '--run-all-compositor-stages-before-draw',
                '--no-pdf-header-footer',  # REMOVE TIMESTAMP AND FILE PATH
                '--print-to-pdf=' + str(os.path.abspath(pdf_path)),
                'file:///' + str(os.path.abspath(html_path)).replace('\\', '/')
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(pdf_path):
                print(f"✅ PDF generated with Chrome: {pdf_path}")
                return True
            else:
                print(f"Chrome error: {result.stderr.decode() if result.stderr else 'Unknown'}")
        except Exception as e:
            print(f"Chrome exception: {str(e)}")
    
    # Fallback to wkhtmltopdf
    try:
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
            '--print-media-type',
            '--no-header-line',  # Remove header line
            '--no-footer-line',  # Remove footer line
            str(html_path),
            str(pdf_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(pdf_path):
            print(f"✅ PDF generated with wkhtmltopdf: {pdf_path}")
            return True
        else:
            print(f"wkhtmltopdf error: {result.stderr.decode() if result.stderr else 'Unknown'}")
            return False
            
    except Exception as e:
        print(f"PDF generation failed: {str(e)}")
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
    st.balloons()  # 🎈 Celebration!
    
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
                st.balloons()  # 🎈 Celebration!
                
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
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for beautiful green header
    st.markdown("""
        <style>
        /* Green Header Styling */
        .main-header {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        .main-header p {
            color: #ecf0f1;
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
        }
        
        /* Sidebar Styling - Colorful! */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Button Styling */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Download Button Styling */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2ecc71;
        }
        
        /* Success Messages */
        .element-container div[data-testid="stMarkdownContainer"] > div[data-testid="stMarkdown"] {
            border-radius: 8px;
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed #2ecc71;
            border-radius: 10px;
            padding: 1rem;
            background: #f8f9fa;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Beautiful Header with Credits
    st.markdown("""
        <div class="main-header">
            <h1>📄 Professional Bill Generator</h1>
            <p>🏗️ Generate contractor bills, deviation statements, and all required documents with zero shrinking PDFs</p>
            <div style='text-align: center; margin-top: 1rem; padding: 0.8rem; background: rgba(255,255,255,0.15); 
                        border-radius: 8px;'>
                <p style='margin: 0; font-size: 0.85rem; color: #ecf0f1;'>Prepared on Initiative of</p>
                <p style='margin: 0.3rem 0; font-size: 1.1rem; font-weight: 700; color: white;'>Mrs. Premlata Jain, AAO, PWD Udaipur</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for mode selection
    st.sidebar.markdown("### ⚙️ Processing Options")
    
    # Info box in sidebar
    st.sidebar.markdown("""
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; 
                    border-left: 4px solid #ffd700; margin: 1rem 0;'>
            <p style='margin: 0; color: white; font-weight: 600;'>✨ Features:</p>
            <ul style='margin: 0.5rem 0; padding-left: 1.5rem; color: white;'>
                <li>📄 Zero-shrinking PDFs</li>
                <li>🎨 Professional formatting</li>
                <li>📦 Batch processing</li>
                <li>⬇️ Instant downloads</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    mode = st.sidebar.radio(
        "Select Processing Mode",
        ["Single File Upload", "Test Run (Sample Files)", "Batch Process All Files"],
        help="Choose mode: Upload file, test with samples, or batch process all"
    )
    
    # Add footer to sidebar with credits
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style='text-align: center; color: white; font-size: 0.85rem;'>
            <p style='margin: 0.3rem 0;'><strong>Bill Generator Pro</strong></p>
            <p style='margin: 0.3rem 0; opacity: 0.9;'>Powered by Chrome Headless</p>
            <p style='margin: 0.3rem 0; opacity: 0.9;'>Version 2.0</p>
            <hr style='margin: 0.8rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.3);'>
            <p style='margin: 0.3rem 0; font-size: 0.75rem;'><strong>🌟 Prepared on Initiative of:</strong></p>
            <p style='margin: 0.3rem 0; color: #ffd700; font-weight: 600; font-size: 0.85rem;'>Mrs. Premlata Jain, AAO</p>
            <p style='margin: 0.3rem 0; font-size: 0.75rem; opacity: 0.9;'>PWD Udaipur</p>
        </div>
    """, unsafe_allow_html=True)
    
    if mode == "Test Run (Sample Files)":
        st.markdown("""
            <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                        padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                <h2 style='color: white; margin: 0;'>🧪 Test Run with Sample Files</h2>
                <p style='color: #ecf0f1; margin: 0.5rem 0 0 0;'>
                    Test the system using pre-loaded sample files - Perfect for trying out the app!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        # Show available files in a nice card
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
                <div style='background: #d5f4e6; padding: 1rem; border-radius: 8px; 
                            border-left: 4px solid #2ecc71; margin: 1rem 0;'>
                    <p style='margin: 0; color: #27ae60; font-weight: 600;'>
                        ✅ Found {len(excel_files)} sample files ready for testing
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # File selector with better styling
        st.markdown("#### 📁 Select a Sample File")
        selected_file = st.selectbox(
            "Choose file to process:",
            excel_files,
            format_func=lambda x: x.name,
            label_visibility="collapsed"
        )
        
        # Settings with better styling
        st.markdown("#### ⚙️ Configuration")
        col1, col2, col3 = st.columns(3)
        with col1:
            premium_percent = st.number_input(
                "💰 Premium Percentage", 
                value=5.0, 
                min_value=0.0, 
                max_value=100.0, 
                step=0.1,
                help="Enter the premium percentage to apply"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            premium_type = st.radio(
                "📊 Premium Type", 
                ["above", "below"], 
                horizontal=True,
                help="Select whether premium is above or below the base amount"
            )
        with col3:
            last_bill_amount = st.number_input(
                "💵 Last Bill Amount", 
                value=0.0, 
                min_value=0.0, 
                step=1000.0,
                help="Amount paid in last bill (0 for first bill)"
            )
        
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
                        ws_wo, ws_bq, ws_extra, premium_percent, premium_type, last_bill_amount
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
                    
                    # Generate PDFs and Word documents
                    st.subheader("📥 Download Options")
                    
                    with st.spinner("Generating PDFs and Word documents..."):
                        pdf_files = []
                        word_files = []
                        
                        # Generate PDFs
                        for html_file in html_files:
                            html_path = output_dir / html_file
                            pdf_file = html_file.replace('.html', '.pdf')
                            pdf_path = output_dir / pdf_file
                            
                            if generate_pdf_from_html(html_path, pdf_path):
                                pdf_files.append(pdf_path)
                        
                        # Generate Word documents
                        from exports.word_generator import generate_first_page_docx, generate_deviation_statement_docx, generate_extra_items_docx
                        
                        try:
                            # First Page Word
                            word_path = output_dir / "first_page.docx"
                            generate_first_page_docx(first_page_data, str(word_path))
                            if word_path.exists():
                                word_files.append(word_path)
                        except Exception as e:
                            print(f"Word generation error: {e}")
                        
                        try:
                            # Deviation Statement Word
                            word_path = output_dir / "deviation_statement.docx"
                            generate_deviation_statement_docx(deviation_data, str(word_path))
                            if word_path.exists():
                                word_files.append(word_path)
                        except Exception as e:
                            print(f"Word generation error: {e}")
                        
                        try:
                            # Extra Items Word
                            word_path = output_dir / "extra_items.docx"
                            generate_extra_items_docx(extra_items_data, str(word_path))
                            if word_path.exists():
                                word_files.append(word_path)
                        except Exception as e:
                            print(f"Word generation error: {e}")
                        
                        if pdf_files or word_files:
                            st.success(f"✅ Generated {len(pdf_files)} PDFs and {len(word_files)} Word documents!")
                            st.balloons()  # 🎈 Celebration!
                            
                            # Create ZIP file with both PDFs and Word files
                            zip_filename = f"bill_documents_{timestamp}.zip"
                            zip_path = output_dir / zip_filename
                            all_files = pdf_files + word_files
                            create_zip_file(all_files, zip_path)
                            
                            # Download buttons
                            col1, col2, col3 = st.columns(3)
                            
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
                                # Download Word files
                                st.markdown("**📝 Word Documents:**")
                                for word_file in word_files:
                                    with open(word_file, 'rb') as f:
                                        st.download_button(
                                            label=f"⬇️ {word_file.name}",
                                            data=f.read(),
                                            file_name=word_file.name,
                                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                            use_container_width=True
                                        )
                            
                            with col3:
                                # Download ZIP
                                st.markdown("**📦 All Documents (ZIP):**")
                                with open(zip_path, 'rb') as f:
                                    st.download_button(
                                        label=f"⬇️ Download All (ZIP)",
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
        st.markdown("""
            <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                        padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                <h2 style='color: white; margin: 0;'>🔄 Batch Process All Files</h2>
                <p style='color: #ecf0f1; margin: 0.5rem 0 0 0;'>
                    Process multiple Excel files at once and download all results in a single ZIP
                </p>
            </div>
        """, unsafe_allow_html=True)
        
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
    st.markdown("""
        <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0;'>📤 Upload Your Excel File</h2>
            <p style='color: #ecf0f1; margin: 0.5rem 0 0 0;'>
                Upload your own bill data and generate professional documents instantly
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload your bill data in Excel format with Work Order, Bill Quantity, and Extra Items sheets"
    )
    
    if uploaded_file is not None:
        try:
            # Settings
            col1, col2, col3 = st.columns(3)
            with col1:
                premium_percent = st.number_input("Premium %", value=5.0, min_value=0.0, max_value=100.0, step=0.1)
            with col2:
                premium_type = st.radio("Premium Type", ["above", "below"], horizontal=True)
            with col3:
                last_bill_amount = st.number_input("Last Bill Amount", value=0.0, min_value=0.0, step=1000.0)
            
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
                            ws_wo, ws_bq, ws_extra, premium_percent, premium_type, last_bill_amount
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
                        
                        # Generate PDFs and Word documents
                        st.subheader("📥 Download Options")
                        
                        with st.spinner("Generating PDFs and Word documents..."):
                            pdf_files = []
                            word_files = []
                            
                            # Generate PDFs
                            for html_file in html_files:
                                html_path = output_dir / html_file
                                pdf_file = html_file.replace('.html', '.pdf')
                                pdf_path = output_dir / pdf_file
                                
                                if generate_pdf_from_html(html_path, pdf_path):
                                    pdf_files.append(pdf_path)
                            
                            # Generate Word documents
                            from exports.word_generator import generate_first_page_docx, generate_deviation_statement_docx, generate_extra_items_docx
                            
                            try:
                                word_path = output_dir / "first_page.docx"
                                generate_first_page_docx(first_page_data, str(word_path))
                                if word_path.exists():
                                    word_files.append(word_path)
                            except: pass
                            
                            try:
                                word_path = output_dir / "deviation_statement.docx"
                                generate_deviation_statement_docx(deviation_data, str(word_path))
                                if word_path.exists():
                                    word_files.append(word_path)
                            except: pass
                            
                            try:
                                word_path = output_dir / "extra_items.docx"
                                generate_extra_items_docx(extra_items_data, str(word_path))
                                if word_path.exists():
                                    word_files.append(word_path)
                            except: pass
                            
                            if pdf_files or word_files:
                                st.success(f"✅ Generated {len(pdf_files)} PDFs and {len(word_files)} Word documents!")
                                st.balloons()  # 🎈 Celebration!
                                
                                # Create ZIP file
                                zip_filename = f"bill_documents_{safe_name}_{timestamp}.zip"
                                zip_path = output_dir / zip_filename
                                all_files = pdf_files + word_files
                                create_zip_file(all_files, zip_path)
                                
                                # Download buttons
                                col1, col2, col3 = st.columns(3)
                                
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
                                    # Download Word files
                                    st.markdown("**📝 Word Documents:**")
                                    for word_file in word_files:
                                        with open(word_file, 'rb') as f:
                                            st.download_button(
                                                label=f"⬇️ {word_file.name}",
                                                data=f.read(),
                                                file_name=word_file.name,
                                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                use_container_width=True
                                            )
                                
                                with col3:
                                    # Download ZIP
                                    st.markdown("**📦 All Documents (ZIP):**")
                                    with open(zip_path, 'rb') as f:
                                        st.download_button(
                                            label=f"⬇️ Download All (ZIP)",
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
    
    # Beautiful Footer with Credits
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); 
                    border-radius: 10px; margin-top: 3rem;'>
            <h3 style='color: white; margin: 0;'>📄 Bill Generator Pro</h3>
            <p style='color: #bdc3c7; margin: 0.5rem 0;'>
                Professional Infrastructure Bill Generation System
            </p>
            <p style='color: #95a5a6; font-size: 0.9rem; margin: 0.5rem 0;'>
                ✨ Zero-Shrinking PDFs | 🚀 Chrome Headless Powered | 📦 Batch Processing
            </p>
            <div style='margin: 1.5rem 0; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;'>
                <p style='color: #ecf0f1; font-size: 1rem; margin: 0.3rem 0;'>
                    <strong>🌟 Prepared on Initiative of</strong>
                </p>
                <p style='color: #f39c12; font-size: 1.2rem; font-weight: 700; margin: 0.5rem 0;'>
                    Mrs. Premlata Jain, AAO
                </p>
                <p style='color: #bdc3c7; font-size: 0.95rem; margin: 0.3rem 0;'>
                    PWD Udaipur
                </p>
            </div>
            <p style='color: #7f8c8d; font-size: 0.8rem; margin: 0.5rem 0 0 0;'>
                Version 2.0 | Made with ❤️ for Infrastructure Projects
            </p>
            <p style='color: #7f8c8d; font-size: 0.75rem; margin: 0.5rem 0 0 0;'>
                © 2024 Bill Generator Pro | All Rights Reserved
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()