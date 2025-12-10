#!/bin/bash

###############################################################################
# setup_environment.sh
#
# This script sets up the complete environment for the upload_spdx_to_corona 
# project including:
# - Python virtual environment creation
# - Installation of all required packages (requests, pytest)
# - Docker daemon verification and startup
# - Docker image build
# - Optional Docker container run
#
# Author: Generated for Ted Gauthier
# Date: 2024-12-10
###############################################################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
VENV_NAME="upload_spdx_py_env"
PYTHON_CMD="python3"
DOCKER_IMAGE_NAME="upload_spdx"
DOCKER_TAG="latest"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Upload SPDX to Corona - Setup Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

###############################################################################
# 1. Python Virtual Environment Setup
###############################################################################
echo -e "${GREEN}[1/5] Setting up Python virtual environment...${NC}"

# Check if Python 3 is available
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "  ${BLUE}✓${NC} Found: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo -e "  Creating virtual environment: $VENV_NAME"
    $PYTHON_CMD -m venv $VENV_NAME
    echo -e "  ${GREEN}✓${NC} Virtual environment created"
else
    echo -e "  ${YELLOW}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo -e "  Activating virtual environment..."
source $VENV_NAME/bin/activate

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}Error: Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Virtual environment activated: $VIRTUAL_ENV"

###############################################################################
# 2. Upgrade pip
###############################################################################
echo ""
echo -e "${GREEN}[2/5] Upgrading pip...${NC}"
pip install --upgrade pip --quiet
PIP_VERSION=$(pip --version)
echo -e "  ${GREEN}✓${NC} $PIP_VERSION"

###############################################################################
# 3. Install Required Packages
###############################################################################
echo ""
echo -e "${GREEN}[3/5] Installing required Python packages...${NC}"

# Install from requirements.txt
if [ -f "requirements.txt" ]; then
    echo -e "  Installing packages from requirements.txt..."
    pip install -r requirements.txt --quiet
    echo -e "  ${GREEN}✓${NC} Installed: requests"
else
    echo -e "  ${YELLOW}Warning: requirements.txt not found${NC}"
    echo -e "  Installing requests manually..."
    pip install requests --quiet
    echo -e "  ${GREEN}✓${NC} Installed: requests"
fi

# Install pytest and testing dependencies
echo -e "  Installing testing packages..."
pip install pytest pytest-cov pytest-mock --quiet
echo -e "  ${GREEN}✓${NC} Installed: pytest, pytest-cov, pytest-mock"

# Display installed packages
echo ""
echo -e "  ${BLUE}Installed Python packages:${NC}"
pip list | grep -E "(requests|pytest)" | sed 's/^/    /'

###############################################################################
# 4. Docker Setup and Verification
###############################################################################
echo ""
echo -e "${GREEN}[4/5] Checking Docker...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo -e "${YELLOW}Please install Docker Desktop for Mac from: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo -e "  ${BLUE}✓${NC} Found: $DOCKER_VERSION"

# Check if Docker daemon is running
echo -e "  Checking Docker daemon status..."
if ! docker info &> /dev/null; then
    echo -e "  ${YELLOW}Docker daemon is not running. Attempting to start...${NC}"
    
    # Try to start Docker Desktop on macOS
    if [ "$(uname)" == "Darwin" ]; then
        echo -e "  Starting Docker Desktop..."
        open -a Docker
        
        # Wait for Docker to start (max 60 seconds)
        echo -e "  Waiting for Docker daemon to start (this may take up to 60 seconds)..."
        counter=0
        while ! docker info &> /dev/null && [ $counter -lt 60 ]; do
            sleep 2
            counter=$((counter + 2))
            printf "."
        done
        echo ""
        
        if docker info &> /dev/null; then
            echo -e "  ${GREEN}✓${NC} Docker daemon started successfully"
        else
            echo -e "${RED}Error: Failed to start Docker daemon${NC}"
            echo -e "${YELLOW}Please start Docker Desktop manually and run this script again${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Error: Docker daemon is not running${NC}"
        echo -e "${YELLOW}Please start Docker manually and run this script again${NC}"
        exit 1
    fi
else
    echo -e "  ${GREEN}✓${NC} Docker daemon is running"
fi

###############################################################################
# 5. Build Docker Image
###############################################################################
echo ""
echo -e "${GREEN}[5/5] Building Docker image...${NC}"

if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}Error: Dockerfile not found in current directory${NC}"
    exit 1
fi

