# Usage Guide: Three Ways to Run upload_spdx

## Overview

The `upload_spdx` application supports **three flexible invocation methods**:

1. **Environment Variables Only** (original method)
2. **CLI Arguments Only** (new method)
3. **Mixed Mode** (CLI overrides env vars) - **Most Flexible** ✅

---

## Method 1: Environment Variables Only

**Best for**: Jenkins, Docker, CI/CD pipelines

### Local Usage
```bash
# Set environment variables
export CORONA_PAT="your_personal_access_token"
export CORONA_HOST="corona.cisco.com"
export CORONA_USERNAME="your_username.gen"
export CORONA_PRODUCT_NAME="My Product"
export CORONA_RELEASE_VERSION="1.0.0"
export CORONA_IMAGE_NAME="My Image"
export CORONA_SPDX_FILE_PATH="./spdx.json"

# Run
python -m upload_spdx
```

### Docker Usage
```bash
docker run \
  -e CORONA_PAT="your_pat" \
  -e CORONA_HOST="corona.cisco.com" \
  -e CORONA_USERNAME="user.gen" \
  -e CORONA_PRODUCT_NAME="My Product" \
  -e CORONA_RELEASE_VERSION="1.0.0" \
  -e CORONA_IMAGE_NAME="My Image" \
  -e CORONA_SPDX_FILE_PATH="/app/spdx.json" \
  -v $(pwd)/spdx.json:/app/spdx.json \
  upload_spdx:latest
```

### Jenkins Usage
```groovy
pipeline {
    environment {
        CORONA_PAT = credentials('corona-pat-id')
        CORONA_HOST = 'corona.cisco.com'
        CORONA_USERNAME = 'jenkins.gen'
        CORONA_PRODUCT_NAME = 'My Product'
        CORONA_RELEASE_VERSION = '1.0.0'
        CORONA_IMAGE_NAME = 'My Image'
    }
    
    stages {
        stage('Upload SPDX') {
            steps {
                sh 'docker run -e CORONA_PAT -e CORONA_HOST ... upload_spdx:latest'
            }
        }
    }
}
```

**Pros**:
- ✅ Original method (backward compatible)
- ✅ Works well with container orchestration
- ✅ Secure (credentials not in command history)
- ✅ Standard for CI/CD

**Cons**:
- ❌ Less flexible for quick testing
- ❌ Requires setting many env vars

---

## Method 2: CLI Arguments Only

**Best for**: Manual testing, scripting, one-off runs

### Local Usage
```bash
python -m upload_spdx \
  --pat "your_personal_access_token" \
  --host "corona.cisco.com" \
  --username "your_username.gen" \
  --product "My Product" \
  --release "1.0.0" \
  --image "My Image" \
  --spdx-file "./spdx.json"
```

### Docker Usage
```bash
docker run \
  -v $(pwd)/spdx.json:/app/spdx.json \
  upload_spdx:latest \
    --pat "your_pat" \
    --product "My Product" \
    --release "1.0.0" \
    --image "My Image" \
    --spdx-file "/app/spdx.json"
```

### Quick Test
```bash
# Minimal arguments (uses defaults)
python -m upload_spdx \
  --product "Test Product" \
  --release "1.0.0" \
  --image "Test Image"
```

**Pros**:
- ✅ Quick and flexible
- ✅ Self-documenting (visible in command)
- ✅ Easy to override specific values
- ✅ Great for testing

**Cons**:
- ❌ Credentials visible in command history
- ❌ Longer command lines
- ❌ Not ideal for automation

---

## Method 3: Mixed Mode (RECOMMENDED) ✅

**Best for**: Most scenarios - combines benefits of both methods

### Concept
```
CLI Arguments > Environment Variables > Defaults
```

**Priority Order**:
1. CLI argument (highest priority)
2. Environment variable
3. Hard-coded default (lowest priority)

### Local Usage
```bash
# Set common/sensitive values as env vars
export CORONA_PAT="your_pat"
export CORONA_HOST="corona.cisco.com"
export CORONA_USERNAME="user.gen"

# Override specific values via CLI
python -m upload_spdx \
  --product "Override Product" \
  --release "2.0.0" \
  --image "Override Image"
```

### Docker Usage
```bash
# Credentials via env vars (secure)
docker run \
  -e CORONA_PAT="your_pat" \
  -e CORONA_HOST="corona.cisco.com" \
  -v $(pwd)/spdx.json:/app/spdx.json \
  upload_spdx:latest \
    --product "CLI Override Product" \
    --release "CLI Override Version"
```

### Testing Different Products
```bash
# Set auth once
export CORONA_PAT="your_pat"
export CORONA_USERNAME="user.gen"

# Test multiple products quickly
python -m upload_spdx --product "Product A" --release "1.0"
python -m upload_spdx --product "Product B" --release "2.0"
python -m upload_spdx --product "Product C" --release "3.0"
```

