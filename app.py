"""
Stream-Bill-App_Main - Streamlit Application
Simple Streamlit app for cloud deployment
"""

import streamlit as st
import pandas as pd
import os

def main():
    st.set_page_config(
        page_title="Stream-Bill-App_Main",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Stream-Bill-App_Main")
    st.markdown("Welcome to Stream-Bill-App_Main - Professional Bill Generation")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload your bill data in Excel format"
    )
    
    if uploaded_file is not None:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded successfully!")
            
            # Display data preview
            st.subheader("📊 Data Preview")
            st.dataframe(df.head())
            
            # Basic info
            st.subheader("📈 File Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Size", f"{uploaded_file.size} bytes")
            
            # Show columns
            st.subheader("📋 Columns")
            st.write(list(df.columns))
            
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