"""NLP processing module for text analysis using SpaCy and NLTK."""
from typing import List, Dict
import spacy
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load SpaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# PUBLIC_INTERFACE
def process_text(text: str) -> Dict[str, List[str]]:
    """
    Process text using NLP techniques.
    
    Args:
        text (str): Input text to process
        
    Returns:
        Dict[str, List[str]]: Dictionary containing processed text elements
            {
                'sentences': List of sentences,
                'keywords': List of important keywords,
                'entities': List of named entities
            }
    """
    # Process with SpaCy
    doc = nlp(text)
    
    # Extract sentences using NLTK for better sentence boundary detection
    sentences = sent_tokenize(text)
    
    # Extract keywords (excluding stopwords)
    stop_words = set(stopwords.words('english'))
    keywords = [token.text.lower() for token in doc
               if not token.is_stop and not token.is_punct and token.text.lower() not in stop_words]
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents]
    
    return {
        'sentences': sentences,
        'keywords': list(set(keywords)),  # Remove duplicates
        'entities': list(set(entities))   # Remove duplicates
    }

# PUBLIC_INTERFACE
def analyze_query(query: str) -> Dict[str, str]:
    """
    Analyze a user query to understand its intent and key components.
    
    Args:
        query (str): User's query text
        
    Returns:
        Dict[str, str]: Dictionary containing query analysis
            {
                'intent': Detected intent of the query,
                'focus': Main focus/subject of the query
            }
    """
    doc = nlp(query)
    
    # Simple intent detection based on question words
    question_words = {'what', 'why', 'how', 'when', 'where', 'who'}
    intent = 'statement'
    for token in doc:
        if token.text.lower() in question_words:
            intent = 'question'
            break
    
    # Extract the main focus (subject) of the query
    focus = ''
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ in {'nsubj', 'dobj', 'pobj'}:
            focus = chunk.text
            break
    
    return {
        'intent': intent,
        'focus': focus
    }