**Pros**:
- ✅ **Most flexible**
- ✅ Secure (credentials in env vars)
- ✅ Quick overrides (via CLI args)
- ✅ Best of both worlds
- ✅ Great for development and production

**Cons**:
- None! This is the recommended approach.

---

## Complete CLI Arguments Reference

### View Help
```bash
python -m upload_spdx --help
```

### All Available Arguments

| Argument | Short | Description | Overrides Env Var |
|----------|-------|-------------|-------------------|
| `--pat PAT` | - | Personal Access Token | `CORONA_PAT` |
| `--host HOST` | - | Corona host | `CORONA_HOST` |
| `--username USER` | - | Corona username | `CORONA_USERNAME` |
| `--product NAME` | - | Product name | `CORONA_PRODUCT_NAME` |
| `--release VERSION` | - | Release version | `CORONA_RELEASE_VERSION` |
| `--image NAME` | - | Image name | `CORONA_IMAGE_NAME` |
| `--spdx-file PATH` | - | SPDX file path | `CORONA_SPDX_FILE_PATH` |
| `--security-contact EMAIL` | - | Security contact | `CORONA_SECURITY_CONTACT` |
| `--engineering-contact EMAIL` | - | Engineering contact | `CORONA_ENGINEERING_CONTACT` |
| `--verbose` | `-v` | Enable verbose logging | - |
| `--version` | - | Show version | - |

---

## Common Scenarios

### Scenario 1: Development Testing
```bash
# Use mixed mode
export CORONA_PAT="dev_pat"
export CORONA_HOST="corona-dev.cisco.com"

# Test different configurations quickly
python -m upload_spdx --product "Test1" --release "1.0" -v
python -m upload_spdx --product "Test2" --release "2.0" -v
```

### Scenario 2: Production Jenkins
```groovy
// Use env vars in Jenkins
environment {
    CORONA_PAT = credentials('prod-corona-pat')
    CORONA_HOST = 'corona.cisco.com'
    CORONA_USERNAME = 'jenkins-prod.gen'
}

steps {
    // Can still override via CLI if needed
    sh '''
        docker run \
          -e CORONA_PAT \
          -e CORONA_HOST \
          -e CORONA_USERNAME \
          upload_spdx:latest \
            --product "${PRODUCT_NAME}" \
            --release "${BUILD_VERSION}"
    '''
}
```

### Scenario 3: Quick Manual Upload
```bash
# All via CLI (for quick one-off)
python -m upload_spdx \
  --pat "quick_test_pat" \
  --product "Manual Test" \
  --release "1.0.0" \
  --image "Manual Image" \
  --spdx-file "./test.json" \
  --verbose
```

### Scenario 4: Batch Processing
```bash
#!/bin/bash
# Set auth once
export CORONA_PAT="batch_pat"
export CORONA_USERNAME="batch.gen"

# Process multiple SPDX files
for file in *.json; do
    product=$(basename "$file" .json)
    python -m upload_spdx \
      --product "$product" \
      --release "1.0.0" \
      --spdx-file "$file"
done
```

---

## Migration from Old to New

### Old Way (Environment Variables Only)
```bash
export CORONA_PRODUCT_NAME="Product"
export CORONA_RELEASE_VERSION="1.0.0"
python src/upload_spdx.py
```

### New Way (Same Behavior)
```bash
export CORONA_PRODUCT_NAME="Product"
export CORONA_RELEASE_VERSION="1.0.0"
python -m upload_spdx
```

### New Way (With CLI Override)
```bash
export CORONA_PRODUCT_NAME="Default Product"
python -m upload_spdx --product "Override Product"
# Uses "Override Product" (CLI wins)
```

---

## Best Practices

### ✅ DO:
- Use env vars for sensitive data (PAT, credentials)
- Use CLI args for frequently changing values (product, release)
- Use `--verbose` when debugging
- Set common values as env vars, override specific ones via CLI
- Use `--help` to verify arguments

### ❌ DON'T:
- Don't put PAT in CLI args in shared environments
- Don't mix up argument names (use `--help` to check)
- Don't hardcode credentials in scripts

---

## Troubleshooting

### Issue: "Required configuration missing"
**Solution**: Provide via env var or CLI arg:
```bash
python -m upload_spdx --pat "your_pat" --product "Product Name"
```

### Issue: "Which value is being used?"
**Solution**: Use `--verbose` to see debug info:
```bash
python -m upload_spdx --verbose --product "Test"
```

### Issue: "CLI arg not working"
**Solution**: Check argument name with `--help`:
```bash
python -m upload_spdx --help
```

---

**Recommendation**: Use **Mixed Mode (Method 3)** for the best balance of security, flexibility, and usability!

