"""Pytest configuration file for the PDF RAG Chatbot tests."""
import pytest

def pytest_configure(config):
    """Configure pytest for the test suite."""
    # Add markers for different test categories
    config.addinivalue_line(
        "markers",
        "pdf: marks tests related to PDF processing"
    )
    config.addinivalue_line(
        "markers",
        "nlp: marks tests related to NLP processing"
    )
    config.addinivalue_line(
        "markers",
        "response: marks tests related to response generation"
    )
    config.addinivalue_line(
        "markers",
        "api: marks tests related to API integration"
    )
