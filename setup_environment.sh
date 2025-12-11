#!/bin/bash

###############################################################################
# setup_environment.sh
#
# Environment setup script for upload_spdx_to_corona project.
# Supports smart dependency management and testing.
#
# IMPORTANT: This script must be SOURCED, not executed!
#
# Usage:
#   source ./setup_environment.sh                 Setup and activate environment
#   source ./setup_environment.sh --test          Run tests with coverage
#   source ./setup_environment.sh --coverage      Generate coverage report
#   source ./setup_environment.sh --force-install Force reinstall dependencies
#
# Author: Ted Gauthier
# Updated: 2024-12-11
###############################################################################

# Check if script is being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "❌ ERROR: This script must be SOURCED, not executed!"
    echo ""
    echo "Run this instead:"
    echo "  source ./setup_environment.sh"
    echo ""
    echo "Or use the shorthand:"
    echo "  . ./setup_environment.sh"
    exit 1
fi

VENV_DIR="upload_spdx_py_env"
REQUIRED_MAJOR=3
REQUIRED_MINOR=12

echo "======================================================================"
echo "Upload SPDX to Corona - Environment Setup"
echo "======================================================================"

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if ! command -v "$python_cmd" &> /dev/null; then
        return 1
    fi
    
    local version=$($python_cmd --version 2>&1 | awk '{print $2}')
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)
    
    if [ "$major" -ge $REQUIRED_MAJOR ] && [ "$minor" -ge $REQUIRED_MINOR ]; then
        echo "$python_cmd:$version"
        return 0
    fi
    return 1
}

# Check if already in virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Already in virtual environment: $VIRTUAL_ENV"
    PYTHON_CMD="python"
    IN_VENV=true
else
    IN_VENV=false
    
    # Try to find suitable Python version
    echo "🔍 Detecting Python version..."
    
    PYTHON_CMD=""
    for cmd in python3.13 python3.12 python3.11 python3 python; do
        if result=$(check_python_version "$cmd"); then
            PYTHON_CMD=$(echo "$result" | cut -d: -f1)
            PYTHON_VERSION=$(echo "$result" | cut -d: -f2)
            echo "✅ Found suitable Python: $PYTHON_CMD ($PYTHON_VERSION)"
            break
        fi
    done
    
    if [ -z "$PYTHON_CMD" ]; then
        echo "❌ Error: Python ${REQUIRED_MAJOR}.${REQUIRED_MINOR}+ is required but not found."
        echo "   Current Python versions available:"
        for cmd in python3 python; do
            if command -v "$cmd" &> /dev/null; then
                echo "   - $cmd: $($cmd --version 2>&1)"
            fi
        done
        echo ""
        echo "   Please install Python ${REQUIRED_MAJOR}.${REQUIRED_MINOR} or later:"
        echo "   https://www.python.org/downloads/"
        exit 1
    fi
fi

if [ "$IN_VENV" = false ]; then
    if [ -d "$VENV_DIR" ]; then
        echo "⚠️  Virtual environment already exists at '$VENV_DIR'"
        
        # Check if it's using compatible Python version
        if [ -f "$VENV_DIR/bin/python" ]; then
            VENV_PYTHON_VERSION=$("$VENV_DIR/bin/python" --version 2>&1 | awk '{print $2}')
            VENV_MAJOR=$(echo "$VENV_PYTHON_VERSION" | cut -d. -f1)
            VENV_MINOR=$(echo "$VENV_PYTHON_VERSION" | cut -d. -f2)
            
            if [ "$VENV_MAJOR" -ge $REQUIRED_MAJOR ] && [ "$VENV_MINOR" -ge $REQUIRED_MINOR ]; then
                echo "✅ Existing venv uses Python $VENV_PYTHON_VERSION (compatible)"
                SKIP_RECREATE=true
            else
                echo "⚠️  Existing venv uses Python $VENV_PYTHON_VERSION (incompatible)"
                SKIP_RECREATE=false
            fi
        fi
        
        if [ "$SKIP_RECREATE" != true ]; then
            read -p "   Do you want to recreate it? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "🗑️  Removing existing virtual environment..."
                rm -rf "$VENV_DIR"
            else
                echo "✅ Using existing virtual environment"
            fi
        fi
    fi
    
    if [ ! -d "$VENV_DIR" ]; then
        echo "📦 Creating virtual environment with $PYTHON_CMD..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        echo "✅ Virtual environment created"
    fi
    
    echo "🔌 Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "⏭️  Skipping virtual environment creation (already active)"
fi

# Check if dependencies are already installed
DEPS_INSTALLED=false
PKG_INSTALLED=false

if python -c "import requests, pytest, pytest_cov, pytest_mock" 2>/dev/null; then
    DEPS_INSTALLED=true
fi

if python -c "import upload_spdx" 2>/dev/null; then
    PKG_INSTALLED=true
fi

if [ "$DEPS_INSTALLED" = true ] && [ "$PKG_INSTALLED" = true ] && [ "$1" != "--force-install" ]; then
    echo "✅ Dependencies and package already installed"
    echo "⏭️  Skipping installation (use --force-install to reinstall)"
    SKIP_INSTALL=true
fi

if [ "$1" = "--force-install" ]; then
    echo "🔄 Force reinstalling all dependencies and package..."
    SKIP_INSTALL=false
fi

if [ "$SKIP_INSTALL" != true ]; then
    echo "⬆️  Upgrading pip..."
    pip install --upgrade pip --quiet
    
    if [ "$DEPS_INSTALLED" = false ]; then
        echo "📥 Installing production dependencies..."
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt --quiet
        fi
        
        echo "📥 Installing development dependencies..."
        pip install pytest pytest-cov pytest-mock --quiet
    else
        echo "✅ Core dependencies already present"
    fi
    
    echo "📦 Installing package in development mode..."
    pip install -e . --quiet
    echo "✅ Package installed"
fi

echo ""
echo "======================================================================"
echo "✅ Environment setup complete!"
echo "======================================================================"
echo ""
echo "🎉 Virtual environment is now ACTIVE in your current shell!"
echo ""
echo "Available commands:"
echo "  source ./setup_environment.sh --test            Run tests with coverage"
echo "  source ./setup_environment.sh --coverage        Generate and open coverage report"
echo "  source ./setup_environment.sh --force-install   Force reinstall dependencies"
echo ""
echo "To run the application:"
echo "  python -m upload_spdx --help"
echo ""

if [ "$1" = "--test" ]; then
    echo "======================================================================"
    echo "Running Tests with Coverage"
    echo "======================================================================"
    pytest --cov=src/upload_spdx --cov-report=term-missing --cov-report=html --cov-fail-under=90 -v
    echo ""
    echo "✅ Tests completed!"
    echo "📊 HTML coverage report generated in: htmlcov/index.html"
elif [ "$1" = "--coverage" ]; then
    echo "======================================================================"
    echo "Generating Coverage Report"
    echo "======================================================================"
    pytest --cov=src/upload_spdx --cov-report=term-missing --cov-report=html -v
    echo ""
    echo "📊 HTML coverage report: htmlcov/index.html"
    echo "📊 Opening coverage report in browser..."
    if command -v open &> /dev/null; then
        open htmlcov/index.html
    elif command -v xdg-open &> /dev/null; then
        xdg-open htmlcov/index.html
    fi
fi

if [ "$IN_VENV" = false ]; then
    echo ""
    echo "To deactivate the virtual environment, run:"
    echo "  deactivate"
fi
