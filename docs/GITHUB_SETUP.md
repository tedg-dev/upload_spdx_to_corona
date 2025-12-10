# GitHub Repository Setup Guide

Complete guide for setting up the `upload_spdx_to_corona` repository on GitHub with CI/CD automation.

## Quick Start

Repository created at: **https://github.com/tedg-dev/upload_spdx_to_corona**

## Step 1: Configure Git and Push Code

```bash
cd /Users/tedg/workspace/upload_spdx_to_corona

# Add GitHub remote (if not already added)
git remote add origin https://github.com/tedg-dev/upload_spdx_to_corona.git

# Or use SSH
git remote add origin git@github.com:tedg-dev/upload_spdx_to_corona.git

# Verify remote
git remote -v

# Check current branch
git branch

# If not on main, create it
git checkout -b main

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial project setup with CI/CD automation

- Add Python application for SPDX upload to Corona
- Include comprehensive test suite (29 tests)
- Add GitHub Actions workflows for CI/CD
- Add Docker support with automated builds
- Add environment setup automation
- Add comprehensive documentation"

# Push to GitHub (ONLY direct push to main)
git push -u origin main
```

## Step 2: Configure Branch Protection

1. Go to **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `main`
3. Enable:
   - ✅ **Require a pull request before merging**
     - Require approvals: 1
   - ✅ **Require status checks to pass before merging**
     - Required checks: `lint`, `test`, `security`, `pr-checks`
   - ✅ **Require conversation resolution before merging**
   - ✅ **Do not allow bypassing the above settings**
   - ✅ **Restrict who can push to matching branches**
   - ❌ **Allow force pushes** (disabled)
4. Click **Create**

## Step 3: Enable GitHub Features

### Security Features (Settings → Security & analysis)
- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning
- ✅ Push protection

### Code Scanning (Security tab)
- CodeQL workflow is already configured in `.github/workflows/codeql.yml`
- It will run automatically on first push

## Step 4: Create Development Branch

```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Optionally set develop as default branch:
# Go to Settings → Branches → Default branch → Switch to 'develop'
```

## Step 5: Configure Repository Secrets (Optional)

If you need to run integration tests in CI/CD:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `CORONA_PAT` - Personal Access Token
   - `CORONA_HOST` - Corona host URL
   - `CORONA_USERNAME` - Corona username

## Working with Pull Requests

### Create Feature Branch

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feat/your-feature-name

# Make changes, then commit
git add .
git commit -m "feat: description of your feature"

# Push to GitHub
git push -u origin feat/your-feature-name
```

### Create Pull Request

1. Go to GitHub repository
2. Click **Pull requests** → **New pull request**
3. Base: `develop`, Compare: `feat/your-feature-name`
4. Fill in title and description
5. Click **Create pull request**
6. Wait for CI checks to pass
7. Request review
8. Merge after approval

### Commit Message Format

Use conventional commits:
```
feat: add new feature
fix: fix bug in component
docs: update documentation
test: add tests
refactor: refactor code
chore: update dependencies
ci: update CI configuration
```

## CI/CD Workflows Overview

### 1. **CI/CD Pipeline** (`.github/workflows/ci.yml`)
Runs on every push and PR:
- **Lint**: Code quality checks (black, flake8, pylint, isort)
- **Security**: Security scanning (bandit, safety)
- **Test**: Run tests on multiple OS and Python versions
- **Docker**: Build and push Docker images (only on main/develop)
- **PR Checks**: Validate PR format and commits

### 2. **CodeQL Security** (`.github/workflows/codeql.yml`)
- Runs weekly and on every push/PR
- Scans for security vulnerabilities

### 3. **Dependency Review** (`.github/workflows/dependency-review.yml`)
- Runs on PRs
- Reviews dependency changes for vulnerabilities

### 4. **Release** (`.github/workflows/release.yml`)
- Triggered by version tags (v*.*.*)
- Creates GitHub release with changelog
- Builds and pushes Docker image

## Creating a Release

```bash
# Tag a release
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This triggers the release workflow automatically.

## Viewing CI/CD Results

1. Go to **Actions** tab in GitHub
2. Click on any workflow run to see details
3. Download artifacts (test reports, coverage) from completed runs

## Troubleshooting

### CI Checks Failing

**Linting errors:**
```bash
# Run locally before pushing
black src/ test/
isort src/ test/
flake8 src/ test/ --max-line-length=120
```

**Test failures:**
```bash
# Run tests locally
pytest test/test_upload_spdx.py -v
```

### Docker Build Fails

```bash
# Test Docker build locally
docker build -t upload_spdx:test .
```

### Can't Push to Main

This is expected! Branch protection is working.
- Always create a PR
- Never push directly to main (except initial push)

## Additional Files Created

The following files support the GitHub CI/CD:
- `.github/workflows/ci.yml` - Main CI/CD pipeline
- `.github/workflows/codeql.yml` - Security scanning
- `.github/workflows/dependency-review.yml` - Dependency checks
- `.github/workflows/release.yml` - Release automation
- `.gitignore` - Git ignore rules
- `.github/pull_request_template.md` - PR template (to be created)
- `.github/CODEOWNERS` - Code owners (optional)

## Best Practices

1. ✅ Always work in feature branches
2. ✅ Create PRs for all changes
3. ✅ Wait for CI checks to pass
4. ✅ Get code review before merging
5. ✅ Use conventional commit messages
6. ✅ Keep PRs small and focused
7. ✅ Update tests with code changes
8. ✅ Update documentation as needed

## Support

For issues or questions:
- Check Actions tab for workflow failures
- Review workflow logs for error details
- Consult documentation in `docs/` directory

---

**Repository**: https://github.com/tedg-dev/upload_spdx_to_corona  
**Last Updated**: December 10, 2024