echo -e "  Building image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
echo -e "  ${YELLOW}This may take a few minutes...${NC}"

if docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} . ; then
    echo -e "  ${GREEN}✓${NC} Docker image built successfully"
    
    # Display image info
    echo ""
    echo -e "  ${BLUE}Docker image details:${NC}"
    docker images ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} | sed 's/^/    /'
else
    echo -e "${RED}Error: Failed to build Docker image${NC}"
    exit 1
fi

###############################################################################
# Setup Complete
###############################################################################
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  • Virtual environment: ${GREEN}$VENV_NAME${NC}"
echo -e "  • Python packages: ${GREEN}requests, pytest, pytest-cov, pytest-mock${NC}"
echo -e "  • Docker image: ${GREEN}${DOCKER_IMAGE_NAME}:${DOCKER_TAG}${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Activate virtual environment:"
echo -e "     ${YELLOW}source $VENV_NAME/bin/activate${NC}"
echo ""
echo -e "  2. Run tests:"
echo -e "     ${YELLOW}pytest test/test_upload_spdx.py -v${NC}"
echo ""
echo -e "  3. Run application locally:"
echo -e "     ${YELLOW}python src/upload_spdx.py${NC}"
echo ""
echo -e "  4. Run application in Docker container:"
echo -e "     ${YELLOW}docker run -e CORONA_PAT=\$CORONA_PAT \\${NC}"
echo -e "     ${YELLOW}              -e CORONA_HOST=\$CORONA_HOST \\${NC}"
echo -e "     ${YELLOW}              -e CORONA_USERNAME=\$CORONA_USERNAME \\${NC}"
echo -e "     ${YELLOW}              ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}${NC}"
echo ""

# Ask user if they want to run tests now
read -p "Would you like to run the PyTest test suite now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}Running PyTest test suite...${NC}"
    echo -e "${BLUE}========================================${NC}"
    pytest test/test_upload_spdx.py -v
    echo ""
fi

# Ask user if they want to run the Docker container now
read -p "Would you like to run the Docker container now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check for required environment variables
    if [ -z "$CORONA_PAT" ] || [ -z "$CORONA_HOST" ] || [ -z "$CORONA_USERNAME" ]; then
        echo ""
        echo -e "${YELLOW}Warning: Required environment variables are not set${NC}"
        echo -e "The following environment variables should be set:"
        echo -e "  - CORONA_PAT"
        echo -e "  - CORONA_HOST"
        echo -e "  - CORONA_USERNAME"
        echo -e "  - CORONA_PRODUCT_NAME (optional, has default)"
        echo -e "  - CORONA_RELEASE_VERSION (optional, has default)"
        echo -e "  - CORONA_IMAGE_NAME (optional, has default)"
        echo ""
        read -p "Continue with default values from CoronaConfig? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Skipping Docker run. You can run it manually later.${NC}"
            exit 0
        fi
    fi
    
    echo ""
    echo -e "${BLUE}Running Docker container...${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # Build docker run command with environment variables if they exist
    DOCKER_RUN_CMD="docker run"
    
    [ ! -z "$CORONA_PAT" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_PAT=$CORONA_PAT"
    [ ! -z "$CORONA_HOST" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_HOST=$CORONA_HOST"
    [ ! -z "$CORONA_USERNAME" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_USERNAME=$CORONA_USERNAME"
    [ ! -z "$CORONA_ENGINEERING_CONTACT" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_ENGINEERING_CONTACT=$CORONA_ENGINEERING_CONTACT"
    [ ! -z "$CORONA_SECURITY_CONTACT" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_SECURITY_CONTACT=$CORONA_SECURITY_CONTACT"
    [ ! -z "$CORONA_PRODUCT_NAME" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_PRODUCT_NAME=$CORONA_PRODUCT_NAME"
    [ ! -z "$CORONA_RELEASE_VERSION" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_RELEASE_VERSION=$CORONA_RELEASE_VERSION"
    [ ! -z "$CORONA_IMAGE_NAME" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_IMAGE_NAME=$CORONA_IMAGE_NAME"
    [ ! -z "$CORONA_SPDX_FILE_PATH" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e CORONA_SPDX_FILE_PATH=$CORONA_SPDX_FILE_PATH"
    
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
    
    echo -e "Executing: ${YELLOW}$DOCKER_RUN_CMD${NC}"
    echo ""
    eval $DOCKER_RUN_CMD
    echo ""
fi

echo -e "${GREEN}All done!${NC}"
