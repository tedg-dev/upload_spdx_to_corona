# Upload SPDX to Corona - GitHub Action

A reusable GitHub Action for uploading SPDX documents to the Cisco Corona platform.

## Usage

### Basic Example

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
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.ref_name }}
          image-name: ci-build-${{ github.run_number }}
          spdx-file-path: ./spdx.json
```

### Advanced Example with All Options

```yaml
- name: Upload SPDX to Corona
  uses: ./.github/actions/upload-spdx
  with:
    # Required inputs
    corona-pat: ${{ secrets.CORONA_PAT }}
    product-name: 'My Product'
    release-version: '1.0.0'
    image-name: 'my-image-v1'
    spdx-file-path: './build/spdx.json'
    
    # Optional inputs
    corona-host: 'corona.cisco.com'
    corona-username: ${{ secrets.CORONA_USERNAME }}
    security-contact: 'security@example.com'
    engineering-contact: 'engineering@example.com'
    verbose: 'true'
    method: 'docker'  # or 'python'
```

### Using from Another Repository

If you want to use this action from a different repository:

```yaml
- name: Upload SPDX to Corona
  uses: tedg-dev/upload_spdx_to_corona/.github/actions/upload-spdx@main
  with:
    corona-pat: ${{ secrets.CORONA_PAT }}
    product-name: ${{ github.event.repository.name }}
    release-version: ${{ github.ref_name }}
    image-name: ci-build-${{ github.run_number }}
    spdx-file-path: ./spdx.json
```

## Inputs

### Required Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `corona-pat` | Corona Personal Access Token | `${{ secrets.CORONA_PAT }}` |
| `product-name` | Product name in Corona | `My Product` |
| `release-version` | Release version string | `1.0.0` |
| `image-name` | Image name in Corona | `my-image-v1` |
| `spdx-file-path` | Path to SPDX JSON file | `./spdx.json` |

### Optional Inputs

| Input | Description | Default | Example |
|-------|-------------|---------|---------|
| `corona-host` | Corona host domain | `corona.cisco.com` | `corona-dev.cisco.com` |
| `corona-username` | Corona username | _(empty)_ | `user.gen` |
| `security-contact` | Security contact | `upload_spdx_mailer` | `security@example.com` |
| `engineering-contact` | Engineering contact | `upload_spdx_mailer` | `eng@example.com` |
| `verbose` | Enable verbose logging | `false` | `true` |
| `method` | Execution method | `docker` | `docker` or `python` |

## Outputs

| Output | Description |
|--------|-------------|
| `status` | Upload status (`success` or `failure`) |
| `product-id` | Product ID in Corona |
| `release-id` | Release ID in Corona |
| `image-id` | Image ID in Corona |

## Examples

### Upload on Release

```yaml
name: Upload SPDX on Release

on:
  release:
    types: [published]

jobs:
  upload-spdx:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate SPDX
        run: |
          # Your SPDX generation logic
          ./scripts/generate-spdx.sh > spdx.json
      
      - name: Upload to Corona
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.event.release.tag_name }}
          image-name: release-${{ github.event.release.tag_name }}
          spdx-file-path: ./spdx.json
```

### Upload with Different Environments

```yaml
name: Upload SPDX to Multiple Environments

on:
  push:
    branches: [develop, staging, main]

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine environment
        id: env
        run: |
          if [[ "${{ github.ref_name }}" == "main" ]]; then
            echo "host=corona.cisco.com" >> $GITHUB_OUTPUT
            echo "env=production" >> $GITHUB_OUTPUT
          elif [[ "${{ github.ref_name }}" == "staging" ]]; then
            echo "host=corona-stage.cisco.com" >> $GITHUB_OUTPUT
            echo "env=staging" >> $GITHUB_OUTPUT
          else
            echo "host=corona-dev.cisco.com" >> $GITHUB_OUTPUT
            echo "env=development" >> $GITHUB_OUTPUT
          fi
      
      - name: Upload to ${{ steps.env.outputs.env }}
        uses: ./.github/actions/upload-spdx
        with:
          corona-pat: ${{ secrets.CORONA_PAT }}
          corona-host: ${{ steps.env.outputs.host }}
          product-name: ${{ github.event.repository.name }}
          release-version: ${{ github.ref_name }}-${{ github.run_number }}
          image-name: ${{ steps.env.outputs.env }}-build
          spdx-file-path: ./spdx.json
