# Running upload_spdx in GitHub Actions

## Overview

This guide covers best practices for running `upload_spdx_to_corona` within GitHub Actions workflows, including three different approaches with varying levels of complexity and reusability.

---

## Quick Start: Use the Reusable Action

The simplest way to use this tool in your workflows:

```yaml
name: Upload SPDX

on:
  push:
    branches: [main]

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Upload SPDX to Corona
        uses: tedg-dev/upload_spdx_to_corona/.github/actions/upload-spdx@main
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.ref_name }}
          image-name: ci-build-${{ github.run_number }}
          spdx-file-path: ./spdx.json
```

---

## Three Implementation Approaches

### Option 1: Docker-Based Workflow (Recommended) ✅

**Best for**: Consistency with local development, portability

```yaml
name: Upload SPDX to Corona

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  upload-spdx:
    name: Upload SPDX to Corona
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t upload_spdx:latest .
      
      - name: Upload SPDX
        run: |
          docker run \
            -e CORONA_PAT="${{ secrets.CORONA_PAT }}" \
            -e CORONA_HOST="${{ secrets.CORONA_HOST }}" \
            -e CORONA_USERNAME="${{ secrets.CORONA_USERNAME }}" \
            -v ${{ github.workspace }}/spdx.json:/app/spdx.json \
            upload_spdx:latest \
              --product "${{ github.event.repository.name }}" \
              --release "${{ github.ref_name }}" \
              --image "ci-build-${{ github.run_number }}" \
              --spdx-file /app/spdx.json
```

**Pros:**
- ✅ Consistent environment (same as local development)
- ✅ Uses existing Dockerfile
- ✅ Secrets handled securely via environment variables
- ✅ Flexible CLI argument overrides
- ✅ Works in any CI/CD platform (not GitHub-specific)
- ✅ Isolated dependencies

**Cons:**
- ⚠️ Slower startup (Docker build time)
- ⚠️ Requires Docker layer caching for optimal performance

**When to Use:**
- You want consistency between local and CI environments
- You already use Docker for local development
- You need to run in multiple CI/CD platforms
- You have complex dependencies

---

### Option 2: Direct Python Execution (Fastest) ⚡

**Best for**: Speed, simplicity, Python-native workflows

```yaml
name: Upload SPDX to Corona

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  upload-spdx:
    name: Upload SPDX to Corona
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Upload SPDX
        env:
          CORONA_PAT: ${{ secrets.CORONA_PAT }}
          CORONA_HOST: ${{ secrets.CORONA_HOST }}
          CORONA_USERNAME: ${{ secrets.CORONA_USERNAME }}
        run: |
          python -m upload_spdx \
            --product "${{ github.event.repository.name }}" \
            --release "${{ github.ref_name }}" \
            --image "ci-build-${{ github.run_number }}" \
            --spdx-file ./spdx.json \
            --verbose
```

**Pros:**
- ✅ Faster execution (no Docker build)
- ✅ Uses GitHub's pip cache for dependencies
- ✅ Simpler configuration
- ✅ Native Python workflow
- ✅ Better for Python-only projects

**Cons:**
- ⚠️ Environment differs from local Docker
- ⚠️ Dependency management must be careful
- ⚠️ Less portable to other CI/CD systems

**When to Use:**
- Speed is critical
- You don't use Docker locally
- Simple Python-only dependencies
- GitHub Actions only (no multi-platform CI)

---

### Option 3: Reusable Composite Action (Most Professional) 🎯

**Best for**: Multiple workflows, team collaboration, marketplace publishing

The reusable action is located at `.github/actions/upload-spdx/action.yml`.

**Usage in Workflows:**

```yaml
name: Build and Upload SPDX

on:
  release:
    types: [published]

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Generate SPDX
        run: |
          # Your SPDX generation logic here
          ./scripts/generate-spdx.sh > spdx.json
      
      - name: Upload to Corona
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.ref_name }}
          image-name: ${{ github.event.repository.name }}-${{ github.sha }}
          spdx-file-path: ./spdx.json
          corona-host: corona.cisco.com
          corona-username: ${{ secrets.CORONA_USERNAME }}
```

**Pros:**
- ✅ Clean, reusable interface
- ✅ Consistent usage across workflows
- ✅ Can be shared across repositories
- ✅ Professional, maintainable
- ✅ Can be published to GitHub Marketplace
- ✅ Encapsulates complexity
- ✅ Versioned and documented

**Cons:**
- ⚠️ Requires initial setup
- ⚠️ More files to maintain

**When to Use:**
- You have multiple workflows that upload SPDX
- You want to share across multiple repositories
- You want professional, maintainable code
- You might publish to GitHub Marketplace

---

## Best Practices

### 1. Security 🔒

