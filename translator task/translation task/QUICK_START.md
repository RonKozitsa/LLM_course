# Quick Start Guide
## Multi-Stage Translation Quality Analysis System

**Version:** 2.0 (Reorganized Structure)
**Last Updated:** November 27, 2025

---

## 📁 New Project Structure

The project has been reorganized into a professional folder structure:

```
translation-task/
├── config/                # Configuration files
├── data/                  # All data files
│   ├── input/            # Original data
│   ├── intermediate/     # Translation steps
│   └── output/           # Final results
├── scripts/               # Python scripts
├── notebooks/             # Jupyter notebooks
├── visualizations/        # Generated plots
├── docs/                  # Documentation
└── tests/                 # Test suite
```

---

## 🚀 Quick Commands

### Run Main Analysis

```bash
# From project root
python scripts/sentence_vector_comparison.py
```

**Output:**
- `data/output/vector_similarity_results.csv`
- `data/output/vector_similarity_averaged.csv`
- `visualizations/vector_similarity_vs_mistakes.png`

---

### Run Enhanced Statistical Analysis

```bash
python scripts/statistical_analysis_enhanced.py
```

**Output:**
- `data/output/statistical_analysis_report.txt`

**Includes:**
- Formal hypothesis testing (H0/H1, p-values)
- 95% confidence intervals
- ANOVA analysis
- Effect size calculations
- Normality tests

---

### Run Comparative Model Analysis

```bash
python scripts/comparative_model_analysis.py
```

**Output:**
- `data/output/comparative_analysis_report.txt`
- `visualizations/model_comparison_visualization.png`
- `data/output/comparative_analysis_results.csv`

**Note:** This downloads 4 different models (~2GB), may take 20-30 minutes first time.

---

### Open Jupyter Notebook

```bash
jupyter notebook notebooks/analysis_notebook.ipynb
```

**Features:**
- Interactive EDA with 10+ visualizations
- Step-by-step statistical analysis
- Outlier analysis
- Correlation heatmaps

---

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=scripts --cov-report=html

# Unit tests only (fast)
pytest tests/ -m unit -v

# Specific test file
pytest tests/test_data_validation.py -v
```

---

## 📊 Data Files

### Input

| File | Location | Description |
|------|----------|-------------|
| Original English | `data/input/English.csv` | 170 sentences with 4-20 errors |

### Intermediate (Translation Pipeline)

| File | Location | Description |
|------|----------|-------------|
| French | `data/intermediate/French.csv` | EnglishToFrench output |
| Hebrew | `data/intermediate/Hebrew.csv` | FrenchToHebrew output |

### Output (Final Results)

| File | Location | Description |
|------|----------|-------------|
| Final English | `data/output/English_final.csv` | Back-translated English |
| Individual Results | `data/output/vector_similarity_results.csv` | All 170 comparisons |
| Averaged Results | `data/output/vector_similarity_averaged.csv` | Grouped by error count |
| Statistical Report | `data/output/statistical_analysis_report.txt` | Full statistical analysis |

---

## 📚 Documentation

| Document | Location | Description |
|----------|----------|-------------|
| README | `README.md` | Main project documentation |
| PRD | `docs/PRD.md` | Product Requirements (647 lines) |
| Prompt Book | `docs/PROMPT_BOOK.md` | AI development process |
| Token Analysis | `docs/TOKEN_COST_ANALYSIS.md` | Cost analysis & optimization |
| Project Structure | `PROJECT_STRUCTURE.md` | Detailed folder organization |

---

## 🔧 Configuration

Edit `config/config.yaml` to customize:
- Model selections
- File paths
- Statistical parameters
- Visualization settings

---

## 📈 Expected Results

### Main Analysis

- **Correlation:** r = -0.19 (statistically significant, p = 0.012)
- **Average Similarity:** 0.6891
- **Interpretation:** Moderate negative correlation between errors and similarity

### Statistical Analysis

- **Hypothesis Test:** ✓ REJECT H0 (significant correlation exists)
- **95% CI:** [-0.33, -0.04]
- **ANOVA:** F = 1.38, p = 0.16 (no significant group differences)
- **Effect Size:** η² = 0.126 (12.6% variance explained)

---

## ⚠️ Important Notes

### Path Updates

All scripts now use the new folder structure. If you move files:

1. Update paths in scripts, OR
2. Edit `config/config.yaml`

### Running from Different Directories

Scripts use relative paths from project root. Always run from:

```bash
cd "/path/to/translation task"
python scripts/scriptname.py
```

Or use absolute paths:

```bash
python "/path/to/translation task/scripts/scriptname.py"
```

---

## 🐛 Troubleshooting

### "File not found" Error

**Problem:** Scripts can't find data files

**Solution:**
```bash
# Check you're in project root
pwd
# Should show: .../translation task

# Verify data files exist
ls data/input/English.csv
ls data/output/English_final.csv

# If not, check original location
ls *.csv
```

---

### Import Errors

**Problem:** Can't import modules

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# For tests
pip install -r tests/requirements_test.txt
```

---

### Model Download Fails

**Problem:** sentence-transformers can't download models

**Solution:**
```bash
# Pre-download main model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Check cache location
python -c "from sentence_transformers import SentenceTransformer; print(SentenceTransformer._get_cache_folder())"
```

---

## 📦 Installation

### From Scratch

```bash
# 1. Clone/download project
cd "/path/to/translation task"

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install test dependencies (optional)
pip install -r tests/requirements_test.txt

# 4. Verify installation
python scripts/sentence_vector_comparison.py --help
```

### Virtual Environment (Recommended)

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run analysis
python scripts/sentence_vector_comparison.py
```

---

## 🎯 Common Workflows

### Complete Analysis Pipeline

```bash
# 1. Run main similarity analysis
python scripts/sentence_vector_comparison.py

# 2. Run statistical analysis
python scripts/statistical_analysis_enhanced.py

# 3. View results
cat data/output/statistical_analysis_report.txt
open visualizations/vector_similarity_vs_mistakes.png

# 4. (Optional) Interactive analysis
jupyter notebook notebooks/analysis_notebook.ipynb
```

### Testing Workflow

```bash
# 1. Run quick unit tests
pytest tests/ -m unit -v

# 2. Run full test suite
pytest tests/ -v

# 3. Generate coverage report
pytest tests/ --cov=scripts --cov-report=html

# 4. View coverage
open htmlcov/index.html
```

### Development Workflow

```bash
# 1. Make changes to scripts
nano scripts/sentence_vector_comparison.py

# 2. Test changes
pytest tests/test_sentence_vector_comparison.py -v

# 3. Run script
python scripts/sentence_vector_comparison.py

# 4. Verify outputs
ls -lh data/output/
```

---

## 📞 Getting Help

1. **Project Structure:** See `PROJECT_STRUCTURE.md`
2. **Full Documentation:** See `docs/PRD.md`
3. **API Details:** See docstrings in scripts
4. **Test Examples:** See `tests/` directory

---

## ✅ Pre-flight Checklist

Before running analysis, verify:

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip list | grep pandas`)
- [ ] Data files in correct locations (`ls data/input/`, `ls data/output/`)
- [ ] Sufficient disk space (~500MB for models)
- [ ] Internet connection (for first-time model download)

---

**Status:** ✅ Project Reorganized and Ready
**Version:** 2.0
**Date:** November 27, 2025
