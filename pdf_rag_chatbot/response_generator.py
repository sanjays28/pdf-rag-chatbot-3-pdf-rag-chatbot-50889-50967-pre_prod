"""Response generation module for the chatbot."""
from typing import Dict, List, Optional
from nltk.tokenize import sent_tokenize
from nltk.metrics.distance import edit_distance

# PUBLIC_INTERFACE
def generate_response(
    query_analysis: Dict[str, str],
    processed_text: Dict[str, List[str]],
    context: Optional[Dict] = None
) -> Dict[str, str]:
    """
    Generate a response based on the analyzed query and processed text.
    
    Args:
        query_analysis (Dict[str, str]): Analysis of the user's query
        processed_text (Dict[str, List[str]]): Processed document text
        context (Optional[Dict]): Additional context for response generation
        
    Returns:
        Dict[str, str]: Generated response
            {
                'response': Generated response text,
                'confidence': Confidence score of the response,
                'source': Source of the information
            }
    """
    if not processed_text['sentences']:
        return {
            'response': "I couldn't find any relevant information in the document.",
            'confidence': '0.0',
            'source': 'none'
        }
    
    # Find most relevant sentences based on keyword matching
    relevant_sentences = _find_relevant_sentences(
        query_analysis['focus'],
        processed_text['sentences'],
        processed_text['keywords']
    )
    
    if not relevant_sentences:
        return {
            'response': "I couldn't find a specific answer to your question.",
            'confidence': '0.0',
            'source': 'none'
        }
    
    # Construct response based on query intent
    response = _construct_response(query_analysis['intent'], relevant_sentences)
    
    return {
        'response': response,
        'confidence': '0.8',  # Simplified confidence scoring
        'source': 'document'
    }

def _find_relevant_sentences(focus: str, sentences: List[str], keywords: List[str]) -> List[str]:
    """
    Find sentences relevant to the query focus.
    
    Args:
        focus (str): Main focus of the query
        sentences (List[str]): List of sentences from the document
        keywords (List[str]): List of important keywords
        
    Returns:
        List[str]: List of relevant sentences
    """
    relevant = []
    focus_words = set(focus.lower().split())
    
    for sentence in sentences:
        # Check for direct matches with focus
        if any(word.lower() in sentence.lower() for word in focus_words):
            relevant.append(sentence)
            continue
            
        # Check for semantic similarity using edit distance
        sentence_words = set(sentence.lower().split())
        for focus_word in focus_words:
            for sentence_word in sentence_words:
                if edit_distance(focus_word, sentence_word) <= 2:  # Allow for minor variations
                    relevant.append(sentence)
                    break
            if sentence in relevant:
                break
    
    return relevant

def _construct_response(intent: str, relevant_sentences: List[str]) -> str:
    """
    Construct a natural language response based on intent and relevant sentences.
    
    Args:
        intent (str): Query intent (question or statement)
        relevant_sentences (List[str]): Relevant sentences from the document
        
    Returns:
        str: Constructed response
    """
    if not relevant_sentences:
        return "I couldn't find specific information about that."
    
    if intent == 'question':
        response = "Based on the document, " + relevant_sentences[0]
        if len(relevant_sentences) > 1:
            response += " Additionally, " + relevant_sentences[1]
    else:
        response = relevant_sentences[0]
        if len(relevant_sentences) > 1:
            response += " " + relevant_sentences[1]
    
    return response.strip()