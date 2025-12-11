# Upload SPDX to Corona

A Python application for uploading SPDX (Software Package Data Exchange) documents to Cisco's Corona platform using the Corona REST API. This tool automates the process of creating products, releases, and images in Corona and attaching SPDX SBOM (Software Bill of Materials) files to them.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Development](#development)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## Overview

The `upload_spdx.py` module provides a robust interface to Corona's REST API for managing software supply chain security through SPDX document uploads. It handles:

- **Authentication**: PAT (Personal Access Token) based authentication with Corona
- **Product Management**: Create or retrieve Corona products
- **Release Management**: Create or retrieve product releases
- **Image Management**: Create or retrieve release images
- **SPDX Upload**: Upload and attach SPDX documents to images

## Features

- ✅ **Automated Setup**: One-command environment setup with `setup_environment.sh`
- ✅ **Comprehensive Testing**: 29 unit tests with pytest and mocking
- ✅ **High Code Coverage**: ≥90% code coverage enforced in CI/CD
- ✅ **Docker Support**: Containerized deployment with automated builds
- ✅ **GitHub Actions CI/CD**: Full automation with linting, testing, security scanning
- ✅ **Error Handling**: Robust error handling with retry logic for transient failures
- ✅ **Configuration**: Environment variable based configuration with sensible defaults
- ✅ **Logging**: Detailed logging for debugging and monitoring

## Prerequisites

- **Python**: 3.9 or higher
- **Docker**: Docker Desktop (for containerized deployment)
- **Corona Access**: Valid Corona PAT (Personal Access Token)
- **macOS/Linux**: Tested on macOS, should work on Linux

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd /Users/tedg/workspace/upload_spdx_to_corona

# Run the automated setup script
./setup_environment.sh
```

The setup script will:
- Create a Python virtual environment
- Install all required dependencies (requests, pytest, pytest-cov, pytest-mock)
- Check and start Docker if needed
- Build the Docker image
- Optionally run tests

### 2. Configure Environment

Set the required environment variables:

```bash
export CORONA_PAT="your_personal_access_token"
export CORONA_HOST="corona.cisco.com"
export CORONA_USERNAME="your_username.gen"
export CORONA_PRODUCT_NAME="Your Product Name"
export CORONA_RELEASE_VERSION="1.0.0"
export CORONA_IMAGE_NAME="Your Image Name"
export CORONA_SPDX_FILE_PATH="./bes-traceability-spdx.json"
```

### 3. Run the Application

**Local Execution (Environment Variables):**
```bash
source upload_spdx_py_env/bin/activate
python -m upload_spdx
```

**Local Execution (CLI Arguments):**
```bash
python -m upload_spdx \
  --pat "your_pat" \
  --product "Product Name" \
  --release "1.0.0" \
  --image "Image Name" \
  --spdx-file "./spdx.json"
```

**Docker (Environment Variables):**
```bash
docker run -e CORONA_PAT=$CORONA_PAT \
           -e CORONA_HOST=$CORONA_HOST \
           -e CORONA_USERNAME=$CORONA_USERNAME \
           upload_spdx:latest
```

**Docker (CLI Arguments):**
```bash
docker run upload_spdx:latest \
  --product "Product Name" \
  --release "1.0.0" \
  --image "Image Name"
