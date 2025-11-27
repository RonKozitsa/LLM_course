"""
Pytest configuration and shared fixtures for test suite
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def sentence_model():
    """
    Load sentence transformer model once for entire test session
    This is expensive, so we cache it at session level
    """
    return SentenceTransformer('all-MiniLM-L6-v2')


@pytest.fixture(scope="session")
def project_root():
    """Return path to project root directory"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def english_csv_path(project_root):
    """Return path to English.csv"""
    return os.path.join(project_root, 'data', 'input', 'English.csv')


@pytest.fixture
def english_final_csv_path(project_root):
    """Return path to English_final.csv"""
    return os.path.join(project_root, 'data', 'output', 'English_final.csv')


@pytest.fixture
def french_csv_path(project_root):
    """Return path to French.csv"""
    return os.path.join(project_root, 'data', 'intermediate', 'French.csv')


@pytest.fixture
def hebrew_csv_path(project_root):
    """Return path to Hebrew.csv"""
    return os.path.join(project_root, 'data', 'intermediate', 'Hebrew.csv')


@pytest.fixture
def sample_sentences():
    """Provide sample sentences for testing"""
    return [
        "The cat sat on the mat.",
        "A feline rested on the rug.",
        "The dog ran in the park.",
        "Completely unrelated sentence about astronomy.",
        "Machine learning is fascinating."
    ]


@pytest.fixture
def sample_csv_data():
    """Provide sample CSV data for testing"""
    return pd.DataFrame({
        'Index': [1, 2, 3, 4, 5],
        'text': [
            "Test sentence one.",
            "Test sentence two.",
            "Test sentence three.",
            "Test sentence four.",
            "Test sentence five."
        ],
        'mistakes': [4, 4, 5, 5, 6]
    })


@pytest.fixture
def load_english_csv(english_csv_path):
    """Load English.csv if it exists"""
    if os.path.exists(english_csv_path):
        return pd.read_csv(english_csv_path)
    return None


@pytest.fixture
def load_english_final_csv(english_final_csv_path):
    """Load English_final.csv if it exists"""
    if os.path.exists(english_final_csv_path):
        return pd.read_csv(english_final_csv_path)
    return None


# Helper function to change working directory to project root for tests
@pytest.fixture(autouse=True)
def change_test_dir(request, project_root):
    """Automatically change to project root directory for all tests"""
    original_dir = os.getcwd()
    os.chdir(project_root)
    yield
    os.chdir(original_dir)


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests based on their names
    """
    for item in items:
        # Mark slow tests
        if "performance" in item.nodeid.lower() or "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)

        # Mark integration tests
        if "integration" in item.nodeid.lower() or "pipeline" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)

        # Mark unit tests
        if "test_" in item.nodeid and "integration" not in item.nodeid.lower():
            item.add_marker(pytest.mark.unit)
