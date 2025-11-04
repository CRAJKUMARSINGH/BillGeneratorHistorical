#!/bin/bash

# Streamlit Cloud Deployment Fix - Automatic Installation Script
# Version: 2.0.0
# Date: 2025-10-17

set -e  # Exit on error

echo "============================================"
echo "  Streamlit Cloud Deployment Fix Installer"
echo "  Version 2.0.0"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "This script must be run from the root of your git repository"
    exit 1
fi

print_info "Detected repository: $(basename $(pwd))"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
print_info "Fix package location: $SCRIPT_DIR"
echo ""

# Confirmation
read -p "This will install the Streamlit Cloud deployment fix. Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Installation cancelled"
    exit 0
fi

echo ""
print_info "Starting installation..."
echo ""

# Step 1: Create directories if they don't exist
print_info "Step 1/7: Creating directories..."
mkdir -p .streamlit
mkdir -p app
mkdir -p core/computations
mkdir -p exports
print_success "Directories created"
echo ""

# Step 2: Copy package initialization files
print_info "Step 2/7: Installing package initialization files..."

if [ -f "$SCRIPT_DIR/__init__.py" ]; then
    cp "$SCRIPT_DIR/__init__.py" ./
    print_success "Copied root __init__.py"
else
    print_warning "Root __init__.py not found in package, creating minimal version..."
    cat > __init__.py << 'EOF'
import os, sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path: sys.path.insert(0, ROOT_DIR)
__version__ = "2.0.0"
__all__ = ['core', 'exports', 'app']
EOF
    print_success "Created root __init__.py"
fi

if [ -f "$SCRIPT_DIR/app/__init__.py" ]; then
    cp "$SCRIPT_DIR/app/__init__.py" ./app/
    print_success "Copied app/__init__.py"
else
    print_warning "app/__init__.py not found, creating..."
    cat > app/__init__.py << 'EOF'
import os, sys
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
if ROOT_DIR not in sys.path: sys.path.insert(0, ROOT_DIR)
if APP_DIR not in sys.path: sys.path.insert(0, APP_DIR)
__all__ = ['main']
EOF
    print_success "Created app/__init__.py"
fi

if [ -f "$SCRIPT_DIR/core/__init__.py" ]; then
    cp "$SCRIPT_DIR/core/__init__.py" ./core/
    print_success "Copied core/__init__.py"
fi

if [ -f "$SCRIPT_DIR/core/computations/__init__.py" ]; then
    cp "$SCRIPT_DIR/core/computations/__init__.py" ./core/computations/
    print_success "Copied core/computations/__init__.py"
fi

if [ -f "$SCRIPT_DIR/exports/__init__.py" ]; then
    cp "$SCRIPT_DIR/exports/__init__.py" ./exports/
    print_success "Copied exports/__init__.py"
fi

echo ""

# Step 3: Copy configuration files
print_info "Step 3/7: Installing configuration files..."

if [ -f "$SCRIPT_DIR/.streamlit/config.toml" ]; then
    cp "$SCRIPT_DIR/.streamlit/config.toml" ./.streamlit/
    print_success "Copied .streamlit/config.toml"
fi

if [ -f "$SCRIPT_DIR/requirements_streamlit_cloud.txt" ]; then
    cp "$SCRIPT_DIR/requirements_streamlit_cloud.txt" ./
    print_success "Copied requirements_streamlit_cloud.txt"
fi

if [ -f "$SCRIPT_DIR/packages.txt" ]; then
    cp "$SCRIPT_DIR/packages.txt" ./
    print_success "Copied packages.txt"
fi

echo ""

# Step 4: Copy main application file
print_info "Step 4/7: Installing fixed main application..."

if [ -f "app/main.py" ]; then
    print_warning "app/main.py exists. Creating backup..."
    cp app/main.py app/main.py.backup.$(date +%Y%m%d_%H%M%S)
    print_success "Backup created"
fi

if [ -f "$SCRIPT_DIR/app/main.py" ]; then
    cp "$SCRIPT_DIR/app/main.py" ./app/
    print_success "Copied fixed app/main.py"
fi

echo ""

# Step 5: Copy documentation
print_info "Step 5/7: Installing documentation..."

DOC_FILES=(
    "STREAMLIT_DEPLOYMENT_FIX_COMPLETE.md"
    "DEPLOYMENT_CHECKLIST.md"
    "DEPLOYMENT_FIX_SUMMARY.md"
    "QUICK_START.md"
)

for doc in "${DOC_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$doc" ]; then
        cp "$SCRIPT_DIR/$doc" ./
        print_success "Copied $doc"
    fi
done

echo ""

# Step 6: Verify installation
print_info "Step 6/7: Verifying installation..."

REQUIRED_FILES=(
    "__init__.py"
    "app/__init__.py"
    "core/__init__.py"
    "core/computations/__init__.py"
    "exports/__init__.py"
    ".streamlit/config.toml"
    "requirements_streamlit_cloud.txt"
    "app/main.py"
)

all_present=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file exists"
    else
        print_error "$file missing"
        all_present=false
    fi
done

echo ""

if [ "$all_present" = false ]; then
    print_error "Some required files are missing!"
    print_warning "Please check the installation and try again"
    exit 1
fi

print_success "All required files are present"
echo ""

# Step 7: Git operations
print_info "Step 7/7: Preparing git commit..."

git add __init__.py app/__init__.py core/__init__.py core/computations/__init__.py exports/__init__.py
git add .streamlit/config.toml
git add requirements_streamlit_cloud.txt packages.txt
git add app/main.py
git add *.md 2>/dev/null || true

echo ""
print_success "Files staged for commit"
echo ""

# Show status
print_info "Git status:"
git status --short
echo ""

# Ask if user wants to commit
read -p "Commit these changes? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Fix: Streamlit Cloud deployment import errors

- Added package initialization files for proper imports
- Implemented 4-tier fallback import strategy
- Created Streamlit Cloud optimized configuration
- Added comprehensive error handling
- Enhanced UI with progress tracking
- Added deployment documentation

Fixes: ModuleNotFoundError in Streamlit Cloud deployment"
    
    print_success "Changes committed"
    echo ""
    
    read -p "Push to remote repository? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push
        print_success "Changes pushed to remote"
    fi
fi

echo ""
echo "============================================"
echo "  Installation Complete! ✅"
echo "============================================"
echo ""
print_success "Streamlit Cloud deployment fix has been installed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Review the changes with: git diff HEAD~1"
echo "  2. Test locally with: streamlit run app/main.py"
echo "  3. Deploy to Streamlit Cloud:"
echo "     - Go to https://share.streamlit.io/"
echo "     - Set main file: app/main.py"
echo "     - Set requirements: requirements_streamlit_cloud.txt"
echo "     - Click Deploy"
echo ""
print_info "Documentation:"
echo "  - Quick Start: QUICK_START.md"
echo "  - Complete Guide: STREAMLIT_DEPLOYMENT_FIX_COMPLETE.md"
echo "  - Checklist: DEPLOYMENT_CHECKLIST.md"
echo "  - Summary: DEPLOYMENT_FIX_SUMMARY.md"
echo ""
print_success "Your app is ready for Streamlit Cloud deployment! 🚀"
echo ""