```

**Mixed (CLI overrides env vars):**
```bash
# Env vars provide defaults, CLI args override
export CORONA_PAT="your_pat"
export CORONA_HOST="corona.cisco.com"
python -m upload_spdx --product "Override Product Name"
```

## Project Structure

```
upload_spdx_to_corona/
├── src/                            # Source code
│   └── upload_spdx.py             # Main application module
├── test/                           # Test files
│   └── test_upload_spdx.py        # Comprehensive unit tests (29 tests)
├── docs/                           # Documentation
│   ├── README.md                  # Documentation index
│   ├── CLEANUP_VERIFICATION.md    # Cleanup verification report
│   └── RESTRUCTURE_SUMMARY.md     # Project restructuring details
├── Dockerfile                      # Docker container definition
├── Jenkinsfile                     # CI/CD pipeline configuration
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── setup_environment.sh            # Automated environment setup
├── bes-traceability-spdx.json     # Sample SPDX document
└── README.md                       # This file
```

## Configuration

### CLI Arguments

The application supports command-line arguments that **override** environment variables:

```bash
python -m upload_spdx --help
```

**Available Arguments:**

| Argument | Description | Overrides |
|----------|-------------|-----------|
| `--pat PAT` | Corona Personal Access Token | `CORONA_PAT` |
| `--host HOST` | Corona host domain | `CORONA_HOST` |
| `--username USER` | Corona username | `CORONA_USERNAME` |
| `--product NAME` | Product name | `CORONA_PRODUCT_NAME` |
| `--release VERSION` | Release version | `CORONA_RELEASE_VERSION` |
| `--image NAME` | Image name | `CORONA_IMAGE_NAME` |
| `--spdx-file PATH` | Path to SPDX file | `CORONA_SPDX_FILE_PATH` |
| `--security-contact EMAIL` | Security contact | `CORONA_SECURITY_CONTACT` |
| `--engineering-contact EMAIL` | Engineering contact | `CORONA_ENGINEERING_CONTACT` |
| `-v, --verbose` | Enable verbose logging | - |
| `--version` | Show version | - |

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CORONA_PAT` | Personal Access Token for Corona authentication | (hardcoded fallback) | Yes |
| `CORONA_HOST` | Corona host domain | `corona.cisco.com` | No |
| `CORONA_USERNAME` | Corona username (typically ends in .gen) | `tedgcisco.gen` | No |
| `CORONA_ENGINEERING_CONTACT` | Engineering contact email/mailer | `upload_spdx_mailer` | No |
| `CORONA_SECURITY_CONTACT` | Security contact email/mailer | `upload_spdx_mailer` | No |
| `CORONA_PRODUCT_NAME` | Target product name in Corona | `tedg test 2024-11-20` | No |
| `CORONA_RELEASE_VERSION` | Target release version | `1.0.20` | No |
| `CORONA_IMAGE_NAME` | Target image name | `test imageViaApi.20` | No |
| `CORONA_SPDX_FILE_PATH` | Path to SPDX document file | `./bes-traceability-spdx.json` | No |

### Configuration Class

The `CoronaConfig` class in `src/upload_spdx.py` manages all configuration:

```python
class CoronaConfig:
    @staticmethod
    def get_corona_pat():
        return os.getenv('CORONA_PAT', 'default_pat')
    
    @staticmethod
    def get_host():
        return os.getenv('CORONA_HOST', 'corona.cisco.com')
    # ... more configuration methods
```

## Usage

### Command Line (Local)

```bash
# Activate virtual environment
source upload_spdx_py_env/bin/activate

# Run with environment variables
python src/upload_spdx.py
```

### Python API

```python
from upload_spdx import (
    ProductManager,
    ReleaseManager,
    ImageManager,
    SpdxManager,
    CoronaConfig
)

# Initialize managers
host = CoronaConfig.get_host()
username = CoronaConfig.get_user_name()

product_manager = ProductManager(host, username)
release_manager = ReleaseManager(host, username)
image_manager = ImageManager(host, username)
spdx_manager = SpdxManager(host, username)

# Get or create resources
product_id = product_manager.get_or_create_product("My Product")
release_id = release_manager.get_or_create_release(product_id, "1.0.0")
image_id = image_manager.get_or_create_image(product_id, release_id, "My Image")

# Upload SPDX
spdx_manager.update_or_add_spdx(image_id, "/path/to/spdx.json")
```

## Docker Deployment

### Build Image

```bash
docker build -t upload_spdx:latest .
```

### Run Container

```bash
docker run \
  -e CORONA_PAT="your_pat" \
  -e CORONA_HOST="corona.cisco.com" \
  -e CORONA_USERNAME="your_username.gen" \
  -e CORONA_PRODUCT_NAME="Product Name" \
  -e CORONA_RELEASE_VERSION="1.0.0" \
  -e CORONA_IMAGE_NAME="Image Name" \
  upload_spdx:latest
```

### Push to Registry

```bash
# Tag for registry
docker tag upload_spdx:latest containers.cisco.com/your_namespace/upload_spdx:latest

# Push to registry
docker push containers.cisco.com/your_namespace/upload_spdx:latest
```

## Testing

### Run All Tests

```bash
# Activate virtual environment
source upload_spdx_py_env/bin/activate

# Run tests with verbose output
pytest test/test_upload_spdx.py -v
```

### Run Specific Test Classes

```bash
# Test ProductManager
pytest test/test_upload_spdx.py::TestProductManager -v

# Test ReleaseManager
pytest test/test_upload_spdx.py::TestReleaseManager -v

# Test ImageManager
pytest test/test_upload_spdx.py::TestImageManager -v

# Test SpdxManager
pytest test/test_upload_spdx.py::TestSpdxManager -v
```

