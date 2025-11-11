# Streamlit Deployment Guide

## Features Added ✅

### 1. Download Options
- **Individual PDF Downloads**: Download each document separately
- **ZIP Download**: Download all PDFs in a single ZIP file
- Available in all three modes (Single Upload, Test Run, Batch Process)

### 2. Test Run with Sample Files
- Works with files in `test_input_files` folder
- **Deployment Ready**: Files are included in the repository
- Select any sample file from dropdown
- Process and download immediately

### 3. Three Processing Modes

#### Mode 1: Single File Upload
- Upload your own Excel file
- Configure premium settings
- Generate and download PDFs instantly

#### Mode 2: Test Run (Sample Files)
- Use pre-loaded sample files from `test_input_files`
- Perfect for testing in Streamlit Cloud
- No file upload needed

#### Mode 3: Batch Process All Files
- Process all files in `test_input_files` folder
- Download master ZIP with all results
- Organized by file name

## Deployment to Streamlit Cloud

### Prerequisites
1. Push your code to GitHub
2. Ensure `test_input_files` folder is committed
3. Ensure `templates` folder is committed

### Steps
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

### Important Notes

#### wkhtmltopdf Installation
Streamlit Cloud may not have wkhtmltopdf pre-installed. Add this to `packages.txt`:
```
wkhtmltopdf
```

Or create `packages.txt` in root:
```bash
wkhtmltopdf
xvfb
```

#### Requirements
Ensure `requirements.txt` includes:
```
streamlit
pandas
openpyxl
jinja2
```

### Testing Deployment
1. After deployment, select "Test Run (Sample Files)" mode
2. Choose a sample file from dropdown
3. Click "Process Selected File"
4. Download PDFs or ZIP

## Local Testing

Run locally:
```bash
streamlit run app.py
```

Access at: http://localhost:8501

## Folder Structure
```
project/
├── app.py                      # Main Streamlit app
├── templates/                  # HTML templates
│   ├── first_page.html
│   ├── deviation_statement.html
│   ├── extra_items.html
│   └── note_sheet.html
├── test_input_files/          # Sample files for testing
│   ├── sample1.xlsx
│   ├── sample2.xlsx
│   └── ...
├── core/                      # Core processing logic
│   └── computations/
│       └── bill_processor.py
├── exports/                   # Export utilities
│   └── renderers.py
├── requirements.txt           # Python dependencies
└── packages.txt              # System packages (for Streamlit Cloud)
```

## Troubleshooting

### PDF Generation Fails
- Check if wkhtmltopdf is installed
- HTML files are still generated and available
- Download HTML files and convert locally

### Sample Files Not Found
- Ensure `test_input_files` folder is committed to Git
- Check folder name is exactly `test_input_files`
- Verify Excel files are present

### Download Buttons Not Working
- Check browser popup blocker
- Try different browser
- Ensure files were generated successfully

## Support
For issues, check the error details in the expander section of the app.
