# Stream Bill Generator

A professional infrastructure bill generation system built with Streamlit.

## Features

- Generate contractor bills from Excel data
- Create deviation statements
- Generate statutory documents
- Export to PDF and Word formats
- Automatic calculations with premium adjustments

## Requirements

- Python 3.8+
- See `requirements.txt` for Python dependencies
- See `packages.txt` for system dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app/main.py
```

## Deployment

This app is optimized for Streamlit Cloud deployment. Simply point to `app/main.py` as the main file.

## Required Excel Format

The app requires an Excel file with three sheets:
1. Work Order
2. Bill Quantity
3. Extra Items

Each sheet should follow the standard format with headers in row 20.

# Stream Bill App

A comprehensive bill generation application built with Streamlit for PWD (Public Works Department) billing processes.

## Features

- **Bill Generation**: Generate detailed bills with multiple templates
- **PDF Export**: High-quality PDF output with professional formatting
- **Template System**: Multiple HTML templates for different bill types
- **Certificate Generation**: Automated certificate creation
- **Deviation Statements**: Handle bill deviations and extra items
- **Multi-language Support**: Hindi and English language support

## Installation

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app/main.py
```

### Docker Installation
```bash
# Build and run with Docker
docker-compose up --build
```

## Project Structure

```
Stream-Bill-App_Main/
├── app/                    # Main application code
├── core/                   # Core business logic
├── templates/              # HTML templates for PDF generation
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
├── packages.txt           # System packages for Streamlit Cloud
└── README.md              # This file
```

## Usage

1. Launch the application using `streamlit run app/main.py`
2. Upload your bill data (Excel format)
3. Select the appropriate template
4. Configure bill parameters
5. Generate and download PDF output

## Templates Available

- **First Page**: Bill header and summary
- **Note Sheet**: Detailed item breakdown
- **Last Page**: Totals and signatures
- **Extra Items**: Additional items and deviations
- **Certificates**: Official certificates (Type II & III)
- **Deviation Statement**: Bill deviation documentation

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- WeasyPrint (for PDF generation)
- Jinja2 (for templating)

## License

This project is licensed under the MIT License.

## Author

Developed by CRAJKUMARSINGH