### Test Coverage

**Coverage Requirement**: ≥90%

The project enforces a minimum code coverage of 90% in CI/CD pipelines.

```bash
# Run tests with coverage report
pytest test/test_upload_spdx.py --cov=src --cov-report=html --cov-report=term

# View coverage in browser
open htmlcov/index.html

# Check if coverage meets 90% requirement
pytest test/test_upload_spdx.py --cov=src --cov-fail-under=90
```

**Coverage Features**:
- ✅ Enforced in CI/CD (fails if below 90%)
- ✅ Coverage reports posted on PRs automatically
- ✅ HTML reports uploaded as artifacts
- ✅ Codecov integration for tracking trends

### Test Summary

The test suite includes **29 comprehensive tests**:
- API client authentication and request handling
- Product creation and retrieval
- Release creation and retrieval
- Image creation and retrieval
- SPDX upload functionality
- Error handling and retries
- Network failure scenarios

## Development

### Setup Development Environment

```bash
# Run the setup script
./setup_environment.sh

# Activate virtual environment
source upload_spdx_py_env/bin/activate

# Install additional dev dependencies if needed
pip install pytest-cov pytest-mock black pylint
```

### Code Style

The project follows Python best practices:
- PEP 8 style guidelines
- Type hints where applicable
- Docstrings for all classes and methods
- Single-line logger messages for clarity

### VS Code Configuration

For VS Code Python debugging and testing, configure `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Upload SPDX",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/upload_spdx.py",
            "console": "integratedTerminal",
            "env": {
                "CORONA_PAT": "${env:CORONA_PAT}",
                "CORONA_PRODUCT_NAME": "Test Product",
                "CORONA_RELEASE_VERSION": "1.0.0",
                "CORONA_IMAGE_NAME": "Test Image"
            }
        }
    ]
}
```

And `.vscode/settings.json`:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "-v",
        "--cov=src/",
        "--cov-report=xml",
        "test/"
    ]
}
```

## Documentation

Additional documentation is available in the `docs/` directory:

- **[RESTRUCTURE_SUMMARY.md](docs/RESTRUCTURE_SUMMARY.md)**: Details about the project structure and recent reorganization

## Troubleshooting

### Docker Not Starting

```bash
# On macOS, start Docker Desktop manually
open -a Docker

# Wait for Docker daemon to start
docker info
```

### Module Import Errors

```bash
# Ensure virtual environment is activated
source upload_spdx_py_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Authentication Failures

- Verify your `CORONA_PAT` is valid and not expired
- Check that your username ends with `.gen`
- Ensure you have proper permissions in Corona

### SPDX Upload Failures

- Verify the SPDX file exists at the specified path
- Ensure the SPDX file is valid JSON format
- Check that `ignore_validation` is set appropriately

### Test Failures

```bash
# Run tests with more verbose output
pytest test/test_upload_spdx.py -vv

# Run a specific failing test
pytest test/test_upload_spdx.py::TestClassName::test_method_name -vv
```

## Architecture

### Class Structure

```
CoronaAPIClient (Base Class)
├── get_auth_token()
├── make_authenticated_request()
└── _handle_error()

ProductManager (extends CoronaAPIClient)
├── get_or_create_product()
└── _create_product()

ReleaseManager (extends CoronaAPIClient)
├── get_or_create_release()
└── _create_release()

ImageManager (extends CoronaAPIClient)
├── get_or_create_image()
└── _create_image()

SpdxManager (extends CoronaAPIClient)
└── update_or_add_spdx()
```

### Error Handling

The application includes:
- Automatic retry logic for transient failures (429, 500, 502, 503, 504)
- Exponential backoff for retries
- Comprehensive error messages
- Proper exception handling with custom `CoronaError` class

### Logging

Logging is configured at the INFO level by default:
- All API interactions are logged
- Product/Release/Image creation events logged
- Error conditions logged at FATAL level

## CI/CD Integration

The project includes a `Jenkinsfile` for automated CI/CD:

1. **Checkout**: Pulls code from SCM
2. **Setup**: Installs dependencies
3. **Build**: Builds Docker image
4. **Push**: Pushes to container registry
5. **Deploy**: Runs the container

## Author

**Ted Gauthier**
- Email: tedg@cisco.com
- Version: 1.0.0

## License

Cisco Internal Use

---

For more information or support, please contact the author or refer to the documentation in the `docs/` directory.
