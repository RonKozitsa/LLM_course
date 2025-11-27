# Project Structure
## Multi-Stage Translation Quality Analysis System

**Organized:** November 27, 2025
**Version:** 2.0 (Reorganized)

---

## Directory Structure

```
translation-task/
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
│
├── config/                            # Configuration files
│   └── config.yaml                    # Central configuration
│
├── data/                              # All data files
│   ├── input/                         # Original input data
│   │   └── English.csv               # 170 sentences with errors (4-20 per sentence)
│   │
│   ├── intermediate/                  # Translation pipeline intermediate outputs
│   │   ├── French.csv                # EnglishToFrench agent output
│   │   └── Hebrew.csv                # FrenchToHebrew agent output
│   │
│   └── output/                        # Final outputs and analysis results
│       ├── English_final.csv         # HebrewToEnglish agent output
│       ├── vector_similarity_results.csv          # Individual sentence comparisons
│       ├── vector_similarity_averaged.csv         # Grouped averages by error count
│       ├── statistical_analysis_report.txt        # Comprehensive statistical report
│       ├── comparative_analysis_report.txt        # Model comparison report
│       └── comparative_analysis_results.csv       # Model comparison data
│
├── scripts/                           # Python analysis scripts
│   ├── sentence_vector_comparison.py              # Main similarity analysis
│   ├── statistical_analysis_enhanced.py           # Advanced statistical tests
│   └── comparative_model_analysis.py              # Multi-model comparison
│
├── notebooks/                         # Jupyter notebooks
│   └── analysis_notebook.ipynb       # Interactive EDA and analysis
│
├── visualizations/                    # Generated plots and figures
│   ├── vector_similarity_vs_mistakes.png         # Main results visualization
│   └── model_comparison_visualization.png        # Comparative analysis plot
│
├── docs/                              # Documentation
│   ├── README.md                     # Project documentation (copy)
│   ├── PRD.md                        # Product Requirements Document
│   ├── PROMPT_BOOK.md                # AI development and prompt engineering
│   └── TOKEN_COST_ANALYSIS.md        # Cost analysis and optimization
│
└── tests/                             # Test suite (50+ tests)
    ├── __init__.py                   # Test package initialization
    ├── conftest.py                   # Pytest configuration and fixtures
    ├── test_sentence_vector_comparison.py         # Main script tests
    ├── test_data_validation.py                    # Data integrity tests
    ├── requirements_test.txt         # Test dependencies
    └── README.md                     # Test documentation
```

---

## File Descriptions

### Root Level

**README.md**
- Main project documentation
- Quick start guide
- Installation instructions
- Usage examples

**requirements.txt**
- All Python dependencies
- Includes: pandas, numpy, sentence-transformers, scipy, statsmodels, matplotlib, seaborn, jupyter

**.gitignore**
- Git ignore patterns
- Excludes: Python cache, virtual environments, model cache, system files

---

### config/

**config.yaml**
- Centralized configuration for all scripts
- Model specifications (primary and comparative models)
- Statistical parameters (alpha, confidence levels)
- Visualization settings
- File paths (can be adjusted here)
- Performance settings

---

### data/

#### data/input/

**English.csv**
- Original input dataset
- 170 sentences with intentional spelling errors
- Columns: Index, text, mistakes
- Stratified sampling: 10 sentences per error count (4-20)

#### data/intermediate/

**French.csv**
- Output from EnglishToFrench agent
- Errors corrected, natural French translation
- Columns: Index, text

**Hebrew.csv**
- Output from FrenchToHebrew agent
- Right-to-left (RTL) formatted Hebrew
- Columns: Index, text

#### data/output/

**English_final.csv**
- Final output from HebrewToEnglish agent
- Back-translated English after 3-stage pipeline
- Columns: Index, text

**vector_similarity_results.csv**
- Individual sentence similarity scores
- 170 rows with cosine similarity for each sentence
- Columns: Index, Mistakes, Cosine_Similarity, Original_Sentence, Final_Sentence

**vector_similarity_averaged.csv**
- Grouped statistics by error count
- 17 rows (one per error count 4-20)
- Columns: Mistakes, Avg_Similarity, Std_Dev, Count

**statistical_analysis_report.txt**
- Comprehensive statistical analysis report
- Hypothesis testing results (H0/H1, p-values)
- Confidence intervals
- ANOVA results
- Effect size calculations

**comparative_analysis_report.txt**
- Comparison of multiple embedding models
- Performance metrics across 4 models
- Baseline comparison
- Recommendations

**comparative_analysis_results.csv**
- Tabular data from model comparison
- Columns: Model, Vector_Dimensions, Mean_Similarity, Correlation, etc.

---

### scripts/

**sentence_vector_comparison.py**
- Main analysis script
- Calculates cosine similarity between original and final English
- Groups by error count and calculates averages
- Generates visualization with error bars and trend line
- **Usage:** `python scripts/sentence_vector_comparison.py`

