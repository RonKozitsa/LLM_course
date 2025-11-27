"""
Unit tests for data validation across the translation pipeline

Tests the integrity and consistency of CSV files generated
by the translation agents and analysis scripts.
"""

import pytest
import pandas as pd
import numpy as np
import os


class TestTranslationPipelineDataFlow:
    """Test data flow through the complete translation pipeline"""

    def test_all_pipeline_files_exist(self, project_root):
        """Test that all expected CSV files exist in the pipeline"""
        files = {
            'English.csv': os.path.join('data', 'input', 'English.csv'),
            'French.csv': os.path.join('data', 'intermediate', 'French.csv'),
            'Hebrew.csv': os.path.join('data', 'intermediate', 'Hebrew.csv'),
            'English_final.csv': os.path.join('data', 'output', 'English_final.csv')
        }

        for name, relpath in files.items():
            filepath = os.path.join(project_root, relpath)
            assert os.path.exists(filepath), f"Missing pipeline file: {name} at {relpath}"

    def test_row_count_consistency(self, project_root):
        """Test that all pipeline files have the same row count"""
        files = {
            'English.csv': os.path.join('data', 'input', 'English.csv'),
            'French.csv': os.path.join('data', 'intermediate', 'French.csv'),
            'Hebrew.csv': os.path.join('data', 'intermediate', 'Hebrew.csv'),
            'English_final.csv': os.path.join('data', 'output', 'English_final.csv')
        }
        row_counts = []
        file_names = []

        for name, relpath in files.items():
            filepath = os.path.join(project_root, relpath)
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                row_counts.append(len(df))
                file_names.append(name)

        if row_counts:
            assert len(set(row_counts)) == 1, \
                f"Inconsistent row counts across pipeline: {dict(zip(file_names, row_counts))}"

    def test_index_alignment_across_pipeline(self, project_root):
        """Test that Index values align across all pipeline files"""
        files = {
            'English.csv': os.path.join('data', 'input', 'English.csv'),
            'French.csv': os.path.join('data', 'intermediate', 'French.csv'),
            'Hebrew.csv': os.path.join('data', 'intermediate', 'Hebrew.csv'),
            'English_final.csv': os.path.join('data', 'output', 'English_final.csv')
        }
        index_sets = []
        file_names = []

        for name, relpath in files.items():
            filepath = os.path.join(project_root, relpath)
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                index_sets.append(set(df['Index'].values))
                file_names.append(name)

        if len(index_sets) > 1:
            # All index sets should be identical
            for i in range(1, len(index_sets)):
                assert index_sets[0] == index_sets[i], \
                    f"Index mismatch between {file_names[0]} and {file_names[i]}"

    def test_no_data_loss_through_pipeline(self, project_root):
        """Test that no rows are lost through the translation pipeline"""
        english_path = os.path.join(project_root, 'data', 'input', 'English.csv')
        final_path = os.path.join(project_root, 'data', 'output', 'English_final.csv')

        if os.path.exists(english_path) and os.path.exists(final_path):
            df_english = pd.read_csv(english_path)
            df_final = pd.read_csv(final_path)

            # Check that all original indices are present in final
            original_indices = set(df_english['Index'].values)
            final_indices = set(df_final['Index'].values)

            missing = original_indices - final_indices
            assert len(missing) == 0, f"Lost rows in translation pipeline: {missing}"


