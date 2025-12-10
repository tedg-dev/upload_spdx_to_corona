# Code Coverage Requirements

## Overview

This project enforces a **minimum 90% code coverage** requirement to ensure code quality and comprehensive testing.

## Coverage Goal

- **Minimum Required**: 90%
- **Target**: 95%+
- **Enforcement**: CI/CD pipeline fails if coverage drops below 90%

---

## How Coverage is Enforced

### 1. CI/CD Pipeline

Every PR and push triggers automated coverage checks:

```yaml
- Runs pytest with --cov-fail-under=90
- Generates coverage reports (XML, HTML, JSON)
- Posts coverage percentage to PR comments
- Fails build if coverage < 90%
```

### 2. Configuration

Coverage is configured in `.coveragerc`:

```ini
[report]
fail_under = 90
show_missing = True
```

### 3. Multiple Validation Steps

The CI/CD pipeline validates coverage at multiple points:
- **Test Job**: Runs with `--cov-fail-under=90` flag
- **Coverage Check Step**: Validates using `coverage report --fail-under=90`
- **Coverage Badge Step**: Calculates and displays percentage

---

## Running Coverage Locally

### Quick Check

```bash
# Activate virtual environment
source upload_spdx_py_env/bin/activate

# Run tests with coverage requirement
pytest test/test_upload_spdx.py --cov=src --cov-fail-under=90
```

### Detailed Report

```bash
# Generate HTML report
pytest test/test_upload_spdx.py --cov=src --cov-report=html --cov-report=term

# Open in browser
open htmlcov/index.html
```

### Coverage Commands

```bash
# Show coverage summary
coverage report

# Show missing lines
coverage report --show-missing

# Check if meets 90% requirement
coverage report --fail-under=90

# Generate specific format
coverage html    # HTML report
coverage xml     # XML for CI/CD
coverage json    # JSON for parsing
```

---

## Coverage Report Features

### On Pull Requests

Every PR automatically receives:

1. **Coverage Comment**
   ```
   📊 Code Coverage Report
   
   Coverage: 92.5%
   Required: 90%
   
   ✅ Coverage meets requirement
   ```

2. **GitHub Step Summary**
   - Coverage percentage
   - Pass/Fail status
   - Comparison with requirement

3. **Artifacts**
   - HTML coverage report
   - XML coverage data
   - Test results

### Coverage Badges

Coming soon: Coverage badge in README showing current coverage percentage.

---

## What Gets Covered?

### Included in Coverage

- All files in `src/` directory
- All production code
- Error handling paths
- Edge cases

### Excluded from Coverage

```python
# Lines marked with pragma: no cover
def debug_only():  # pragma: no cover
    pass

# Type checking blocks
if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional

# Main execution blocks
if __name__ == "__main__":  # pragma: no cover
    main()

# Abstract methods
@abstractmethod
def abstract_method():  # pragma: no cover
    raise NotImplementedError
```

---

## Coverage Best Practices

### Writing Testable Code

1. **Keep functions small** - Easier to test thoroughly
2. **Reduce complexity** - Lower cyclomatic complexity
3. **Inject dependencies** - Makes mocking easier
4. **Separate concerns** - UI/logic/data layers

### Achieving 90%+ Coverage

```python
# ✅ Good: Testable function
def calculate_total(items, tax_rate):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)

# ❌ Difficult to test: Too much coupling
def calculate_and_save_total(items):
    db = Database.connect()  # Hard to mock
    total = calculate_complex_logic(items, db)
    db.save(total)
    send_email(total)  # Side effect
```

### Test Organization

```python
# Test all paths
def test_function_success():
    """Test happy path"""
    pass

def test_function_with_empty_input():
    """Test edge case"""
    pass

def test_function_with_error():
    """Test error handling"""
    pass

def test_function_with_retry():
    """Test retry logic"""
    pass
```

---

## Current Coverage Status

### Test Suite Statistics

- **Total Tests**: 29
- **Test Classes**: 5
  - `TestCoronaAPIClient`
  - `TestProductManager`
  - `TestReleaseManager`
  - `TestImageManager`
  - `TestSpdxManager`

### Coverage by Module

Check latest coverage in CI/CD artifacts or run locally:

```bash
coverage report --show-missing
```

Example output:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/upload_spdx.py        368     28    92%   45-47, 123-125
-----------------------------------------------------
TOTAL                     368     28    92%
```

---

## Troubleshooting

### Coverage Below 90%

If CI/CD fails due to coverage:

1. **Identify missing coverage**:
   ```bash
   pytest test/ --cov=src --cov-report=term-missing
   ```

2. **Check which lines are uncovered**:
   - Lines marked with `!` in coverage report
   - View HTML report for visual representation

3. **Add tests for uncovered code**:
   - Test error paths
   - Test edge cases
   - Test conditional branches

### False Positives

If code is truly untestable or debug-only:

```python
# Use pragma: no cover sparingly
if debug_mode:  # pragma: no cover
    print(f"Debug: {data}")
```

### Coverage Not Updating

```bash
# Clear coverage data
coverage erase

# Remove cached files
rm -rf .coverage .coverage.* htmlcov/

# Re-run tests
pytest test/ --cov=src
```

---

## CI/CD Integration

### GitHub Actions Workflow

The coverage check is integrated into `.github/workflows/ci.yml`:

**Jobs**:
1. `test` - Runs tests with coverage on multiple Python versions
2. `coverage-report` - Generates and posts coverage report on PRs
3. `pr-checks` - Validates all checks including coverage pass

**Status Checks**:
- `Run Tests (ubuntu-latest, 3.9)` - Must pass with 90% coverage
- `Coverage Report` - Must pass with 90% coverage

### Adding to Branch Protection

After first run, add these required checks:
- `test / Run Tests (ubuntu-latest, 3.9)`
- `coverage-report / Coverage Report`

---

## References

### Tools Used

- **pytest-cov**: Coverage plugin for pytest
- **coverage.py**: Python coverage measurement tool
- **Codecov**: Coverage tracking and visualization

### Configuration Files

- `.coveragerc` - Coverage configuration
- `.github/workflows/ci.yml` - CI/CD pipeline
- `pytest.ini` - Pytest configuration

### Documentation

- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [coverage.py documentation](https://coverage.readthedocs.io/)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

---

**Maintained by**: Ted G  
**Last Updated**: December 10, 2024  
**Coverage Requirement**: ≥90%
