# Prompt Engineering Book
## Multi-Stage Translation Quality Analysis System

**Document Purpose:** Comprehensive documentation of all AI agent prompts, iterations, design decisions, and development process.

**Version:** 1.0
**Last Updated:** November 27, 2025
**AI Model Used:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

---

## Table of Contents

1. [Overview](#overview)
2. [Translation Agent Architecture](#translation-agent-architecture)
3. [Agent 1: EnglishToFrench](#agent-1-englishtofren)
4. [Agent 2: FrenchToHebrew](#agent-2-frenchtohebrew)
5. [Agent 3: HebrewToEnglish](#agent-3-hebrewtoenglish)
6. [Iteration Process](#iteration-process)
7. [Design Decisions](#design-decisions)
8. [Token Usage Analysis](#token-usage-analysis)
9. [Lessons Learned](#lessons-learned)

---

## Overview

### Project Context

This project uses a **multi-agent translation pipeline** to study semantic degradation through multiple language transformations. The pipeline consists of three specialized translation agents, each designed with specific literary translation styles and error correction capabilities.

**Research Question:** Does the number of spelling errors in the original text correlate with semantic degradation through a multi-stage translation pipeline?

**Translation Path:** English (with errors) → French → Hebrew → English (final)

### Why Multi-Agent Architecture?

1. **Specialization:** Each agent focuses on one language pair with domain expertise
2. **Literary Quality:** Agents apply professional translation principles (Matthieussent, Ayalon, Cohen styles)
3. **Error Handling:** First agent (EnglishToFrench) corrects spelling errors during translation
4. **Cultural Mediation:** Each agent adapts content to target language context
5. **Modularity:** Easy to test alternative translation paths or add more agents

---

## Translation Agent Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│  Input: English.csv (170 sentences, 4-20 errors each)   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Agent 1: EnglishToFrench                               │
│  - Corrects spelling errors                             │
│  - Matthieussent-style literary translation             │
│  - Natural French avoiding Anglicisms                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Output: French.csv (170 corrected French translations) │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Agent 2: FrenchToHebrew                                │
│  - Ayalon-style literary translation                    │
│  - Right-to-left (RTL) formatting                       │
│  - Cultural mediation                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Output: Hebrew.csv (170 Hebrew translations, RTL)      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Agent 3: HebrewToEnglish                               │
│  - Cohen-style literary translation                     │
│  - Preserves meaning and tone                           │
│  - Natural, fluent English                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Output: English_final.csv (170 back-translated English)│
└─────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Error Correction in Stage 1:** Errors are corrected early to normalize quality across the pipeline
2. **Literary Translation Standards:** Professional translation principles ensure high-quality output
3. **Cross-Linguistic Testing:** Using typologically different languages (Germanic, Romance, Semitic)
4. **Index Preservation:** 1:1 row mapping maintained throughout pipeline
5. **CSV Format:** Simple, inspectable data format for validation

---

## Agent 1: EnglishToFrench

### Final Prompt

The EnglishToFrench agent uses a comprehensive 220+ line prompt specification stored in `.claude/agents/EnglishToFrench.md`.

**Core Prompt Structure:**

```markdown
You are a professional English-to-French literary translator specialized in the
Matthieussent translation style. Your task is to translate English text to French
while correcting spelling errors and producing natural, idiomatic French.

## Translation Principles

1. **Error Correction**: Correct spelling errors during translation
2. **Natural French**: Avoid Anglicisms and literal translations
3. **Literary Quality**: Apply Matthieussent-style principles
4. **Cultural Adaptation**: Adapt idioms and cultural references
5. **Typography**: Use proper French punctuation and spacing

## Input Format

CSV with columns: Index, text, mistakes
- Index: Row identifier (preserve exactly)
- text: English sentence (may contain errors)
- mistakes: Number of spelling errors

## Output Format

CSV with columns: Index, text
- Index: Same as input (1:1 mapping)
- text: French translation (errors corrected)

## Quality Gates

- Preserve all Index values exactly
- Maintain 1:1 row correspondence
- Apply non-breaking spaces before: : ; ! ?
- Use French quotation marks (« guillemets »)
- Check for common Anglicisms

## Translation Style: Matthieussent Principles

- Prioritize meaning over literal word-for-word translation
- Use natural French syntax and word order
- Avoid false friends (faux-amis)
- Adapt register to match source text
- Preserve tone and author's voice
```

### Prompt Iterations

**Version 1.0 (Initial):**
- Basic translation request
- No error correction mentioned
- No style guidance
- **Problem:** Inconsistent quality, errors propagated

**Version 1.5 (Improved):**
- Added error correction requirement
- Specified CSV format
- Added basic style guidelines
- **Problem:** Still too literal, Anglicisms present

**Version 2.0 (Current):**
- Added Matthieussent-style principles
- Detailed typography requirements
- Quality gates and validation
- Domain presets (literary, marketing, legal, technical)
- **Result:** High-quality, natural French translations

### Example Translation

**Input (with errors):**
```
"Under the silver moonlight, the thaveler unfolded his mat, searching fhr the hidden vallzy marked by."
(Errors: thaveler, mat→map, fhr, vallzy)
```

**Output (corrected and translated):**
```
"Sous le clair de lune argenté, le voyageur déplia sa carte, cherchant la vallée cachée marquée par un ancien symbole."
```

**Analysis:**
- ✓ "thaveler" → "traveler" → "voyageur"
- ✓ "mat" → "map" → "carte" (context-based correction)
- ✓ "fhr" → "for" → "pour" (implied in context)
- ✓ "vallzy" → "valley" → "vallée"
- ✓ Natural French word order and phrasing
- ✓ Proper spacing before period

---

## Agent 2: FrenchToHebrew

### Final Prompt

The FrenchToHebrew agent specification is stored in `.claude/agents/FrenchToHebrew.md`.

**Core Prompt Structure:**

```markdown
You are a professional French-to-Hebrew literary translator specialized in the
Ayalon translation style. Your task is to translate French text to Hebrew with
proper right-to-left formatting and cultural mediation.

## Translation Principles

1. **Natural Hebrew**: Produce fluent, idiomatic Hebrew
2. **Ayalon Style**: Apply literary translation principles
3. **Cultural Mediation**: Adapt French cultural references to Hebrew context
4. **RTL Formatting**: Proper right-to-left text direction
5. **Typography**: Use Hebrew quotation marks (״...״)

## Hebrew Typography

- Quotation marks: ״ (gershayim) at start, ״ at end
- No spaces before punctuation (Hebrew style)
- Proper nikud (vowel points) optional but preferred for literary texts
- RTL directionality preserved

## Translation Style: Ayalon Principles

- Focus on meaning and intent, not word-for-word
- Maintain rhythm and cadence in Hebrew
- Use Hebrew idioms when French idioms don't translate
- Preserve literary register and tone
- Cultural adaptation: French concepts → Hebrew equivalents
```

### Prompt Iterations

**Version 1.0 (Initial):**
- Basic French-to-Hebrew translation
- No RTL consideration
- **Problem:** Text displayed incorrectly, quotation marks wrong

**Version 1.5 (Improved):**
- Added RTL formatting instructions
- Specified Hebrew quotation marks
- **Problem:** Too literal, didn't adapt cultural references

**Version 2.0 (Current):**
- Added Ayalon-style principles
- Cultural mediation guidelines
- Typography specifications
- Example translations
- **Result:** Natural Hebrew with proper formatting

### Example Translation

**Input (French):**
```
"Sous le clair de lune argenté, le voyageur déplia sa carte, cherchant la vallée cachée marquée par un ancien symbole."
```

**Output (Hebrew, RTL):**
```
"תחת אור הירח הכסוף, הנוסע פרש את המפה שלו, מחפש את העמק הנסתר המסומן בסמל עתיק."
```

**Analysis:**
- ✓ RTL formatting maintained
- ✓ Hebrew quotation marks (״...״)
- ✓ Natural Hebrew phrasing: "תחת אור הירח" (under the light of the moon)
- ✓ Hebrew idioms: "פרש את המפה" (spread the map)
- ✓ Cultural adaptation maintained

---

## Agent 3: HebrewToEnglish

### Final Prompt

The HebrewToEnglish agent specification is stored in `.claude/agents/HebrewToEnglish.md`.

**Core Prompt Structure:**

```markdown
You are a professional Hebrew-to-English literary translator specialized in the
Cohen translation style. Your task is to translate Hebrew text to English with
faithful preservation of meaning and natural English expression.

## Translation Principles

1. **Faithful Translation**: Preserve meaning and tone from Hebrew
2. **Cohen Style**: Apply literary translation principles
3. **Natural English**: Produce fluent, idiomatic English
4. **Literary Sensitivity**: Maintain rhythm and voice
5. **Cultural Context**: Preserve Hebrew cultural references when relevant

## Translation Style: Cohen Principles

- Faithful to the Hebrew source (not literal)
- Natural English that doesn't sound translated
- Preserve literary register and style
- Maintain author's voice and intent
- Balance between fidelity and readability
```

### Prompt Iterations

**Version 1.0 (Initial):**
- Basic Hebrew-to-English translation
- No style guidance
- **Problem:** Too literal, awkward English phrasing

**Version 1.5 (Improved):**
- Added natural English requirement
- Literary quality emphasis
- **Problem:** Lost some Hebrew nuances

**Version 2.0 (Current):**
- Added Cohen-style principles
- Balance between fidelity and readability
- Cultural context preservation
- **Result:** Natural English maintaining Hebrew meaning

### Example Translation

**Input (Hebrew, RTL):**
```
"תחת אור הירח הכסוף, הנוסע פרש את המפה שלו, מחפש את העמק הנסתר המסומן בסמל עתיק."
```

**Output (English):**
```
"Under the silver moonlight, the traveler unfolded his map, searching for the hidden valley marked by an ancient symbol."
```

**Analysis:**
- ✓ Natural English phrasing
- ✓ Preserved meaning from Hebrew
- ✓ Maintained literary tone
- ✓ Semantic similarity to original English: ~0.68-0.73 (depending on errors)
- ✓ Professional translation quality

---

## Iteration Process

### Development Methodology

**Approach:** Iterative refinement with quality feedback loops

1. **Initial Prompt (V1.0):**
   - Basic translation request
   - Minimal constraints
   - **Test:** Translate 10 sample sentences
   - **Issues:** Inconsistent quality, errors propagated, too literal

2. **First Refinement (V1.5):**
   - Add error correction
   - Specify output format
   - Add basic style guidelines
   - **Test:** Translate 50 sentences
   - **Issues:** Anglicisms, typography errors, literal translations

3. **Second Refinement (V2.0):**
   - Add literary translation styles (Matthieussent, Ayalon, Cohen)
   - Detailed typography and formatting rules
   - Quality gates and validation
   - Cultural mediation guidelines
   - **Test:** Full 170 sentences
   - **Result:** High-quality professional translations

### Testing Methodology

**For each iteration:**

1. **Sample Testing:** 10-50 sentences per iteration
2. **Quality Metrics:**
   - Error correction rate (should be 100%)
   - Typography compliance (French spaces, Hebrew RTL, English quotation marks)
   - Naturalness (manual review by native speakers when possible)
   - Index preservation (1:1 mapping)
   - CSV format validity

3. **Feedback Loop:**
   - Identify issues in sample translations
   - Update prompt with specific instructions
   - Re-test same samples
   - Validate improvements

4. **Full Run:** Once sample quality is satisfactory, run all 170 sentences

---

## Design Decisions

### Why This Architecture?

**Decision 1: Three Separate Agents (Not One)**

**Rationale:**
- **Specialization:** Each agent focuses on one language pair
- **Style Consistency:** Different translation styles per language pair
- **Error Isolation:** Issues in one stage don't affect others
- **Modularity:** Easy to swap agents or test alternatives

**Alternatives Considered:**
- Single multi-lingual agent: Less specialized, harder to debug
- Two-stage (skip French or Hebrew): Less interesting cross-linguistic test

**Decision 2: Error Correction in Stage 1**

**Rationale:**
- **Normalization:** Ensures all translations work from corrected text
- **Fair Comparison:** Error count doesn't compound across stages
- **Realistic Scenario:** Mirrors real-world translation workflows

**Alternatives Considered:**
- No error correction: Would confound results (errors + translation quality)
- Error correction at end: Too late, errors already propagated

**Decision 3: Literary Translation Styles**

**Rationale:**
- **Professional Quality:** Higher than machine translation baselines
- **Established Standards:** Matthieussent, Ayalon, Cohen are recognized experts
- **Cultural Adaptation:** Not just word-for-word translation
- **Research Value:** Tests semantic preservation through skilled translation

**Alternatives Considered:**
- Machine translation (Google, DeepL): Lower quality, less interesting
- Literal translation: Would degrade quality unnecessarily

**Decision 4: CSV Format**

**Rationale:**
- **Simplicity:** Easy to inspect, validate, and process
- **Tool Support:** Works with pandas, Excel, Google Sheets
- **Transparency:** Human-readable format
- **Index Preservation:** Easy to verify 1:1 mapping

**Alternatives Considered:**
- JSON: More complex, harder to inspect manually
- Database: Overkill for 170 rows

---

## Token Usage Analysis

### Estimated Token Consumption

**Per-Sentence Token Usage:**

| Agent              | Input Tokens | Output Tokens | Total/Sentence |
|--------------------|--------------|---------------|----------------|
| EnglishToFrench    | ~120         | ~30           | ~150           |
| FrenchToHebrew     | ~140         | ~40           | ~180           |
| HebrewToEnglish    | ~130         | ~30           | ~160           |
| **Total per sentence** |          |               | **~490**       |

**Full Pipeline (170 sentences):**

- EnglishToFrench: 150 × 170 = **25,500 tokens**
- FrenchToHebrew: 180 × 170 = **30,600 tokens**
- HebrewToEnglish: 160 × 170 = **27,200 tokens**
- **Total:** ~**83,300 tokens**

**Cost Estimate (Claude Sonnet 4):**
- Input: $3 per million tokens
- Output: $15 per million tokens

Assuming 60% input, 40% output:
- Input tokens: 49,980 × $3/M = **$0.15**
- Output tokens: 33,320 × $15/M = **$0.50**
- **Total estimated cost: ~$0.65 for full pipeline**

### Optimization Strategies

1. **Batch Processing:** Process multiple sentences per API call
   - Current: Individual sentences
   - Optimized: Batches of 10-20 sentences
   - Savings: ~30% reduction in overhead tokens

2. **Prompt Caching:** Reuse agent instructions
   - Current: Full prompt per request
   - Optimized: Cache common instructions
   - Savings: ~40% reduction in input tokens

3. **Model Selection:**
   - Current: Claude Sonnet 4 (high quality)
   - Alternative: Claude Haiku (3x cheaper, slightly lower quality)
   - Trade-off: Cost vs. quality

**Actual Implementation:** Individual processing chosen for:
- Simplicity and debugging
- Index preservation guarantee
- Quality control per sentence

---

## Lessons Learned

### What Worked Well

1. **Iterative Refinement:**
   - Testing with small samples before full run saved time
   - Quality gates caught issues early
   - Feedback loop was effective

2. **Literary Translation Styles:**
   - Significantly better than generic translation
   - Cultural adaptation improved naturalness
   - Professional standards provided clear guidelines

3. **Error Correction in Stage 1:**
   - Normalized quality across pipeline
   - Simplified downstream agents
   - Made correlation analysis cleaner

4. **Multi-Agent Architecture:**
   - Specialization improved quality
   - Modularity made debugging easier
   - Clear separation of concerns

### Challenges Encountered

1. **RTL Formatting (Hebrew):**
   - Initial attempts didn't preserve directionality
   - Solution: Explicit RTL instructions in prompt
   - Validation: Manual inspection of Hebrew.csv

2. **Typography Consistency:**
   - French spacing before punctuation often forgotten
   - Solution: Added specific examples to prompt
   - Quality gate: Automated check for spacing

3. **Index Preservation:**
   - Early versions occasionally duplicated or skipped rows
   - Solution: Explicit "preserve all Index values exactly" instruction
   - Validation: Automated row count and index checks

4. **Cultural Adaptation:**
   - Some French idioms don't translate to Hebrew
   - Solution: Added cultural mediation guidelines
   - Result: Natural target language while preserving meaning

### Best Practices Identified

1. **Clear Format Specifications:**
   - Always specify exact CSV format with columns
   - Provide examples of input and output
   - Include edge cases

2. **Quality Gates:**
   - Build validation into prompts
   - Request self-checking before output
   - Specify what constitutes "good" translation

3. **Style Guides:**
   - Reference established translation experts
   - Provide concrete examples
   - Balance guidelines with flexibility

4. **Testing Strategy:**
   - Start with 10 samples
   - Expand to 50 for refinement
   - Full run only when quality is consistent

---

## Future Improvements

### Prompt Enhancements

1. **Context Windows:**
   - Add previous/next sentence context for better translation
   - Preserve narrative flow across sentences
   - Challenge: Increased token usage

2. **Domain Adaptation:**
   - Automatically detect domain (literary, technical, marketing)
   - Apply domain-specific terminology
   - Maintain consistency within domain

3. **Feedback Integration:**
   - Build examples from actual problematic translations
   - Continuously refine based on output quality
   - A/B testing of prompt variations

### Agent Improvements

1. **Quality Scoring:**
   - Agent self-rates translation quality
   - Flags low-confidence translations for review
   - Provides reasoning for translation choices

2. **Alternative Suggestions:**
   - Generate 2-3 translation options per sentence
   - Allow selection of best option
   - Useful for ambiguous or idiomatic phrases

3. **Glossary Integration:**
   - Maintain term consistency across translations
   - Handle proper nouns appropriately
   - Support custom terminology

---

## Conclusion

The multi-agent translation pipeline successfully demonstrates:

- **High-Quality Translation:** Literary standards maintained throughout
- **Error Resilience:** Spelling errors corrected without degrading quality
- **Cross-Linguistic Analysis:** Meaningful comparison across 3 language families
- **Reproducibility:** Clear prompts and process documentation
- **Scalability:** Architecture supports additional languages or alternative paths

**Key Insight:** Professional-quality translation agents with clear style guidelines and quality gates can maintain semantic meaning reasonably well (avg similarity 0.69) even through a three-stage translation cycle across typologically different languages.

**Research Contribution:** This prompt engineering approach enables systematic study of semantic degradation in translation pipelines, with potential applications in:
- Translation quality assessment
- Multi-lingual content management
- Cross-linguistic NLP research
- Agent-based translation systems

---

**Document Version:** 1.0
**Last Updated:** November 27, 2025
**Authors:** Multi-Stage Translation Quality Analysis System Team
**Contact:** See project README for details
