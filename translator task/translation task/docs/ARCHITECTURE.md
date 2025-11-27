# Architecture Documentation
## Multi-Stage Translation Quality Analysis System

**Version:** 2.0
**Last Updated:** November 27, 2025

---

## C4 Model Architecture Diagrams

This document presents the system architecture using the C4 model (Context, Container, Component, Code).

---

## Level 1: System Context Diagram

The System Context diagram shows how the Multi-Stage Translation Quality Analysis System fits into the world around it.

```mermaid
graph TB
    subgraph External
        User[👤 Researcher/Data Scientist]
        Claude[🤖 Claude AI<br/>Translation Agents]
        HuggingFace[🤗 Hugging Face<br/>Model Hub]
    end

    subgraph System[Multi-Stage Translation Quality Analysis System]
        MTQAS[Translation Quality<br/>Analysis System]
    end

    User -->|Provides error-injected<br/>English sentences| MTQAS
    User -->|Runs analysis scripts| MTQAS
    User -->|Reviews results<br/>and visualizations| MTQAS

    MTQAS -->|Requests translations| Claude
    Claude -->|Returns translated text<br/>English→French→Hebrew→English| MTQAS

    MTQAS -->|Downloads sentence<br/>embedding models| HuggingFace
    HuggingFace -->|Provides transformer models<br/>all-MiniLM-L6-v2, etc.| MTQAS

    MTQAS -->|Generates statistical<br/>reports & visualizations| User

    style System fill:#e1f5ff
    style MTQAS fill:#4fc3f7
    style User fill:#ffeb3b
    style Claude fill:#9c27b0,color:#fff
    style HuggingFace fill:#ff9800
```

**Key Interactions:**
- **User**: Provides input data (English sentences with errors) and executes analysis pipelines
- **Claude AI**: Performs multi-stage translations through specialized agents
- **Hugging Face**: Provides pre-trained sentence transformer models for semantic similarity
- **System**: Orchestrates translation, embedding, similarity calculation, and statistical analysis

---

## Level 2: Container Diagram

The Container diagram shows the high-level technical building blocks of the system.

```mermaid
graph TB
    subgraph External
        User[👤 User]
        Claude[🤖 Claude AI]
        HF[🤗 Hugging Face]
    end

    subgraph System[Multi-Stage Translation Quality Analysis System]
        subgraph Data[📁 Data Layer]
            Input[(Input Data<br/>CSV)]
            Intermediate[(Intermediate<br/>Translations<br/>CSV)]
            Output[(Analysis Results<br/>CSV + TXT)]
        end

        subgraph Analysis[🔬 Analysis Scripts]
            SentVec[Sentence Vector<br/>Comparison<br/>Python Script]
            StatAnalysis[Statistical Analysis<br/>Enhanced<br/>Python Script]
            CompModel[Comparative Model<br/>Analysis<br/>Python Script]
        end

        subgraph Agents[🤖 Translation Agents]
            EnFr[EnglishToFrench<br/>Agent]
            FrHe[FrenchToHebrew<br/>Agent]
            HeEn[HebrewToEnglish<br/>Agent]
        end

        subgraph Visualization[📊 Visualization]
            Plots[PNG Plots<br/>matplotlib]
        end

        subgraph Notebooks[📓 Interactive Analysis]
            Jupyter[Jupyter Notebook<br/>EDA & Analysis]
        end

        subgraph Config[⚙️ Configuration]
            ConfigYAML[config.yaml<br/>Parameters]
        end
    end

    User -->|1. Provides CSV<br/>English.csv| Input
    Input -->|2. Reads sentences| EnFr
    EnFr -->|Translates| Claude
    Claude -->|Returns French| Intermediate

    Intermediate -->|3. French sentences| FrHe
    FrHe -->|Translates| Claude
    Claude -->|Returns Hebrew| Intermediate

    Intermediate -->|4. Hebrew sentences| HeEn
    HeEn -->|Translates| Claude
    Claude -->|Returns English| Output

    Input -->|5. Original text| SentVec
    Output -->|6. Final text| SentVec
    SentVec -->|Downloads models| HF
    HF -->|all-MiniLM-L6-v2| SentVec
    SentVec -->|Calculates similarity| Output
    SentVec -->|Generates plots| Plots

    Output -->|7. Reads results| StatAnalysis
    StatAnalysis -->|Statistical tests<br/>ANOVA, CIs| Output

    Output -->|8. Reads results| CompModel
    CompModel -->|Downloads 4 models| HF
    CompModel -->|Model comparison| Output

    ConfigYAML -.->|Parameters| SentVec
    ConfigYAML -.->|Parameters| StatAnalysis
    ConfigYAML -.->|Parameters| CompModel

    Output -->|9. View reports| User
    Plots -->|10. View visualizations| User
    Jupyter -->|11. Interactive analysis| User

    style System fill:#e1f5ff
    style Data fill:#fff9c4
    style Analysis fill:#c8e6c9
    style Agents fill:#d1c4e9
    style Visualization fill:#ffccbc
    style Notebooks fill:#b2dfdb
    style Config fill:#f8bbd0
```

