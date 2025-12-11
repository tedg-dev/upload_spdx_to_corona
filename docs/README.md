# Documentation Directory

This directory contains detailed documentation for the upload_spdx_to_corona project.

## Available Documentation

### Project Structure and Organization

- **[RESTRUCTURE_SUMMARY.md](RESTRUCTURE_SUMMARY.md)**
  - Comprehensive details about the project restructuring
  - Before/after directory structure comparison
  - File modifications and updates
  - Verification steps and results
  - Benefits of the new structure

- **[CLEANUP_VERIFICATION.md](CLEANUP_VERIFICATION.md)**
  - Final cleanup verification report
  - Actions completed during cleanup
  - Duplicate file verification with MD5 checksums
  - Final project structure
  - Verification tests and results
  - Next steps and recommendations

### GitHub and CI/CD

- **[GITHUB_SETUP.md](GITHUB_SETUP.md)**
  - Detailed GitHub repository setup guide
  - Branch protection configuration
  - Security features setup
  - CI/CD workflow overview

- **[GITHUB_NEXT_STEPS.md](GITHUB_NEXT_STEPS.md)**
  - Complete post-setup guide
  - Creating and working with PRs
  - CI/CD workflow details
  - Troubleshooting tips

### Testing and Quality

- **[CODE_COVERAGE.md](CODE_COVERAGE.md)**
  - Code coverage requirements (≥90%)
  - How coverage is enforced in CI/CD
  - Running coverage locally
  - Coverage best practices
  - Troubleshooting coverage issues

## Quick Links

### Main Documentation
- **[Main README](../README.md)** - Comprehensive project documentation at root level

### Key Files
- **[setup_environment.sh](../setup_environment.sh)** - Automated environment setup
- **[Dockerfile](../Dockerfile)** - Container definition
- **[Jenkinsfile](../Jenkinsfile)** - CI/CD pipeline configuration

### Source Code
- **[src/upload_spdx.py](../src/upload_spdx.py)** - Main application module
- **[test/test_upload_spdx.py](../test/test_upload_spdx.py)** - Comprehensive test suite

## Document Organization

All markdown documentation (except README.md) is stored in this `docs/` directory to keep the root clean and organized. This follows best practices for project documentation management.

### When to Add New Documentation

Place new documentation files in this directory when:
- Creating detailed technical specifications
- Writing architecture or design documents
- Adding API documentation
- Creating deployment guides
- Writing troubleshooting guides
- Adding any supplementary documentation

### Naming Conventions

- Use UPPERCASE for major documentation files (e.g., `ARCHITECTURE.md`)
- Use descriptive names that clearly indicate content
- Use underscores for multi-word file names (e.g., `API_REFERENCE.md`)
- Keep filenames concise but meaningful

## Contributing to Documentation

When adding or updating documentation:
1. Place detailed docs in this `docs/` directory
2. Keep the root README.md as the main entry point
3. Link to detailed docs from the main README
4. Update this `docs/README.md` index when adding new files
5. Use clear, consistent markdown formatting

## Documentation Standards

- Use proper markdown formatting
- Include table of contents for longer documents
- Add code examples where appropriate
- Keep language clear and concise
- Include verification steps when describing procedures
- Update documentation when code changes

---

*Last Updated: December 10, 2024*