class TestEnglishCSVValidation:
    """Validation tests specific to English.csv (input file)"""

    def test_required_columns(self, load_english_csv):
        """Test that English.csv has all required columns"""
        if load_english_csv is not None:
            required_columns = ['Index', 'text', 'mistakes']
            for col in required_columns:
                assert col in load_english_csv.columns, f"Missing required column: {col}"

    def test_data_types(self, load_english_csv):
        """Test that columns have correct data types"""
        if load_english_csv is not None:
            assert load_english_csv['Index'].dtype in [np.int64, int], \
                f"Index should be integer, got {load_english_csv['Index'].dtype}"
            assert load_english_csv['mistakes'].dtype in [np.int64, int], \
                f"mistakes should be integer, got {load_english_csv['mistakes'].dtype}"

    def test_index_values(self, load_english_csv):
        """Test Index column properties"""
        if load_english_csv is not None:
            # Should be unique
            assert load_english_csv['Index'].is_unique, "Index values are not unique"

            # Should be positive
            assert (load_english_csv['Index'] > 0).all(), "Index contains non-positive values"

            # Should be sequential (1, 2, 3, ...)
            sorted_indices = sorted(load_english_csv['Index'].values)
            expected = list(range(1, len(load_english_csv) + 1))
            assert sorted_indices == expected, "Index values are not sequential from 1 to N"

    def test_mistakes_values(self, load_english_csv):
        """Test mistakes column properties"""
        if load_english_csv is not None:
            # Should be non-negative
            assert (load_english_csv['mistakes'] >= 0).all(), \
                "mistakes contains negative values"

            # Should be within expected range for this project (4-20)
            assert load_english_csv['mistakes'].min() >= 4, \
                f"Minimum mistakes ({load_english_csv['mistakes'].min()}) below expected (4)"
            assert load_english_csv['mistakes'].max() <= 20, \
                f"Maximum mistakes ({load_english_csv['mistakes'].max()}) above expected (20)"

    def test_text_column(self, load_english_csv):
        """Test text column properties"""
        if load_english_csv is not None:
            # No null values
            assert load_english_csv['text'].notna().all(), "text column contains null values"

            # No empty strings
            assert (load_english_csv['text'].str.strip() != '').all(), \
                "text column contains empty strings"

            # All entries should be strings
            assert load_english_csv['text'].dtype == object, \
                f"text should be string/object type, got {load_english_csv['text'].dtype}"

    def test_stratified_sampling(self, load_english_csv):
        """Test that there are 10 sentences per mistake count (stratified sampling)"""
        if load_english_csv is not None:
            mistake_counts = load_english_csv['mistakes'].value_counts()

            # Most groups should have exactly 10 sentences
            expected_count = 10
            for mistake_val, count in mistake_counts.items():
                assert count == expected_count, \
                    f"Mistake count {mistake_val} has {count} sentences, expected {expected_count}"


class TestFrenchCSVValidation:
    """Validation tests specific to French.csv (intermediate file)"""

    def test_french_file_structure(self, french_csv_path):
        """Test French.csv structure"""
        if os.path.exists(french_csv_path):
            df = pd.read_csv(french_csv_path)

            # Required columns
            assert 'Index' in df.columns, "Missing Index column"
            assert 'text' in df.columns, "Missing text column"

            # Data quality
            assert df['text'].notna().all(), "Null values in French text"
            assert (df['text'].str.strip() != '').all(), "Empty strings in French text"

    def test_french_text_quality(self, french_csv_path):
        """Test that French text appears to be valid"""
        if os.path.exists(french_csv_path):
            df = pd.read_csv(french_csv_path)

            # French text should have reasonable length (not just a few characters)
            avg_length = df['text'].str.len().mean()
            assert avg_length > 10, f"French text seems too short (avg: {avg_length} chars)"


class TestHebrewCSVValidation:
    """Validation tests specific to Hebrew.csv (intermediate file)"""

    def test_hebrew_file_structure(self, hebrew_csv_path):
        """Test Hebrew.csv structure"""
        if os.path.exists(hebrew_csv_path):
            df = pd.read_csv(hebrew_csv_path)

            # Required columns
            assert 'Index' in df.columns, "Missing Index column"
            assert 'text' in df.columns, "Missing text column"

            # Data quality
            assert df['text'].notna().all(), "Null values in Hebrew text"
            assert (df['text'].str.strip() != '').all(), "Empty strings in Hebrew text"

    def test_hebrew_text_quality(self, hebrew_csv_path):
        """Test that Hebrew text appears to be valid"""
        if os.path.exists(hebrew_csv_path):
            df = pd.read_csv(hebrew_csv_path)

            # Hebrew text should have reasonable length
            avg_length = df['text'].str.len().mean()
            assert avg_length > 10, f"Hebrew text seems too short (avg: {avg_length} chars)"


class TestEnglishFinalCSVValidation:
    """Validation tests specific to English_final.csv (output file)"""

    def test_final_file_structure(self, load_english_final_csv):
        """Test English_final.csv structure"""
        if load_english_final_csv is not None:
            # Required columns
            assert 'Index' in load_english_final_csv.columns, "Missing Index column"
            assert 'text' in load_english_final_csv.columns, "Missing text column"

            # Data quality
            assert load_english_final_csv['text'].notna().all(), \
                "Null values in final English text"
            assert (load_english_final_csv['text'].str.strip() != '').all(), \
                "Empty strings in final English text"

    def test_final_text_quality(self, load_english_final_csv):
        """Test that final English text has reasonable quality"""
        if load_english_final_csv is not None:
            # Text should have reasonable length
            avg_length = load_english_final_csv['text'].str.len().mean()
            assert avg_length > 10, \
                f"Final English text seems too short (avg: {avg_length} chars)"

    def test_translation_completeness(self, load_english_csv, load_english_final_csv):
        """Test that all original sentences have been translated"""
        if load_english_csv is not None and load_english_final_csv is not None:
            original_indices = set(load_english_csv['Index'].values)
            final_indices = set(load_english_final_csv['Index'].values)

            # All original indices should be present
            missing = original_indices - final_indices
            assert len(missing) == 0, f"Missing translations for indices: {missing}"

            # No extra indices should be present
            extra = final_indices - original_indices
            assert len(extra) == 0, f"Extra indices in final output: {extra}"