**Container Descriptions:**

### 1. Data Layer (CSV Files)
- **Input**: `English.csv` - 170 sentences with 4-20 spelling errors
- **Intermediate**: `French.csv`, `Hebrew.csv` - Translation pipeline outputs
- **Output**: `English_final.csv`, results CSVs, statistical reports

### 2. Translation Agents (Claude AI Integration)
- **EnglishToFrench**: Corrects errors, translates to French (Matthieussent style)
- **FrenchToHebrew**: Translates to Hebrew with RTL formatting (Ayalon style)
- **HebrewToEnglish**: Translates back to English (Cohen style)

### 3. Analysis Scripts (Python)
- **sentence_vector_comparison.py**:
  - Loads sentence transformer models from Hugging Face
  - Encodes sentences into 384-dimensional vectors
  - Calculates cosine similarity
  - Groups by error count and computes averages

- **statistical_analysis_enhanced.py**:
  - Hypothesis testing (H0/H1, p-values)
  - 95% confidence intervals
  - ANOVA with Tukey HSD post-hoc
  - Effect size calculations (η², Cohen's d)
  - Normality tests

- **comparative_model_analysis.py**:
  - Tests 4 different embedding models
  - Baseline identity comparison
  - Model performance metrics

### 4. Visualization (matplotlib)
- Scatter plots with error bars
- Trend lines and regression
- Model comparison charts
- 300 DPI publication-quality images

### 5. Interactive Analysis (Jupyter)
- Exploratory Data Analysis (EDA)
- 10+ interactive visualizations
- Step-by-step statistical walkthrough

### 6. Configuration (YAML)
- Centralized parameter management
- Model selections
- Statistical parameters (α, confidence levels)
- File paths

---

## Level 3: Component Diagram (Analysis Scripts)

### Sentence Vector Comparison Components

```mermaid
graph TB
    subgraph SentVecScript[sentence_vector_comparison.py]
        Main[main function]

        subgraph DataLoad[Data Loading]
            LoadCSV1[Load English.csv]
            LoadCSV2[Load English_final.csv]
            SortData[Sort by Index]
            CleanData[Remove empty rows]
        end

        subgraph Encoding[Vector Encoding]
            LoadModel[Load SentenceTransformer<br/>all-MiniLM-L6-v2]
            Encode1[Encode original sentences]
            Encode2[Encode final sentences]
        end

        subgraph Similarity[Similarity Calculation]
            CalcSim[Calculate cosine<br/>similarity pairwise]
            GroupMistakes[Group by mistake count]
            CalcAvg[Calculate mean & std<br/>per group]
        end

        subgraph Visualization[Visualization]
            CreatePlot[Create scatter plot]
            AddErrorBars[Add error bars]
            AddTrend[Add trend line]
            AddStats[Add statistics box]
            SavePNG[Save PNG at 300 DPI]
        end

        subgraph Output[Output Generation]
            SaveResults[Save individual results<br/>vector_similarity_results.csv]
            SaveAveraged[Save averaged results<br/>vector_similarity_averaged.csv]
        end
    end

    Main --> LoadCSV1
    Main --> LoadCSV2
    LoadCSV1 --> SortData
    LoadCSV2 --> SortData
    SortData --> CleanData

    CleanData --> LoadModel
    LoadModel --> Encode1
    LoadModel --> Encode2

    Encode1 --> CalcSim
    Encode2 --> CalcSim
    CalcSim --> GroupMistakes
    GroupMistakes --> CalcAvg

    CalcAvg --> CreatePlot
    CreatePlot --> AddErrorBars
    AddErrorBars --> AddTrend
    AddTrend --> AddStats
    AddStats --> SavePNG

    CalcSim --> SaveResults
    CalcAvg --> SaveAveraged

    style SentVecScript fill:#c8e6c9
    style DataLoad fill:#fff9c4
    style Encoding fill:#bbdefb
    style Similarity fill:#f8bbd0
    style Visualization fill:#ffccbc
    style Output fill:#d1c4e9
```

### Statistical Analysis Components

```mermaid
graph TB
    subgraph StatAnalysis[statistical_analysis_enhanced.py]
        Analyzer[EnhancedStatisticalAnalyzer<br/>Class]

        subgraph HypTest[Hypothesis Testing]
            Pearson[Pearson correlation]
            Spearman[Spearman correlation]
            PValue[Calculate p-values]
            Decision[H0 decision:<br/>reject or fail to reject]
        end

        subgraph CI[Confidence Intervals]
            FisherZ[Fisher's z-transformation]
            CICorr[95% CI for correlation]
            CIGroups[CIs for group means]
        end

        subgraph ANOVA[ANOVA Analysis]
            OneWay[One-way ANOVA]
            FStatistic[F-statistic]
            EffectSize[Effect size η²]
            Tukey[Tukey HSD post-hoc]
        end

        subgraph EffectCalc[Effect Size]
            CohenD[Cohen's d<br/>4 vs 20 errors]
            RSquared[R² calculation]
        end

        subgraph Normality[Normality Tests]
            Shapiro[Shapiro-Wilk test]
            KS[Kolmogorov-Smirnov test]
        end

        subgraph Report[Report Generation]
            Compile[Compile all results]
            Format[Format as text report]
            Save[Save to<br/>statistical_analysis_report.txt]
        end
    end

    Analyzer --> HypTest
    Analyzer --> CI
    Analyzer --> ANOVA
    Analyzer --> EffectCalc
    Analyzer --> Normality

    HypTest --> Report
    CI --> Report
    ANOVA --> Report
    EffectCalc --> Report
    Normality --> Report

    Report --> Compile
    Compile --> Format
    Format --> Save

    style StatAnalysis fill:#c8e6c9
    style HypTest fill:#fff9c4
    style CI fill:#bbdefb
    style ANOVA fill:#f8bbd0
    style EffectCalc fill:#ffccbc
    style Normality fill:#d1c4e9
    style Report fill:#b2dfdb
```

---

## Data Flow Architecture

### Translation Pipeline Flow

```mermaid
sequenceDiagram
    participant User
    participant EnFr as EnglishToFrench Agent
    participant Claude as Claude AI
    participant FrHe as FrenchToHebrew Agent
    participant HeEn as HebrewToEnglish Agent
    participant Data as Data Storage

    User->>Data: Provide English.csv<br/>(170 sentences, 4-20 errors)

    Note over EnFr,Claude: Stage 1: Error Correction + Translation
    Data->>EnFr: Read English.csv
    EnFr->>Claude: Request translation (Matthieussent style)
    Claude->>EnFr: Return French translations
    EnFr->>Data: Save French.csv

    Note over FrHe,Claude: Stage 2: Cross-linguistic Transfer
    Data->>FrHe: Read French.csv
    FrHe->>Claude: Request translation (Ayalon style, RTL)
    Claude->>FrHe: Return Hebrew translations
    FrHe->>Data: Save Hebrew.csv

    Note over HeEn,Claude: Stage 3: Back-translation
    Data->>HeEn: Read Hebrew.csv
    HeEn->>Claude: Request translation (Cohen style)
    Claude->>HeEn: Return English translations
    HeEn->>Data: Save English_final.csv

    Data->>User: Pipeline complete<br/>4 CSV files generated
```

### Analysis Pipeline Flow

```mermaid
sequenceDiagram
    participant User
    participant SentVec as sentence_vector_comparison.py
    participant HF as Hugging Face
    participant StatAnalysis as statistical_analysis_enhanced.py
    participant Viz as Visualizations

    User->>SentVec: Execute analysis script

    Note over SentVec,HF: Model Loading
    SentVec->>HF: Request all-MiniLM-L6-v2
    HF->>SentVec: Return model (384 dimensions)

    Note over SentVec: Vector Encoding
    SentVec->>SentVec: Encode English.csv
    SentVec->>SentVec: Encode English_final.csv

    Note over SentVec: Similarity Calculation
    SentVec->>SentVec: Calculate cosine similarity (170 pairs)
    SentVec->>SentVec: Group by mistake count (17 groups)
    SentVec->>SentVec: Calculate averages & std dev

    Note over SentVec,Viz: Output Generation
    SentVec->>Data: Save vector_similarity_results.csv
    SentVec->>Data: Save vector_similarity_averaged.csv
    SentVec->>Viz: Generate scatter plot with error bars
    SentVec->>User: Analysis complete (correlation = -0.19)

    Note over StatAnalysis: Statistical Testing
    User->>StatAnalysis: Execute statistical analysis
    StatAnalysis->>Data: Read results CSV
    StatAnalysis->>StatAnalysis: Hypothesis testing (p = 0.012)
    StatAnalysis->>StatAnalysis: Confidence intervals (95% CI)
    StatAnalysis->>StatAnalysis: ANOVA (F = 1.38, p = 0.16)
    StatAnalysis->>StatAnalysis: Effect size (η² = 12.6%)
    StatAnalysis->>StatAnalysis: Normality tests (Shapiro-Wilk)
    StatAnalysis->>Data: Save statistical_analysis_report.txt
    StatAnalysis->>User: Statistical analysis complete
```

---

## Technology Stack

```mermaid
graph TB
    subgraph Languages[Programming Languages]
        Python[Python 3.9+]
    end

    subgraph ML[Machine Learning & NLP]
        SentenceTransformers[sentence-transformers<br/>Sentence embeddings]
        SkLearn[scikit-learn<br/>Cosine similarity]
        HuggingFace[Hugging Face Transformers<br/>Model hub]
    end

    subgraph Stats[Statistical Libraries]
        SciPy[scipy<br/>Statistical tests]
        StatsModels[statsmodels<br/>ANOVA, Tukey HSD]
    end

    subgraph DataViz[Data & Visualization]
        Pandas[pandas<br/>Data manipulation]
        NumPy[numpy<br/>Numerical computing]
        Matplotlib[matplotlib<br/>Plotting]
        Seaborn[seaborn<br/>Statistical plots]
        Jupyter[Jupyter<br/>Interactive notebooks]
    end

    subgraph AIAgents[AI Integration]
        ClaudeAPI[Claude AI<br/>Translation agents]
    end

    subgraph Config[Configuration]
        YAML[PyYAML<br/>Config management]
    end

    subgraph Testing[Testing & QA]
        Pytest[pytest<br/>Test framework]
        PytestCov[pytest-cov<br/>Coverage reporting]
    end

    Python --> SentenceTransformers
    Python --> SkLearn
    Python --> SciPy
    Python --> StatsModels
    Python --> Pandas
    Python --> NumPy
    Python --> Matplotlib
    Python --> Seaborn
    Python --> Jupyter
    Python --> ClaudeAPI
    Python --> YAML
    Python --> Pytest

    style Languages fill:#4fc3f7
    style ML fill:#c8e6c9
    style Stats fill:#fff9c4
    style DataViz fill:#ffccbc
    style AIAgents fill:#d1c4e9
    style Config fill:#f8bbd0
    style Testing fill:#b2dfdb
```

---

## Deployment View

```mermaid
graph TB
    subgraph DevEnv[Development Environment]
        LocalMachine[👨‍💻 Local Machine<br/>macOS/Linux/Windows]

        subgraph Python[Python Environment]
            Venv[Virtual Environment<br/>venv/]
            Dependencies[Dependencies<br/>requirements.txt]
        end

        subgraph ProjectStructure[Project Structure]
            Config[config/]
            Data[data/<br/>input/intermediate/output]
            Scripts[scripts/]
            Notebooks[notebooks/]
            Tests[tests/]
            Docs[docs/]
            Viz[visualizations/]
        end
    end

    subgraph External[External Services]
        HFHub[🤗 Hugging Face Hub<br/>Model storage]
        ClaudeService[🤖 Claude AI API<br/>Translation service]
    end

    LocalMachine --> Venv
    Venv --> Dependencies
    Dependencies --> Scripts

    Scripts <-->|Download models<br/>~500MB cache| HFHub
    Scripts <-->|API calls<br/>~88K tokens| ClaudeService

    Scripts --> Data
    Scripts --> Viz
    Notebooks --> Data
    Tests --> Scripts

    Config -.-> Scripts
    Config -.-> Notebooks

    style DevEnv fill:#e1f5ff
    style Python fill:#ffeb3b
    style ProjectStructure fill:#c8e6c9
    style External fill:#ffccbc
```

---

## Key Architecture Decisions

### 1. Multi-Agent Translation Pipeline
**Decision**: Use three separate specialized translation agents instead of one general-purpose agent
**Rationale**:
- Each agent applies specific translation style (Matthieussent, Ayalon, Cohen)
- Better control over error correction timing (Stage 1 only)
- Cultural mediation at each stage
- Clear separation of concerns

### 2. Sentence Transformers for Embeddings
**Decision**: Use `sentence-transformers/all-MiniLM-L6-v2` as primary model
**Rationale**:
- 384-dimensional embeddings (good balance size/performance)
- Fast inference (~100 sentences/second)
- Pre-trained on semantic similarity tasks
- Small model size (~90MB)

### 3. Averaged Group Analysis
**Decision**: Group 10 sentences per error count and report averages
**Rationale**:
- Reduces noise from individual outliers
- Stratified sampling ensures balanced representation
- Statistical power with n=10 per group
- Clearer trend visualization

### 4. Comprehensive Statistical Testing
**Decision**: Include hypothesis testing, CIs, ANOVA, effect sizes
**Rationale**:
- Academic rigor for research publication
- Multiple validation approaches
- Effect size provides practical significance
- Meets university grading criteria (95+)

### 5. CSV-Based Data Pipeline
**Decision**: Use CSV files for all data storage
**Rationale**:
- Human-readable and editable
- Excel compatibility for stakeholders
- Simple backup and version control
- No database dependencies

### 6. Folder-Based Organization
**Decision**: Organize into `config/`, `data/`, `scripts/`, `notebooks/`, `docs/`, `tests/`, `visualizations/`
**Rationale**:
- Industry best practice
- Clear separation of concerns
- Scalable for future additions
- Easy navigation for new contributors

---

## Performance Characteristics

### Translation Pipeline
- **Throughput**: 170 sentences in ~20 minutes
- **Token Usage**: ~88,740 tokens ($0.40 with Sonnet)
- **Bottleneck**: API calls to Claude AI

### Analysis Pipeline
- **Sentence Encoding**: ~5 seconds for 340 sentences
- **Similarity Calculation**: <1 second for 170 pairs
- **Statistical Analysis**: ~2 seconds
- **Bottleneck**: Model loading from disk (first time: ~3 seconds)

### Storage Requirements
- **Models**: ~500MB (cached from Hugging Face)
- **Data**: ~2MB (CSV files)
- **Outputs**: ~5MB (plots, reports)
- **Total**: ~507MB

---

## Security Considerations

1. **API Keys**: Not hardcoded, managed externally
2. **Secrets**: `.gitignore` excludes `.env`, `credentials.json`
3. **Data Privacy**: All data processed locally (except Claude API calls)
4. **Model Provenance**: All models from verified Hugging Face sources

---

## Scalability Considerations

### Current Scale
- 170 sentences
- 17 error count groups
- 4 translation stages

### Scaling Options
1. **Horizontal**: Batch processing with multiprocessing
2. **Data**: Can handle 10K+ sentences with same architecture
3. **Languages**: Modular design supports adding new language pairs
4. **Models**: Comparative analysis framework supports N models

---

**Document Status**: ✅ Complete
**Last Review**: November 27, 2025
**Next Review**: Quarterly or upon major architecture changes
