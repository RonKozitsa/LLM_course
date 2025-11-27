# Multi-Stage Translation Quality Analysis System

A comprehensive framework for evaluating semantic preservation through multi-stage translation pipelines using vector embeddings and cosine similarity metrics.

## 🎯 Project Objective

This project measures how well semantic meaning is preserved when text undergoes multiple translation cycles across typologically different languages. The system translates English text through French and Hebrew intermediaries before returning to English, then quantifies the semantic drift to analyze translation quality and error resilience.

**Key Question**: Does the number of errors in the original text correlate with semantic degradation through a multi-stage translation pipeline?

## 📊 Overview

The system implements a three-stage translation pipeline:

```
English (with errors) → French → Hebrew → English (final)
```

Each translated output is then analyzed using sentence embeddings to measure semantic similarity between the original and final English text.

## 🏗️ Architecture

### Translation Pipeline

1. **Stage 1: English → French**
   - Agent: `EnglishToFrench`
   - Corrects spelling errors during translation
   - Applies Matthieussent-style literary translation
   - Produces natural, idiomatic French

2. **Stage 2: French → Hebrew**
   - Agent: `FrenchToHebrew`
   - Applies Ayalon-style literary translation
   - Handles RTL (right-to-left) formatting
   - Cultural mediation between French and Hebrew contexts

3. **Stage 3: Hebrew → English**
   - Agent: `HebrewToEnglish`
   - Applies Cohen-style literary translation
   - Produces natural, fluent English
   - Preserves meaning and tone from Hebrew source

### Analysis Engine

**Script**: `sentence_vector_comparison.py`

- Uses `all-MiniLM-L6-v2` sentence transformer model (384-dimensional embeddings)
- Calculates cosine similarity between original and final English sentences
- Groups sentences by error count and computes average similarities
- Generates statistical analysis and visualizations

## 📁 Project Structure

```
translation task/
├── English.csv                          # Input: 170 sentences with 4-20 spelling errors each
├── French.csv                           # Output from EnglishToFrench agent
├── Hebrew.csv                           # Output from FrenchToHebrew agent
├── English_final.csv                    # Output from HebrewToEnglish agent
├── sentence_vector_comparison.py        # Semantic analysis script
├── vector_similarity_results.csv        # Individual sentence comparisons (170 rows)
├── vector_similarity_averaged.csv       # Averaged results by error count (17 groups)
├── vector_similarity_vs_mistakes.png    # Visualization of results
├── tests/                              # Test suite (50+ tests)
│   ├── __init__.py                     # Test package initialization
│   ├── conftest.py                     # Pytest configuration
│   ├── test_sentence_vector_comparison.py  # Analysis script tests
│   ├── test_data_validation.py         # Data integrity tests
│   ├── requirements_test.txt           # Test dependencies
│   └── README.md                       # Test documentation
├── PRD.md                              # Product Requirements Document
└── README.md                           # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Claude Code CLI with agent support
- Minimum 4GB RAM (8GB recommended)

### Installation

1. **Install Python dependencies:**

```bash
pip install pandas numpy sentence-transformers scikit-learn matplotlib
```

Or using requirements file:

```bash
pip install -r requirements.txt
```

2. **Ensure translation agents are configured:**

The following agents must be available in your Claude Code environment:
- `EnglishToFrench`
- `FrenchToHebrew`
- `HebrewToEnglish`

### Usage

#### Step 1: Run Translation Pipeline

Execute the translation agents in sequence via Claude Code:

```
Run EnglishToFrench agent  → produces French.csv
Run FrenchToHebrew agent   → produces Hebrew.csv
Run HebrewToEnglish agent  → produces English_final.csv
```

#### Step 2: Run Semantic Analysis

```bash
python3 sentence_vector_comparison.py
```

**Output:**
- `vector_similarity_results.csv` - Individual sentence comparisons
- `vector_similarity_averaged.csv` - Grouped averages by error count
- `vector_similarity_vs_mistakes.png` - Visualization with error bars and trend line

**Custom file paths:**
```bash
python3 sentence_vector_comparison.py <input1.csv> <input2.csv> <output.png>
```

## 📈 Results

### Key Findings

| Metric                  | Value    |
|-------------------------|----------|
| Average Similarity      | 0.6891   |
| Correlation Coefficient | -0.540   |
| Min Similarity          | 0.4510   |
| Max Similarity          | 0.8793   |

**Interpretation**: Moderate negative correlation between error count and semantic similarity. While more errors tend to reduce semantic preservation, the effect is not deterministic, and the translation pipeline maintains reasonable semantic fidelity (avg 0.69) even with noisy input.

### Similarity by Error Count

| Errors | Avg Similarity | Std Dev |
|--------|----------------|---------|
| 4      | 0.7273         | 0.0942  |
| 5      | 0.6425         | 0.1029  |
| 10     | 0.6962         | 0.0583  |
| 15     | 0.6589         | 0.0671  |
| 20     | 0.6485         | 0.1088  |

## 🧪 Testing

The project includes a comprehensive test suite with 50+ unit and integration tests.

### Running Tests

**Install test dependencies:**
```bash
pip install -r tests/requirements_test.txt
```

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test categories:**
```bash
# Unit tests only (fast)
pytest tests/ -m unit -v

# Integration tests
pytest tests/ -m integration -v

# With coverage report
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

The test suite covers:
- ✅ CSV data loading and validation
- ✅ Translation pipeline data flow
- ✅ Vector encoding and similarity computation
- ✅ Statistical calculations (averaging, correlation)
- ✅ Output file generation and integrity
- ✅ Edge cases and error handling
- ✅ Performance benchmarks

**Coverage Target**: >80%

See `tests/README.md` for detailed test documentation.

