# Test Suite

Comprehensive unit and integration tests for the Multi-Stage Translation Quality Analysis System.

## 📋 Test Coverage

The test suite covers:

- ✅ **CSV Data Loading** - File existence, structure, data types
- ✅ **Data Validation** - Row alignment, index integrity, null checks
- ✅ **Translation Pipeline** - Data flow through English → French → Hebrew → English
- ✅ **Vector Encoding** - Sentence embedding model, vector dimensions
- ✅ **Similarity Computation** - Cosine similarity calculation, value ranges
- ✅ **Statistical Analysis** - Grouping, averaging, correlation calculations
- ✅ **Output Generation** - CSV files, visualization, data integrity
- ✅ **Edge Cases** - Empty data, identical sentences, error handling
- ✅ **Performance** - Encoding speed, memory efficiency

## 🚀 Running Tests

### Install Test Dependencies

```bash
pip install -r tests/requirements_test.txt
```

### Run All Tests

```bash
# From project root
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Test sentence vector comparison functionality
pytest tests/test_sentence_vector_comparison.py -v

# Test data validation
pytest tests/test_data_validation.py -v
```

### Run by Test Category

```bash
# Run only unit tests (fast)
pytest tests/ -m unit -v

# Run only integration tests
pytest tests/ -m integration -v

# Exclude slow tests
pytest tests/ -m "not slow" -v
```

### Run with Coverage Report

```bash
# Generate coverage report
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Parallel Test Execution

```bash
# Run tests in parallel (faster)
pytest tests/ -n auto
```

## 📊 Test Organization

```
tests/
├── __init__.py                          # Package initialization
├── conftest.py                          # Pytest configuration and fixtures
├── test_sentence_vector_comparison.py   # Main analysis script tests
├── test_data_validation.py              # Data integrity tests
├── requirements_test.txt                # Test dependencies
└── README.md                           # This file
```

## 🧪 Test Classes

### test_sentence_vector_comparison.py

| Test Class                  | Description                                    |
|-----------------------------|------------------------------------------------|
| `TestCSVLoading`            | CSV file loading and structure validation      |
| `TestDataValidation`        | Data integrity, ranges, and distributions      |
| `TestVectorEncoding`        | Sentence embedding and encoding                |
| `TestStatisticalCalculations`| Grouping, averaging, correlation              |
| `TestOutputFiles`           | Output file generation and validity            |
| `TestEdgeCases`             | Edge cases and error handling                  |
| `TestIntegration`           | Full pipeline integration tests                |
| `TestPerformance`           | Performance and efficiency tests               |

### test_data_validation.py

| Test Class                         | Description                                |
|------------------------------------|--------------------------------------------|
| `TestTranslationPipelineDataFlow`  | Data flow through translation pipeline     |
| `TestEnglishCSVValidation`         | English.csv specific validation            |
| `TestFrenchCSVValidation`          | French.csv specific validation             |
| `TestHebrewCSVValidation`          | Hebrew.csv specific validation             |
| `TestEnglishFinalCSVValidation`    | English_final.csv specific validation      |
| `TestOutputCSVValidation`          | Analysis output CSV validation             |
| `TestDataConsistency`              | Cross-file data consistency                |

## 📝 Test Markers

Tests are marked with the following categories:

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests (slower)
- `@pytest.mark.slow` - Slow tests (model loading, full pipeline)

## 🔍 Example Usage

### Run Quick Unit Tests Only

```bash
pytest tests/ -m unit --tb=short
```

### Run Full Test Suite with Detailed Output

```bash
pytest tests/ -v --tb=long
```

### Run Tests and Generate Coverage Report

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Run Specific Test Method

```bash
pytest tests/test_sentence_vector_comparison.py::TestVectorEncoding::test_vector_dimensions -v
```

## 🛠️ Writing New Tests

### Using Fixtures

Fixtures are defined in `conftest.py` and can be used in any test:

```python
def test_example(sentence_model, sample_sentences):
    """Example test using fixtures"""
    vectors = sentence_model.encode(sample_sentences)
    assert len(vectors) == len(sample_sentences)
```

### Available Fixtures

- `sentence_model` - Pre-loaded SentenceTransformer model (session-scoped)
- `project_root` - Path to project root directory
- `english_csv_path` - Path to English.csv
- `english_final_csv_path` - Path to English_final.csv
- `french_csv_path` - Path to French.csv
- `hebrew_csv_path` - Path to Hebrew.csv
- `sample_sentences` - List of sample sentences for testing
- `sample_csv_data` - Sample DataFrame for testing
- `load_english_csv` - Pre-loaded English.csv DataFrame
- `load_english_final_csv` - Pre-loaded English_final.csv DataFrame

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

## ✅ Test Requirements

For tests to pass, the following files should exist:

- `English.csv` - Original English sentences with errors
- `French.csv` - French translations
- `Hebrew.csv` - Hebrew translations
- `English_final.csv` - Back-translated English
- `sentence_vector_comparison.py` - Analysis script

## 📈 Expected Test Results

With all files present and valid:

- **Total Tests**: ~50+ tests
- **Expected Pass Rate**: 100%
- **Execution Time**:
  - Unit tests only: ~5-10 seconds
  - Full suite (including slow tests): ~30-60 seconds

## 🐛 Troubleshooting

### Model Download Issues

If tests fail due to model download:

```bash
# Pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Missing CSV Files

If tests skip due to missing files:

```bash
# Ensure translation pipeline has been run
# Run agents: EnglishToFrench, FrenchToHebrew, HebrewToEnglish
# Then run: python3 sentence_vector_comparison.py
```

### Import Errors

If tests fail with import errors:

```bash
# Ensure parent directory is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

## 🔧 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r tests/requirements_test.txt
      - name: Run tests
        run: |
          pytest tests/ -v --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [SentenceTransformers Documentation](https://www.sbert.net/)

## 🤝 Contributing Tests

When adding new features, please:

1. Write tests first (TDD approach)
2. Ensure >80% code coverage
3. Mark tests appropriately (unit/integration/slow)
4. Update this README if adding new test categories
5. Run full test suite before committing

---

**Test Suite Version**: 1.0.0

**Last Updated**: November 27, 2025
