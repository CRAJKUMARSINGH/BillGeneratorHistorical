"""
Generate Word (.docx) files from HTML outputs
For easy last-minute edits by non-technical users
"""
import os
from pathlib import Path

print("""
================================================================================
WORD FILE GENERATION - For Easy Editing
================================================================================

This feature generates editable Word (.docx) files alongside HTML files.
Perfect for last-minute edits by non-technical users!

INSTALLATION REQUIRED:
  pip install python-docx

Once installed, Word files will be automatically generated during batch processing.

BENEFITS:
  - Easy to edit by anyone (no HTML knowledge needed)
  - Preserve formatting
  - Make last-minute changes
  - Print directly from Word

================================================================================
""")

try:
    from docx import Document
    print("[OK] python-docx is installed!")
    print("\nWord file generation is READY!")
except ImportError:
    print("[INFO] python-docx is NOT installed")
    print("\nTo enable Word file generation, run:")
    print("  pip install python-docx")
    print("\nThen re-run the batch processor.")

print("\n" + "="*80)