## 🔍 Dataset Details

**Input Data (English.csv)**:
- **Total Sentences**: 170
- **Error Range**: 4-20 spelling mistakes per sentence
- **Distribution**: 10 sentences per error count (stratified sampling)
- **Format**: CSV with columns: `Index`, `text`, `mistakes`

**Sample Entry**:
```csv
Index,text,mistakes
1,"Under the silver moonlight, the thaveler unfolded his mat, searching fhr the hidden vallzy marked by.",4
```

## 🛠️ Technical Details

### Sentence Embedding

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding Dimensions**: 384
- **Framework**: SentenceTransformers
- **Optimization**: Pre-trained for semantic similarity tasks

### Similarity Metric

**Cosine Similarity**:
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

- **Range**: [0.0, 1.0]
- **Interpretation**:
  - 1.0 = Perfect semantic alignment
  - > 0.6 = Moderate to high similarity
  - < 0.5 = Low similarity

### Statistical Analysis

- **Grouping**: 10 sentences per error count (4-20 errors)
- **Metrics**: Mean, standard deviation, correlation coefficient
- **Visualization**: Scatter plot with error bars (±1 std dev) and linear trend line

## 📊 Visualization

The generated graph (`vector_similarity_vs_mistakes.png`) includes:

- **Scatter points**: Average similarity per error count
- **Error bars**: Standard deviation (vertical bars)
- **Trend line**: Linear regression showing correlation
- **Statistics box**: Overall avg, min, max, and group count
- **Resolution**: 300 DPI, 14" × 9" figure

## 🔬 Use Cases

1. **Translation Quality Assessment**: Benchmark translation systems for semantic fidelity
2. **Error Resilience Testing**: Determine impact of input quality on translation accuracy
3. **Multi-Language Pipeline Validation**: Test robustness of sequential translation
4. **Linguistic Research**: Study cross-linguistic semantic preservation
5. **Quality Assurance**: Automated testing for translation services

## 🧪 Methodology Highlights

### Why This Approach?

- **Multi-Stage Translation**: Tests real-world scenarios where text may be translated multiple times
- **Cross-Linguistic**: Uses typologically different languages (Indo-European ↔ Semitic)
- **Literary Quality**: High-quality translation agents ensure professional-grade output
- **Quantitative Metrics**: Vector embeddings provide objective semantic measurements
- **Statistical Rigor**: 10 samples per error count ensures meaningful averages

### Translation Quality Factors

1. **Error Correction**: First stage (English→French) normalizes errors
2. **Literary Translation**: Agents apply professional translation principles
3. **Cultural Mediation**: Each agent adapts content to target language context
4. **Semantic Focus**: Prioritizes meaning over literal word-for-word translation

## 📝 Outputs Explained

### vector_similarity_results.csv
Individual comparison for each of the 170 sentences:
```csv
Index,Mistakes,Cosine_Similarity,Original_Sentence,Final_Sentence
1,4,0.6830,"Under the silver moonlight...","Under the silver moonlight..."
```

### vector_similarity_averaged.csv
Grouped averages by error count (17 groups):
```csv
Mistakes,Avg_Similarity,Std_Dev,Count
4,0.7273,0.0942,10
5,0.6425,0.1029,10
```

### vector_similarity_vs_mistakes.png
Professional visualization showing:
- X-axis: Number of mistakes (4-20)
- Y-axis: Average cosine similarity (0.0-1.0)
- Data points with error bars
- Trend line with equation
- Statistics summary box

## 🔧 Configuration

The script can be customized by modifying `sentence_vector_comparison.py`:

- **Embedding Model**: Change `model = SentenceTransformer('all-MiniLM-L6-v2')` to use different models
- **Visualization Style**: Modify matplotlib configuration in visualization section
- **Statistical Methods**: Adjust grouping, correlation methods, or trend fitting

## ⚠️ Limitations

1. **Fixed Dataset**: Optimized for 170 sentences with specific error distribution
2. **Spelling Errors Only**: Does not test grammar or semantic errors
3. **English-Centric Metrics**: Similarity measured using English embeddings
4. **Sequential Execution**: Translation agents require manual invocation
5. **Model Dependency**: Results depend on chosen embedding model

## 📚 Dependencies

```
pandas>=1.3.0
numpy>=1.21.0
sentence-transformers>=2.2.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
```

## 🤝 Contributing

This project is designed as a research framework. Potential extensions:

- Additional language pairs (German, Spanish, Mandarin, etc.)
- Alternative embedding models (mpnet, roberta, etc.)
- Error type categorization (spelling, grammar, semantic)
- Human evaluation correlation studies
- Automated pipeline execution

## 📄 Documentation

For detailed technical specifications, see **PRD.md** (Product Requirements Document).

## 📞 Support

For questions about:
- **Translation Agents**: Check Claude Code agent configuration
- **Python Script**: Review `sentence_vector_comparison.py` comments
- **Methodology**: Consult PRD.md for in-depth technical details

## 🎓 References

**Sentence Transformers**:
- Reimers & Gurevych (2019): "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- Model: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

**Translation Principles**:
- Matthieussent Style: Natural French translation avoiding Anglicisms
- Ayalon Style: Literary Hebrew with cultural adaptation
- Cohen Style: Faithful English literary translation

---

## 📊 Quick Start Example

```bash
# 1. Ensure you have all CSV files from translation pipeline
ls *.csv
# Expected: English.csv, French.csv, Hebrew.csv, English_final.csv

# 2. Run analysis
python3 sentence_vector_comparison.py

# 3. View results
cat vector_similarity_averaged.csv
open vector_similarity_vs_mistakes.png
```

---

**Project Status**: ✅ Complete and Operational

**Version**: 1.0

**Last Updated**: November 27, 2025