#### ✅ DO: Use GitHub Secrets
```yaml
env:
  CORONA_PAT: ${{ secrets.CORONA_PAT }}
  CORONA_HOST: ${{ secrets.CORONA_HOST }}
  CORONA_USERNAME: ${{ secrets.CORONA_USERNAME }}
```

#### ❌ DON'T: Hardcode Credentials
```yaml
env:
  CORONA_PAT: "corona_eyJhbGc..."  # NEVER DO THIS
```

#### Setting Up Secrets
1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Click: `New repository secret`
3. Add secrets:
   - `CORONA_PAT` - Your Personal Access Token
   - `CORONA_HOST` - Corona host (optional, has default)
   - `CORONA_USERNAME` - Your Corona username

---

### 2. Dynamic Values 🎯

Use GitHub context variables for dynamic configuration:

```yaml
# Repository name as product
--product "${{ github.event.repository.name }}"

# Branch or tag name as release version
--release "${{ github.ref_name }}"

# Build number as image identifier
--image "ci-build-${{ github.run_number }}"

# Commit SHA for traceability
--image "${{ github.event.repository.name }}-${{ github.sha }}"

# Release tag for production
--release "${{ github.event.release.tag_name }}"
```

**Useful GitHub Context Variables:**
- `${{ github.event.repository.name }}` - Repository name
- `${{ github.ref_name }}` - Branch or tag name
- `${{ github.sha }}` - Commit SHA (short: `${{ github.sha }}` first 7 chars)
- `${{ github.run_number }}` - Workflow run number
- `${{ github.run_id }}` - Unique workflow run ID
- `${{ github.actor }}` - User who triggered workflow
- `${{ github.event.release.tag_name }}` - Release tag (on release events)

---

### 3. Error Handling ⚠️

#### Fail Workflow on Upload Failure
```yaml
- name: Upload SPDX
  id: upload
  continue-on-error: false  # Default: fail workflow if step fails
  run: python -m upload_spdx ...
```

#### Handle Failures Gracefully
```yaml
- name: Upload SPDX
  id: upload
  continue-on-error: true
  run: python -m upload_spdx ...

- name: Handle upload failure
  if: failure() && steps.upload.outcome == 'failure'
  run: |
    echo "::error::SPDX upload failed"
    echo "::notice::Continuing workflow despite upload failure"
    # Optionally notify team, create issue, etc.
```

#### Retry on Failure
```yaml
- name: Upload SPDX with retries
  uses: nick-fields/retry-action@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_wait_seconds: 30
    command: |
      python -m upload_spdx \
        --product "${{ github.event.repository.name }}" \
        --release "${{ github.ref_name }}"
```

---

### 4. Performance Optimization ⚡

#### Cache Docker Layers
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build Docker image with cache
  uses: docker/build-push-action@v5
  with:
    context: .
    tags: upload_spdx:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
    load: true

- name: Run upload
  run: docker run upload_spdx:latest ...
```

#### Cache Python Dependencies
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.9'
    cache: 'pip'  # Automatically caches pip dependencies
```

#### Use GitHub Container Registry
```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/${{ github.repository }}/upload-spdx:latest
    cache-from: type=registry,ref=ghcr.io/${{ github.repository }}/upload-spdx:cache
    cache-to: type=registry,ref=ghcr.io/${{ github.repository }}/upload-spdx:cache,mode=max

- name: Run from registry
  run: |
    docker run ghcr.io/${{ github.repository }}/upload-spdx:latest ...
```

---

### 5. Conditional Execution 🔀

#### Only on Main Branch
```yaml
jobs:
  upload:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Upload SPDX
        run: ...
```

#### Only on Release
```yaml
on:
  release:
    types: [published]

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - name: Upload SPDX for release
        run: |
          python -m upload_spdx \
            --release "${{ github.event.release.tag_name }}"
```

#### Skip for Dependabot
```yaml
jobs:
  upload:
    runs-on: ubuntu-latest
    if: github.actor != 'dependabot[bot]'
    steps:
      - name: Upload SPDX
        run: ...
```

---

### 6. Logging and Debugging 📝

#### Enable Verbose Mode
```yaml
- name: Upload SPDX with verbose logging
  run: |
    python -m upload_spdx \
      --verbose \
      --product "Test Product"
```

#### Capture Output
```yaml
- name: Upload SPDX
  id: upload
  run: |
    OUTPUT=$(python -m upload_spdx ... 2>&1)
    echo "$OUTPUT"
    echo "output=$OUTPUT" >> $GITHUB_OUTPUT

- name: Use output
  run: |
    echo "Upload result: ${{ steps.upload.outputs.output }}"
```

#### Debug Mode
```yaml
# Enable debug logging for entire workflow
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

---

## Complete Example Workflows

### Example 1: Simple Production Upload

```yaml
name: Upload SPDX on Release

