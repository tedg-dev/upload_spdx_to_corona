# Security Guidelines

## Environment Variables

**NEVER commit secrets, tokens, or credentials to the repository.**

All sensitive configuration must be provided via environment variables:

### Required Variables
- `CORONA_PAT` - Corona Personal Access Token
- `CORONA_USERNAME` - Your Corona username
- `CORONA_PRODUCT_NAME` - Product name
- `CORONA_RELEASE_VERSION` - Release version
- `CORONA_IMAGE_NAME` - Image name

### Optional Variables (with defaults)
- `CORONA_HOST` - Corona host (default: `corona.cisco.com`)
- `CORONA_SECURITY_CONTACT` - Security contact email (default: `upload_spdx_mailer`)
- `CORONA_ENGINEERING_CONTACT` - Engineering contact email (default: `upload_spdx_mailer`)
- `CORONA_SPDX_FILE_PATH` - Path to SPDX file (default: `./bes-traceability-spdx.json`)

## Local Configuration (keys.json)

For local development, you can create a `keys.json` file (NOT committed to git):

1. Copy the example file:
   ```bash
   cp keys.json.example keys.json
   ```

2. Edit `keys.json` with your actual values

3. Load it before running:
   ```bash
   export $(cat keys.json | jq -r 'to_entries | .[] | "\(.key)=\(.value)"')
   python3 -m upload_spdx
   ```

## Files Ignored by Git

The following files are automatically ignored (see `.gitignore`):
- `keys.json` - Local credentials
- `key.json` - Alternative credentials file
- `*.key` - Any key files
- `*.pem` - Certificate files
- `.secrets` - Secret files
- `secrets.yml` - Secret configuration

## Secret Scanning

This repository uses:
- **GitHub Secret Scanning** - Automatic detection of committed secrets
- **Bandit** - Python security issue scanner
- **Safety** - Dependency vulnerability scanner

## If You Accidentally Commit a Secret

1. **Immediately revoke the secret** (PAT, password, etc.)
2. Generate a new secret
3. Update your local configuration
4. Contact security team if needed

**DO NOT** try to hide it by rewriting git history - the secret may already be exposed.
