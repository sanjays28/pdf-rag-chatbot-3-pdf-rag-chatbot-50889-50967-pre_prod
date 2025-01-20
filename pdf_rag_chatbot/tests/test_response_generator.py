"""Unit tests for the response generator module."""
import pytest
from response_generator import generate_response, _find_relevant_sentences, _construct_response

@pytest.fixture
def sample_query_analysis():
    """Sample query analysis results."""
    return {
        'intent': 'question',
        'focus': 'cloud computing'
    }

@pytest.fixture
def sample_processed_text():
    """Sample processed text results."""
    return {
        'sentences': [
            'Cloud computing is a technology that enables remote access to computing resources.',
            'It provides scalable and flexible solutions for businesses.',
            'Many companies are adopting cloud computing for their operations.'
        ],
        'keywords': ['cloud', 'computing', 'technology', 'remote', 'access', 'scalable', 'flexible'],
        'entities': ['Cloud computing']
    }

def test_generate_response_with_valid_input(sample_query_analysis, sample_processed_text):
    """Test response generation with valid input."""
    result = generate_response(sample_query_analysis, sample_processed_text)
    
    assert isinstance(result, dict)
    assert 'response' in result
    assert 'confidence' in result
    assert 'source' in result
    assert len(result['response']) > 0
    assert result['source'] == 'document'
    assert float(result['confidence']) > 0

def test_generate_response_with_empty_text():
    """Test response generation with empty processed text."""
    empty_text = {
        'sentences': [],
        'keywords': [],
        'entities': []
    }
    result = generate_response({'intent': 'question', 'focus': 'test'}, empty_text)
    
    assert result['response'] == "I couldn't find any relevant information in the document."
    assert result['confidence'] == '0.0'
    assert result['source'] == 'none'

def test_find_relevant_sentences():
    """Test finding relevant sentences."""
    sentences = [
        'Cloud computing is important.',
        'AI is advancing rapidly.',
        'Cloud services are popular.'
    ]
    focus = 'cloud computing'
    keywords = ['cloud', 'computing', 'important', 'services']
    
    result = _find_relevant_sentences(focus, sentences, keywords)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert any('Cloud computing' in s for s in result)

def test_find_relevant_sentences_with_no_matches():
    """Test finding relevant sentences with no matches."""
    sentences = ['AI is advancing rapidly.']
    focus = 'cloud computing'
    keywords = ['ai', 'advancing']
    
    result = _find_relevant_sentences(focus, sentences, keywords)
    assert len(result) == 0

def test_construct_response_question():
    """Test response construction for questions."""
    sentences = ['Cloud computing is important.', 'It enables remote work.']
    result = _construct_response('question', sentences)
    
    assert result.startswith('Based on the document')
    assert 'Cloud computing is important' in result
    assert 'enables remote work' in result

def test_construct_response_statement():
    """Test response construction for statements."""
    sentences = ['Cloud computing is important.']
    result = _construct_response('statement', sentences)
    
    assert 'Cloud computing is important' in result
    assert not result.startswith('Based on the document')

def test_construct_response_empty():
    """Test response construction with no relevant sentences."""
    result = _construct_response('question', [])
    assert result == "I couldn't find specific information about that."