**statistical_analysis_enhanced.py**
- Advanced statistical analysis
- Formal hypothesis testing (Pearson, Spearman)
- 95% confidence intervals
- ANOVA and Tukey HSD post-hoc tests
- Effect size calculations (Cohen's d, eta-squared)
- Normality tests
- Generates statistical_analysis_report.txt
- **Usage:** `python scripts/statistical_analysis_enhanced.py`

**comparative_model_analysis.py**
- Compares 4 different sentence embedding models
- Baseline identity comparison
- Performance metrics and visualizations
- Generates comparative reports
- **Usage:** `python scripts/comparative_model_analysis.py`

---

### notebooks/

**analysis_notebook.ipynb**
- Interactive Jupyter notebook
- Exploratory Data Analysis (EDA)
- Step-by-step statistical analysis
- Multiple visualizations (histograms, box plots, violin plots, Q-Q plots)
- Correlation heatmaps
- Outlier analysis
- Hypothesis testing walkthrough
- **Usage:** `jupyter notebook notebooks/analysis_notebook.ipynb`

---

### visualizations/

**vector_similarity_vs_mistakes.png**
- Main results visualization
- Scatter plot with error bars showing average similarity by error count
- Includes trend line and statistics box
- 300 DPI, 14" × 9" figure

**model_comparison_visualization.png**
- 4-panel comparison of different models
- Bar charts for mean similarity, correlation, processing time
- Box plot for distribution comparison

---

### docs/

**README.md**
- Copy of main README for documentation folder
- Project overview and quick reference

**PRD.md (Product Requirements Document)**
- Comprehensive technical specification (647 lines)
- System architecture
- Technical specifications (CSV formats, models, metrics)
- Key findings and results
- Testing & quality assurance (Section 9)
- Dependencies and workflow
- File structure and references

**PROMPT_BOOK.md**
- Complete AI development documentation (550+ lines)
- All 3 translation agent prompts with iterations
- Design decisions and rationale
- Token usage per agent
- Iteration process and testing methodology
- Lessons learned

**TOKEN_COST_ANALYSIS.md**
- Comprehensive token usage breakdown
- Cost analysis per component
- Optimization strategies (30-75% savings)
- ROI analysis (400-700x return)
- Comparative cost analysis vs alternatives
- Recommendations for future projects

---

### tests/

**Complete test suite with 50+ tests**

**__init__.py**
- Test package initialization

**conftest.py**
- Pytest configuration
- Shared fixtures (sentence_model, file paths, sample data)
- Test markers (unit, integration, slow)

**test_sentence_vector_comparison.py**
- 40+ tests for main analysis script
- CSV loading, vector encoding, statistical calculations
- Output file generation, edge cases, performance

**test_data_validation.py**
- 30+ tests for data integrity
- Translation pipeline data flow
- CSV structure validation for all files
- Cross-file consistency checks

**requirements_test.txt**
- Test-specific dependencies (pytest, pytest-cov, pytest-mock)

**README.md**
- Test documentation
- Usage instructions
- Coverage information

---

## Usage Workflows

### Standard Analysis Workflow

```bash
# 1. Ensure data files are in place
ls data/input/English.csv
ls data/output/English_final.csv

# 2. Run main similarity analysis
python scripts/sentence_vector_comparison.py

# 3. Run enhanced statistical analysis
python scripts/statistical_analysis_enhanced.py

# 4. (Optional) Run comparative model analysis
python scripts/comparative_model_analysis.py

# 5. (Optional) Open Jupyter notebook for interactive analysis
jupyter notebook notebooks/analysis_notebook.ipynb
```

### Testing Workflow

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run only unit tests
pytest tests/ -m unit -v

# Run specific test file
pytest tests/test_data_validation.py -v
```

### Development Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install -r tests/requirements_test.txt

# 2. Configure settings (optional)
nano config/config.yaml

# 3. Run analysis
python scripts/sentence_vector_comparison.py

# 4. Review outputs
cat data/output/statistical_analysis_report.txt
open visualizations/vector_similarity_vs_mistakes.png

# 5. Run tests to validate
pytest tests/ -v
```

---

## Path Updates

### Scripts Now Reference:

**Input Paths:**
- `data/input/English.csv`
- `data/output/English_final.csv`

**Output Paths:**
- `data/output/vector_similarity_results.csv`
- `data/output/vector_similarity_averaged.csv`
- `data/output/statistical_analysis_report.txt`
- `visualizations/vector_similarity_vs_mistakes.png`

### Configuration:

All paths can be customized in `config/config.yaml`

---

## Benefits of This Structure

1. **Clear Separation of Concerns**
   - Data, code, documentation, tests all separated
   - Easy to find any file

2. **Scalability**
   - Easy to add more scripts, notebooks, or data files
   - Clear hierarchy

3. **Git-Friendly**
   - Logical .gitignore patterns
   - Data can be excluded if needed

4. **Professional Standard**
   - Follows industry best practices
   - Similar to production codebases

5. **Easy Navigation**
   - Intuitive folder names
   - Clear file purposes

6. **Maintenance**
   - Easy to update or replace components
   - Clear dependencies

---

## File Count Summary

| Category        | Count | Location            |
|-----------------|-------|---------------------|
| Data Files      | 8     | data/               |
| Scripts         | 3     | scripts/            |
| Notebooks       | 1     | notebooks/          |
| Visualizations  | 2     | visualizations/     |
| Documentation   | 4     | docs/               |
| Tests           | 6     | tests/              |
| Config          | 1     | config/             |
| Root Files      | 3     | ./                  |
| **Total**       | **28**|                     |

---

**Document Version:** 2.0
**Last Updated:** November 27, 2025
**Status:** Reorganized for Professional Structure