class TestOutputCSVValidation:
    """Validation tests for analysis output CSV files"""

    def test_results_csv_structure(self, project_root):
        """Test vector_similarity_results.csv structure"""
        results_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv')

        if os.path.exists(results_path):
            df = pd.read_csv(results_path)

            # Required columns
            required_cols = ['Index', 'Mistakes', 'Cosine_Similarity',
                           'Original_Sentence', 'Final_Sentence']
            for col in required_cols:
                assert col in df.columns, f"Missing column: {col}"

            # Data validity
            assert (df['Cosine_Similarity'] >= 0).all(), "Negative similarity values"
            assert (df['Cosine_Similarity'] <= 1).all(), "Similarity values > 1"
            assert df['Index'].is_unique, "Duplicate indices in results"

    def test_averaged_csv_structure(self, project_root):
        """Test vector_similarity_averaged.csv structure"""
        averaged_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_averaged.csv')

        if os.path.exists(averaged_path):
            df = pd.read_csv(averaged_path)

            # Required columns
            required_cols = ['Mistakes', 'Avg_Similarity', 'Std_Dev', 'Count']
            for col in required_cols:
                assert col in df.columns, f"Missing column: {col}"

            # Data validity
            assert (df['Avg_Similarity'] >= 0).all(), "Negative average similarity"
            assert (df['Avg_Similarity'] <= 1).all(), "Average similarity > 1"
            assert (df['Std_Dev'] >= 0).all(), "Negative standard deviation"
            assert (df['Count'] > 0).all(), "Non-positive counts"

    def test_averaged_csv_completeness(self, project_root):
        """Test that averaged CSV has entries for all mistake counts"""
        averaged_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_averaged.csv')

        if os.path.exists(averaged_path):
            df = pd.read_csv(averaged_path)

            # Should have entries for mistake counts 4-20
            expected_mistakes = set(range(4, 21))
            actual_mistakes = set(df['Mistakes'].values)

            assert expected_mistakes == actual_mistakes, \
                f"Missing mistake counts: {expected_mistakes - actual_mistakes}"


class TestDataConsistency:
    """Tests for data consistency across different files"""

    def test_results_match_input_count(self, project_root):
        """Test that results CSV has same row count as input"""
        english_path = os.path.join(project_root, 'data', 'input', 'English.csv')
        results_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv')

        if os.path.exists(english_path) and os.path.exists(results_path):
            df_english = pd.read_csv(english_path)
            df_results = pd.read_csv(results_path)

            assert len(df_english) == len(df_results), \
                f"Row count mismatch: input has {len(df_english)}, results has {len(df_results)}"

    def test_mistakes_preserved_in_results(self, project_root):
        """Test that mistake counts are preserved in results CSV"""
        english_path = os.path.join(project_root, 'data', 'input', 'English.csv')
        results_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv')

        if os.path.exists(english_path) and os.path.exists(results_path):
            df_english = pd.read_csv(english_path)
            df_results = pd.read_csv(results_path)

            # Merge on Index and compare mistakes
            merged = df_english.merge(df_results, on='Index', suffixes=('_orig', '_result'))

            if 'mistakes_orig' in merged.columns and 'Mistakes' in merged.columns:
                assert (merged['mistakes_orig'] == merged['Mistakes']).all(), \
                    "Mistake counts don't match between input and results"

    def test_averaged_counts_correct(self, project_root):
        """Test that Count column in averaged CSV is correct"""
        results_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv')
        averaged_path = os.path.join(project_root, 'data', 'output', 'vector_similarity_averaged.csv')

        if os.path.exists(results_path) and os.path.exists(averaged_path):
            df_results = pd.read_csv(results_path)
            df_averaged = pd.read_csv(averaged_path)

            # Count sentences per mistake in results
            actual_counts = df_results.groupby('Mistakes').size()

            # Compare with Count column in averaged
            for _, row in df_averaged.iterrows():
                mistake_val = int(row['Mistakes'])
                expected_count = actual_counts.get(mistake_val, 0)
                assert row['Count'] == expected_count, \
                    f"Count mismatch for {mistake_val} mistakes: " \
                    f"averaged says {row['Count']}, actual is {expected_count}"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
