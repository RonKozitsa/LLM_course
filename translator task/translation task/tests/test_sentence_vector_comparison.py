"""
Unit Tests for Multi-Stage Translation Quality Analysis System

Tests cover:
- CSV file loading and validation
- Data alignment and integrity
- Vector encoding and similarity computation
- Statistical calculations and grouping
- Output file generation
- Edge cases and error handling
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Import the function to test
import sys
import os
# Add parent directory to path to import from scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.sentence_vector_comparison import compare_sentence_vectors


class TestCSVLoading:
    """Test suite for CSV file loading and validation"""

    def test_csv_files_exist(self):
        """Test that required CSV files exist"""
        assert os.path.exists('data/input/English.csv'), "English.csv not found"
        assert os.path.exists('data/output/English_final.csv'), "English_final.csv not found"

    def test_csv_structure_english(self):
        """Test that English.csv has correct structure"""
        df = pd.read_csv('data/input/English.csv')

        # Check required columns exist
        assert 'Index' in df.columns, "Missing 'Index' column"
        assert 'text' in df.columns, "Missing 'text' column"
        assert 'mistakes' in df.columns, "Missing 'mistakes' column"

        # Check data types
        assert df['Index'].dtype in [np.int64, int], "Index should be integer"
        assert df['mistakes'].dtype in [np.int64, int], "Mistakes should be integer"
        assert df['text'].dtype == object, "Text should be string/object"

    def test_csv_structure_english_final(self):
        """Test that English_final.csv has correct structure"""
        df = pd.read_csv('data/output/English_final.csv')

        # Check required columns exist
        assert 'Index' in df.columns, "Missing 'Index' column"
        assert 'text' in df.columns, "Missing 'text' column"

        # Check data types
        assert df['Index'].dtype in [np.int64, int], "Index should be integer"
        assert df['text'].dtype == object, "Text should be string/object"

    def test_row_count_match(self):
        """Test that English.csv and English_final.csv have same row count"""
        df1 = pd.read_csv('data/input/English.csv')
        df2 = pd.read_csv('data/output/English_final.csv')

        assert len(df1) == len(df2), f"Row count mismatch: {len(df1)} vs {len(df2)}"

    def test_index_alignment(self):
        """Test that Index values align between files"""
        df1 = pd.read_csv('data/input/English.csv')
        df2 = pd.read_csv('data/output/English_final.csv')

        # Sort both by Index
        df1_sorted = df1.sort_values('Index')['Index'].values
        df2_sorted = df2.sort_values('Index')['Index'].values

        assert np.array_equal(df1_sorted, df2_sorted), "Index values don't match between files"

    def test_no_null_values(self):
        """Test that there are no null values in critical columns"""
        df1 = pd.read_csv('data/input/English.csv')
        df2 = pd.read_csv('data/output/English_final.csv')

        assert df1['text'].notna().all(), "Null values found in English.csv text column"
        assert df2['text'].notna().all(), "Null values found in English_final.csv text column"
        assert df1['mistakes'].notna().all(), "Null values found in mistakes column"

    def test_no_empty_strings(self):
        """Test that there are no empty strings in text columns"""
        df1 = pd.read_csv('data/input/English.csv')
        df2 = pd.read_csv('data/output/English_final.csv')

        assert (df1['text'].str.strip() != '').all(), "Empty strings found in English.csv"
        assert (df2['text'].str.strip() != '').all(), "Empty strings found in English_final.csv"


class TestDataValidation:
    """Test suite for data validation and integrity"""

    def test_mistake_range(self):
        """Test that mistake counts are within expected range"""
        df = pd.read_csv('data/input/English.csv')

        assert df['mistakes'].min() >= 4, "Mistake count below minimum (4)"
        assert df['mistakes'].max() <= 20, "Mistake count above maximum (20)"

    def test_mistake_distribution(self):
        """Test that there are 10 sentences per mistake count"""
        df = pd.read_csv('data/input/English.csv')

        mistake_counts = df['mistakes'].value_counts()

        # Check that most/all mistake counts have 10 sentences
        expected_count = 10
        for mistake_val, count in mistake_counts.items():
            assert count == expected_count, \
                f"Mistake count {mistake_val} has {count} sentences, expected {expected_count}"

    def test_index_uniqueness(self):
        """Test that Index values are unique"""
        df1 = pd.read_csv('data/input/English.csv')
        df2 = pd.read_csv('data/output/English_final.csv')

        assert len(df1['Index'].unique()) == len(df1), "Duplicate Index values in English.csv"
        assert len(df2['Index'].unique()) == len(df2), "Duplicate Index values in English_final.csv"

    def test_index_sequential(self):
        """Test that Index values are sequential from 1 to N"""
        df = pd.read_csv('data/input/English.csv')

        sorted_indices = sorted(df['Index'].values)
        expected_indices = list(range(1, len(df) + 1))

        assert sorted_indices == expected_indices, "Index values are not sequential"


class TestVectorEncoding:
    """Test suite for sentence encoding and vector operations"""

    @pytest.fixture
    def sample_sentences(self):
        """Provide sample sentences for testing"""
        return [
            "The cat sat on the mat.",
            "A feline rested on the rug.",
            "The dog ran in the park.",
            "Completely unrelated sentence about astronomy."
        ]

    @pytest.fixture
    def model(self):
        """Load sentence transformer model"""
        return SentenceTransformer('all-MiniLM-L6-v2')

    def test_model_loads(self, model):
        """Test that the sentence transformer model loads successfully"""
        assert model is not None
        assert isinstance(model, SentenceTransformer)

    def test_vector_dimensions(self, model, sample_sentences):
        """Test that vectors have correct dimensions (384)"""
        vectors = model.encode(sample_sentences)

        assert vectors.shape[0] == len(sample_sentences), "Wrong number of vectors"
        assert vectors.shape[1] == 384, f"Wrong vector dimensions: expected 384, got {vectors.shape[1]}"

    def test_vector_encoding_deterministic(self, model):
        """Test that encoding is deterministic (same input = same output)"""
        sentence = "This is a test sentence."

        vector1 = model.encode([sentence])[0]
        vector2 = model.encode([sentence])[0]

        assert np.allclose(vector1, vector2), "Encoding is not deterministic"

    def test_similar_sentences_high_similarity(self, model):
        """Test that semantically similar sentences have high cosine similarity"""
        sent1 = "The cat sat on the mat."
        sent2 = "A feline rested on the rug."

        vec1 = model.encode([sent1])[0]
        vec2 = model.encode([sent2])[0]

        similarity = cosine_similarity([vec1], [vec2])[0][0]

        # Similar sentences should have similarity > 0.5
        assert similarity > 0.5, f"Similar sentences have low similarity: {similarity}"

    def test_dissimilar_sentences_low_similarity(self, model):
        """Test that semantically different sentences have lower similarity"""
        sent1 = "The cat sat on the mat."
        sent2 = "Quantum physics is fascinating."

        vec1 = model.encode([sent1])[0]
        vec2 = model.encode([sent2])[0]

        similarity = cosine_similarity([vec1], [vec2])[0][0]

        # Dissimilar sentences should have lower similarity
        # Note: even random sentences rarely go below 0.2 in semantic space
        assert similarity < 0.6, f"Dissimilar sentences have high similarity: {similarity}"

    def test_cosine_similarity_range(self, model, sample_sentences):
        """Test that cosine similarity values are in valid range [-1, 1] (with small tolerance for floating point precision)"""
        vectors = model.encode(sample_sentences)
        tolerance = 1e-6

        for i in range(len(vectors)):
            for j in range(len(vectors)):
                sim = cosine_similarity([vectors[i]], [vectors[j]])[0][0]
                assert -1 - tolerance <= sim <= 1 + tolerance, f"Cosine similarity out of range: {sim}"


class TestStatisticalCalculations:
    """Test suite for statistical calculations and grouping"""

    def test_grouping_by_mistakes(self):
        """Test that sentences are correctly grouped by mistake count"""
        df = pd.read_csv('data/input/English.csv')

        grouped = df.groupby('mistakes').size()

        # Each group should have 10 sentences
        for mistake_count, size in grouped.items():
            assert size == 10, f"Group {mistake_count} has {size} sentences, expected 10"

    def test_average_calculation(self):
        """Test that averages are calculated correctly"""
        # Create sample data
        data = pd.DataFrame({
            'Mistakes': [4, 4, 4, 5, 5, 5],
            'Cosine_Similarity': [0.8, 0.9, 0.7, 0.6, 0.5, 0.7]
        })

        # Group and calculate average
        avg_by_mistakes = data.groupby('Mistakes')['Cosine_Similarity'].mean()

        assert np.isclose(avg_by_mistakes[4], 0.8), "Average calculation incorrect for group 4"
        assert np.isclose(avg_by_mistakes[5], 0.6), "Average calculation incorrect for group 5"

    def test_standard_deviation_calculation(self):
        """Test that standard deviation is calculated correctly"""
        # Create sample data with known std dev
        data = pd.DataFrame({
            'Mistakes': [4, 4, 4, 4],
            'Cosine_Similarity': [0.6, 0.7, 0.8, 0.9]
        })

        grouped = data.groupby('Mistakes')['Cosine_Similarity'].std()
        expected_std = np.std([0.6, 0.7, 0.8, 0.9], ddof=1)

        assert np.isclose(grouped[4], expected_std), "Standard deviation calculation incorrect"

    def test_correlation_calculation(self):
        """Test correlation coefficient calculation"""
        # Create data with known correlation
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])  # Perfect positive correlation

        correlation = np.corrcoef(x, y)[0, 1]

        assert np.isclose(correlation, 1.0), "Correlation calculation incorrect for perfect correlation"


class TestOutputFiles:
    """Test suite for output file generation"""

    def test_results_csv_generated(self):
        """Test that vector_similarity_results.csv is generated"""
        # This assumes the script has been run at least once
        if os.path.exists('data/output/vector_similarity_results.csv'):
            df = pd.read_csv('data/output/vector_similarity_results.csv')

            # Check structure
            assert 'Index' in df.columns
            assert 'Mistakes' in df.columns
            assert 'Cosine_Similarity' in df.columns
            assert 'Original_Sentence' in df.columns
            assert 'Final_Sentence' in df.columns

            # Check row count matches input
            df_input = pd.read_csv('data/input/English.csv')
            assert len(df) == len(df_input)

    def test_averaged_csv_generated(self):
        """Test that vector_similarity_averaged.csv is generated"""
        # This assumes the script has been run at least once
        if os.path.exists('data/output/vector_similarity_averaged.csv'):
            df = pd.read_csv('data/output/vector_similarity_averaged.csv')

            # Check structure
            assert 'Mistakes' in df.columns
            assert 'Avg_Similarity' in df.columns
            assert 'Std_Dev' in df.columns
            assert 'Count' in df.columns

            # Check that all counts are 10
            assert (df['Count'] == 10).all(), "Not all groups have 10 sentences"

    def test_plot_generated(self):
        """Test that plot file is generated"""
        # This assumes the script has been run at least once
        assert os.path.exists('visualizations/vector_similarity_vs_mistakes.png'), \
            "Plot file not generated"

    def test_output_similarity_range(self):
        """Test that all similarity values in output are in valid range"""
        if os.path.exists('data/output/vector_similarity_results.csv'):
            df = pd.read_csv('data/output/vector_similarity_results.csv')

            assert (df['Cosine_Similarity'] >= 0).all(), "Negative similarity values found"
            assert (df['Cosine_Similarity'] <= 1).all(), "Similarity values > 1 found"

    def test_averaged_output_validity(self):
        """Test that averaged output has valid statistics"""
        if os.path.exists('data/output/vector_similarity_averaged.csv'):
            df = pd.read_csv('data/output/vector_similarity_averaged.csv')

            # All averages should be in valid range
            assert (df['Avg_Similarity'] >= 0).all(), "Negative average similarity"
            assert (df['Avg_Similarity'] <= 1).all(), "Average similarity > 1"

            # Standard deviations should be non-negative
            assert (df['Std_Dev'] >= 0).all(), "Negative standard deviation"

            # Mistake counts should be in expected range
            assert df['Mistakes'].min() >= 4, "Mistake count below 4"
            assert df['Mistakes'].max() <= 20, "Mistake count above 20"


class TestEdgeCases:
    """Test suite for edge cases and error handling"""

    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('Index,text,mistakes\n')
            empty_file = f.name

        try:
            df = pd.read_csv(empty_file)
            assert len(df) == 0, "Empty file should produce empty DataFrame"
        finally:
            os.unlink(empty_file)

    def test_single_sentence_similarity(self):
        """Test that identical sentences have similarity of 1.0"""
        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentence = "This is a test sentence."

        vec1 = model.encode([sentence])[0]
        vec2 = model.encode([sentence])[0]

        similarity = cosine_similarity([vec1], [vec2])[0][0]

        # Should be very close to 1.0 (allowing for floating point precision)
        assert np.isclose(similarity, 1.0, atol=1e-5), f"Identical sentences should have similarity ~1.0, got {similarity}"

    def test_file_not_found_handling(self):
        """Test that appropriate error is raised for missing files"""
        with pytest.raises(FileNotFoundError):
            pd.read_csv('nonexistent_file.csv')


class TestIntegration:
    """Integration tests for the complete pipeline"""

    @pytest.mark.slow
    def test_full_pipeline_execution(self):
        """Test that the full comparison pipeline executes without errors"""
        # This is a slow test as it loads the model and processes all sentences
        try:
            results, correlation = compare_sentence_vectors(
                'data/input/English.csv',
                'data/output/English_final.csv',
                'test_output.png'
            )

            # Verify results structure
            assert isinstance(results, pd.DataFrame)
            assert isinstance(correlation, float)
            assert -1 <= correlation <= 1

            # Cleanup
            if os.path.exists('test_output.png'):
                os.unlink('test_output.png')

        except Exception as e:
            pytest.fail(f"Full pipeline execution failed: {e}")

    def test_translation_pipeline_data_flow(self):
        """Test that data flows correctly through translation pipeline"""
        # Verify the translation pipeline CSV files
        files = ['data/input/English.csv', 'data/intermediate/French.csv', 'data/intermediate/Hebrew.csv', 'data/output/English_final.csv']

        for file in files:
            if os.path.exists(file):
                df = pd.read_csv(file)
                assert 'Index' in df.columns, f"{file} missing Index column"
                assert 'text' in df.columns, f"{file} missing text column"

        # Verify row counts match across all files
        if all(os.path.exists(f) for f in files):
            row_counts = [len(pd.read_csv(f)) for f in files]
            assert len(set(row_counts)) == 1, "Row counts don't match across translation pipeline"


class TestPerformance:
    """Test suite for performance and efficiency"""

    @pytest.mark.slow
    def test_encoding_performance(self):
        """Test that encoding performance is acceptable"""
        import time

        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = ["This is a test sentence."] * 100

        start_time = time.time()
        vectors = model.encode(sentences)
        end_time = time.time()

        elapsed = end_time - start_time

        # Encoding 100 sentences should take less than 10 seconds on most hardware
        assert elapsed < 10, f"Encoding too slow: {elapsed:.2f} seconds for 100 sentences"

    def test_memory_efficiency(self):
        """Test that vector storage is memory efficient"""
        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = ["Test sentence"] * 1000

        vectors = model.encode(sentences)

        # Check memory footprint is reasonable (384 dims * 1000 sentences * 4 bytes/float32)
        expected_size = 384 * 1000 * 4  # ~1.5 MB
        actual_size = vectors.nbytes

        # Should be close to expected (within 10%)
        assert abs(actual_size - expected_size) / expected_size < 0.1, \
            f"Unexpected vector size: {actual_size} bytes vs expected {expected_size}"


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
