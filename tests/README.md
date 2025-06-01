# SEAL API Test Suite

This directory contains comprehensive tests for the SEAL API, designed to achieve 100% code coverage across all modules.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared pytest fixtures and configuration
├── requirements.txt            # Test dependencies
├── pytest.ini                 # Pytest configuration
├── run_tests.py               # Test runner script
├── README.md                  # This file
├── unit/                      # Unit tests
│   ├── app/
│   │   └── test_main.py       # FastAPI application tests
│   ├── schemas/
│   │   ├── test_base.py       # Base schema tests
│   │   └── test_curriculum.py # Curriculum schema tests
│   ├── prompts/
│   │   ├── test_intervention.py # Intervention prompt tests
│   │   └── test_curriculum.py   # Curriculum prompt tests
│   ├── safety/
│   │   └── test_guardrails.py   # Safety validation tests
│   └── llm/
│       ├── test_intervention_gateway.py # Intervention gateway tests
│       └── test_curriculum_gateway.py   # Curriculum gateway tests
├── integration/
│   └── test_api_integration.py # End-to-end API tests
└── fixtures/
    └── sample_data.py         # Test data fixtures
```

## 🚀 Quick Start

### Prerequisites

1. Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

2. Set up environment variables (if needed):
```bash
export GOOGLE_API_KEY="your-test-api-key"
```

### Running Tests

#### Using the Test Runner Script (Recommended)

```bash
# Run all tests with coverage
python tests/run_tests.py

# Run only unit tests
python tests/run_tests.py --unit

# Run only integration tests
python tests/run_tests.py --integration

# Run with HTML coverage report
python tests/run_tests.py --html

# Run specific module tests
python tests/run_tests.py --module schemas/test_base.py

# Run specific test function
python tests/run_tests.py --test test_emt_scores_validation

# Run tests in parallel
python tests/run_tests.py --parallel 4

# Run tests without coverage (faster)
python tests/run_tests.py --no-coverage

# Verbose output
python tests/run_tests.py --verbose
```

#### Using Pytest Directly

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/schemas/test_base.py

# Run specific test function
pytest tests/unit/schemas/test_base.py::TestEMTScores::test_valid_scores

# Run tests with specific marker
pytest -m unit
pytest -m integration
```

## 📊 Coverage Goals

This test suite aims for **100% code coverage** across all modules:

- ✅ **app/main.py** - FastAPI application and endpoints
- ✅ **app/schemas/** - Pydantic models and validation
- ✅ **app/prompts/** - Prompt generation and formatting
- ✅ **app/safety/** - Content safety validation
- ✅ **app/llm/** - LLM gateway integrations

### Coverage Reports

After running tests with coverage, you can view reports in multiple formats:

1. **Terminal Output**: Shows coverage percentages and missing lines
2. **HTML Report**: Detailed interactive report in `htmlcov/index.html`
3. **Coverage Database**: `.coverage` file for further analysis

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)

Test individual components in isolation with mocked dependencies:

- **Schema Tests**: Validate Pydantic models, field validation, and error handling
- **Prompt Tests**: Test prompt generation, formatting, and template rendering
- **Gateway Tests**: Test LLM integration logic with mocked API calls
- **Safety Tests**: Validate content filtering and safety mechanisms
- **Main App Tests**: Test FastAPI endpoints and middleware

### Integration Tests (`tests/integration/`)

Test complete API workflows with realistic scenarios:

- **End-to-End API Tests**: Full request/response cycles
- **Error Handling**: Integration-level error scenarios
- **Safety Integration**: Safety validation in complete flows
- **Concurrent Requests**: Multi-threaded test scenarios
- **Edge Cases**: Boundary conditions and unusual inputs

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

- **Coverage**: Minimum 95% coverage required
- **Async Support**: Automatic async test handling
- **Markers**: Organized test categorization
- **Warnings**: Filtered deprecation warnings

### Fixtures (`conftest.py`)

Shared test fixtures provide:

- **Mock LLM Responses**: Consistent test data
- **Sample Requests**: Realistic API payloads
- **Environment Setup**: Test environment configuration
- **Database Mocks**: Isolated test data

## 📝 Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test Structure

```python
class TestNewFeature:
    """Test cases for new feature."""
    
    def test_valid_input(self):
        """Test with valid input."""
        # Arrange
        input_data = {"key": "value"}
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result.success is True
    
    def test_invalid_input(self):
        """Test with invalid input."""
        with pytest.raises(ValidationError):
            function_under_test(invalid_data)
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async functionality."""
        result = await async_function()
        assert result is not None
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_functionality():
    """Unit test example."""
    pass

@pytest.mark.integration
def test_integration_flow():
    """Integration test example."""
    pass

@pytest.mark.slow
def test_performance_heavy():
    """Slow test that might be skipped."""
    pass
```

## 🐛 Debugging Tests

### Running Failed Tests Only

```bash
pytest --lf  # Last failed
pytest --ff  # Failed first
```

### Debugging with PDB

```bash
pytest --pdb  # Drop into debugger on failure
pytest --pdb-trace  # Drop into debugger at start
```

### Verbose Output

```bash
pytest -v  # Verbose test names
pytest -vv  # Extra verbose
pytest -s  # Don't capture output
```

## 📈 Continuous Integration

This test suite is designed for CI/CD integration:

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    pip install -r tests/requirements.txt
    python tests/run_tests.py --html
    
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Coverage Badges

Generate coverage badges using the coverage reports:

```bash
coverage-badge -o coverage.svg
```

## 🔍 Test Data and Fixtures

### Sample Data

Test fixtures provide realistic data for:

- EMT scores and metadata
- Curriculum requests and responses
- Intervention plans and strategies
- Error scenarios and edge cases

### Mock Strategies

- **LLM Responses**: Predefined realistic responses
- **API Calls**: Mocked external service calls
- **Database**: In-memory test databases
- **File System**: Temporary test files

## 📚 Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test names should describe the scenario
3. **Coverage**: Aim for both line and branch coverage
4. **Performance**: Keep unit tests fast (<1s each)
5. **Maintenance**: Update tests when code changes
6. **Documentation**: Comment complex test scenarios

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Check PYTHONPATH and module structure
2. **Async Issues**: Ensure `pytest-asyncio` is installed
3. **Coverage Gaps**: Use `--cov-report=html` to identify missing lines
4. **Slow Tests**: Use `--fast` flag to skip performance tests
5. **Flaky Tests**: Check for race conditions in concurrent tests

### Getting Help

- Check test output for specific error messages
- Use `pytest --collect-only` to verify test discovery
- Run individual test files to isolate issues
- Check fixture dependencies and mock configurations

---

## 📊 Current Coverage Status

Run `python tests/run_tests.py --html` to generate the latest coverage report and view detailed coverage statistics in `htmlcov/index.html`.

**Target**: 100% coverage across all modules
**Current**: Run tests to see current status 