on:
  release:
    types: [published]

jobs:
  upload-spdx:
    name: Upload SPDX to Corona
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Download release SPDX
        uses: actions/download-artifact@v4
        with:
          name: spdx-document
          path: .
      
      - name: Upload to Corona
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.event.release.tag_name }}
          image-name: ${{ github.event.repository.name }}-${{ github.event.release.tag_name }}
          spdx-file-path: ./spdx.json
```

### Example 2: Multi-Environment Upload

```yaml
name: Upload SPDX Multi-Environment

on:
  push:
    branches: [develop, staging, main]

jobs:
  upload-spdx:
    name: Upload SPDX to ${{ matrix.environment }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - branch: develop
            environment: development
            host: corona-dev.cisco.com
          - branch: staging
            environment: staging
            host: corona-stage.cisco.com
          - branch: main
            environment: production
            host: corona.cisco.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Upload to ${{ matrix.environment }}
        if: github.ref_name == matrix.branch
        env:
          CORONA_PAT: ${{ secrets[format('CORONA_PAT_{0}', matrix.environment)] }}
          CORONA_HOST: ${{ matrix.host }}
        run: |
          python -m upload_spdx \
            --product "${{ github.event.repository.name }}" \
            --release "${{ github.ref_name }}-${{ github.run_number }}" \
            --image "${{ matrix.environment }}-build" \
            --spdx-file ./spdx.json
```

### Example 3: Scheduled SBOM Updates

```yaml
name: Daily SBOM Update

on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM UTC daily
  workflow_dispatch:

jobs:
  generate-and-upload:
    name: Generate and Upload SBOM
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: spdx-json
          output-file: spdx.json
      
      - name: Upload SBOM to Corona
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: daily-${{ github.run_number }}
          image-name: scheduled-scan-${{ github.run_number }}
          spdx-file-path: ./spdx.json
      
      - name: Archive SBOM
        uses: actions/upload-artifact@v4
        with:
          name: spdx-${{ github.run_number }}
          path: spdx.json
          retention-days: 90
```

---

## Troubleshooting

### Issue: "Authentication Failed"

**Cause**: Invalid or expired CORONA_PAT

**Solution**:
1. Verify secret is set correctly in repository settings
2. Check PAT hasn't expired in Corona
3. Ensure PAT has correct permissions

```yaml
- name: Verify authentication
  env:
    CORONA_PAT: ${{ secrets.CORONA_PAT }}
  run: |
    if [ -z "$CORONA_PAT" ]; then
      echo "::error::CORONA_PAT secret is not set"
      exit 1
    fi
```

### Issue: "SPDX File Not Found"

**Cause**: File path mismatch or file not generated

**Solution**:
```yaml
- name: Verify SPDX file exists
  run: |
    if [ ! -f "./spdx.json" ]; then
      echo "::error::SPDX file not found at ./spdx.json"
      ls -la
      exit 1
    fi
    echo "SPDX file size: $(stat -f%z spdx.json) bytes"
```

### Issue: "Product Not Found"

**Cause**: Product doesn't exist in Corona

**Solution**: The tool automatically creates products, but ensure:
- Product name is valid
- You have permissions to create products
- Check Corona for existing product

```yaml
- name: Upload with product creation
  run: |
    python -m upload_spdx \
      --product "${{ github.event.repository.name }}" \
      --verbose  # See product creation logs
```

---

## Comparison Matrix

| Feature | Docker | Direct Python | Reusable Action |
|---------|--------|---------------|-----------------|
| **Speed** | Moderate | Fast | Moderate |
| **Consistency** | High | Medium | High |
| **Portability** | High | Medium | Low (GitHub only) |
| **Maintenance** | Low | Medium | Medium |
| **Reusability** | Medium | Low | High |
| **Complexity** | Low | Low | Medium |
| **Caching** | Docker layers | pip packages | Docker layers |
| **Best For** | Production | Quick CI | Team projects |

---

## Recommendations

### Choose Docker (Option 1) if:
- ✅ You value consistency with local development
- ✅ You use Docker for local testing
- ✅ You need portability across CI/CD platforms
- ✅ You have complex dependencies

### Choose Direct Python (Option 2) if:
- ✅ Speed is your top priority
- ✅ You're GitHub Actions only
- ✅ You have simple Python dependencies
- ✅ You want minimal configuration

### Choose Reusable Action (Option 3) if:
- ✅ You have multiple workflows using this tool
- ✅ You want to share across repositories
- ✅ You value maintainability and reusability
- ✅ You might publish to Marketplace

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Creating Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [GitHub Context Variables](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker in GitHub Actions](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

---

**For the simplest integration, use the reusable action at `.github/actions/upload-spdx/`**
