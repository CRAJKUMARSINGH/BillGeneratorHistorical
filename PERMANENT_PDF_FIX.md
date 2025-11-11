# PERMANENT PDF FIX - No More Table Shrinking!

## The Problem
wkhtmltopdf shrinks tables when converting HTML to PDF, destroying the elegant layout.

## The PERMANENT Solution

### 1. Add These CSS Rules to ALL Templates

```css
@page {
    size: A4 portrait; /* or landscape */
    margin: 10mm;
}

body {
    font-family: Calibri, sans-serif;
    font-size: 8pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

table {
    width: 190mm !important; /* 210mm - 20mm margins = 190mm */
    max-width: 190mm !important;
    min-width: 190mm !important;
    border-collapse: collapse;
    table-layout: fixed !important;
    font-size: 8pt;
}

/* Prevent any scaling */
* {
    -webkit-transform: scale(1) !important;
    transform: scale(1) !important;
    zoom: 1 !important;
}
```

### 2. Use These wkhtmltopdf Options

```bash
wkhtmltopdf \
  --enable-local-file-access \
  --page-size A4 \
  --margin-top 10mm \
  --margin-bottom 10mm \
  --margin-left 10mm \
  --margin-right 10mm \
  --orientation Portrait \
  --no-pdf-compression \
  --disable-smart-shrinking \
  --zoom 1.0 \
  input.html output.pdf
```

### 3. Key Options Explained

- `--disable-smart-shrinking` - **CRITICAL!** Prevents automatic scaling
- `--zoom 1.0` - Forces 100% zoom, no scaling
- `--no-pdf-compression` - Better quality
- `--dpi 96` - Standard screen DPI

## Implementation

I'm applying this fix to ALL templates now.
