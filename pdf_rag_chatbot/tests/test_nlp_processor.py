"""Unit tests for the NLP processor module."""
import pytest
from nlp_processor import process_text, analyze_query

@pytest.fixture
def sample_text():
    """Sample text for testing NLP processing."""
    return """John Smith works at Microsoft in Seattle. 
    He is developing new software for cloud computing. 
    The project aims to improve AI capabilities."""

@pytest.fixture
def sample_queries():
    """Sample queries for testing query analysis."""
    return [
        "What is cloud computing?",
        "Who works at Microsoft?",
        "The software is being developed",
        "Where is John Smith working?"
    ]

def test_process_text_with_valid_input(sample_text):
    """Test text processing with valid input."""
    result = process_text(sample_text)
    
    assert isinstance(result, dict)
    assert 'sentences' in result
    assert 'keywords' in result
    assert 'entities' in result
    
    # Check sentences
    assert len(result['sentences']) >= 3
    assert all(isinstance(s, str) for s in result['sentences'])
    
    # Check keywords
    assert len(result['keywords']) > 0
    assert all(isinstance(k, str) for k in result['keywords'])
    assert 'software' in result['keywords']
    
    # Check entities
    assert len(result['entities']) > 0
    assert all(isinstance(e, str) for e in result['entities'])
    assert any('John Smith' in e for e in result['entities'])
    assert any('Microsoft' in e for e in result['entities'])

def test_process_text_with_empty_input():
    """Test text processing with empty input."""
    result = process_text("")
    
    assert isinstance(result, dict)
    assert len(result['sentences']) == 0
    assert len(result['keywords']) == 0
    assert len(result['entities']) == 0

def test_analyze_query_with_question(sample_queries):
    """Test query analysis with question queries."""
    for query in sample_queries[:2]:  # First two are questions
        result = analyze_query(query)
        
        assert isinstance(result, dict)
        assert 'intent' in result
        assert 'focus' in result
        assert result['intent'] == 'question'
        assert len(result['focus']) > 0

def test_analyze_query_with_statement(sample_queries):
    """Test query analysis with statement queries."""
    result = analyze_query(sample_queries[2])  # Third one is a statement
    
    assert isinstance(result, dict)
    assert result['intent'] == 'statement'
    assert len(result['focus']) > 0

def test_analyze_query_with_empty_input():
    """Test query analysis with empty input."""
    result = analyze_query("")
    
    assert isinstance(result, dict)
    assert result['intent'] == 'statement'
    assert result['focus'] == ''