```

### Using Python Method for Speed

```yaml
- name: Upload SPDX (Fast Python Method)
  uses: ./.github/actions/upload-spdx
  with:
    corona-pat: ${{ secrets.CORONA_PAT }}
    product-name: ${{ github.event.repository.name }}
    release-version: ${{ github.ref_name }}
    image-name: quick-build-${{ github.run_number }}
    spdx-file-path: ./spdx.json
    method: python  # Faster than docker
    verbose: true
```

### Handle Upload Failure

```yaml
- name: Upload SPDX
  id: upload
  uses: ./.github/actions/upload-spdx
  continue-on-error: true
  with:
    corona-pat: ${{ secrets.CORONA_PAT }}
    product-name: ${{ github.event.repository.name }}
    release-version: ${{ github.ref_name }}
    image-name: ci-build-${{ github.run_number }}
    spdx-file-path: ./spdx.json

- name: Check upload status
  if: steps.upload.outputs.status == 'failure'
  run: |
    echo "::error::SPDX upload failed"
    # Notify team, create issue, etc.
```

## Requirements

### Repository Secrets

You must configure these secrets in your repository:

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Click: `New repository secret`
3. Add:
   - **CORONA_PAT** (required) - Your Corona Personal Access Token
   - **CORONA_USERNAME** (optional) - Your Corona username

### Prerequisites

- The SPDX file must exist before calling this action
- The file must be in valid SPDX JSON format
- You must have appropriate permissions in Corona

## Execution Methods

### Docker Method (Default)

- **Pros**: Consistent environment, same as local development
- **Cons**: Slower startup due to Docker build
- **Use when**: You want consistency with local testing

```yaml
method: docker
```

### Python Method

- **Pros**: Faster execution, uses pip cache
- **Cons**: Different environment from local Docker
- **Use when**: Speed is critical, simple dependencies

```yaml
method: python
```

## Troubleshooting

### Authentication Failed

**Error**: `Authentication failed` or `Invalid PAT`

**Solution**:
1. Verify `CORONA_PAT` secret is set in repository settings
2. Check PAT hasn't expired in Corona
3. Ensure PAT has correct permissions

### SPDX File Not Found

**Error**: `SPDX file not found: ./spdx.json`

**Solution**:
1. Ensure SPDX file is generated before this step
2. Check the file path is correct
3. Verify file exists with `ls -la` in a previous step

### Product Creation Failed

**Error**: `Failed to create product`

**Solution**:
1. Ensure you have permissions to create products in Corona
2. Check product name is valid (no special characters)
3. Try with `verbose: true` to see detailed logs

## Best Practices

### Use Dynamic Values

```yaml
product-name: ${{ github.event.repository.name }}
release-version: ${{ github.ref_name }}
image-name: ci-build-${{ github.run_number }}
```

### Enable Verbose Logging for Debugging

```yaml
verbose: true
```

### Cache Docker Builds

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Upload SPDX
  uses: ./.github/actions/upload-spdx
  with:
    method: docker
    # ... other inputs
```

### Use Matrix for Multiple Uploads

```yaml
strategy:
  matrix:
    environment: [dev, staging, prod]

steps:
  - uses: ./.github/actions/upload-spdx
    with:
      product-name: ${{ matrix.environment }}-product
      # ... other inputs
```

## Contributing

See the main repository README for contribution guidelines.

## License

See the main repository LICENSE file.

## Support

For issues or questions:
1. Check [GITHUB_ACTIONS_USAGE.md](../../../docs/GITHUB_ACTIONS_USAGE.md) for detailed usage
2. Review [troubleshooting section](#troubleshooting)
3. Open an issue in the repository

---

**Part of the [upload_spdx_to_corona](https://github.com/tedg-dev/upload_spdx_to_corona) project**
