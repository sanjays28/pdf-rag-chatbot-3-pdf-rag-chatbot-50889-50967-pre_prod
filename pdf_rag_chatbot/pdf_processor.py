"""PDF processing module for handling PDF uploads and text extraction."""
import os
from typing import Dict, Optional
from PyPDF2 import PdfReader

# PUBLIC_INTERFACE
def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        Optional[str]: Extracted text content or None if extraction fails
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

# PUBLIC_INTERFACE
def validate_pdf(file_path: str) -> Dict[str, bool | str]:
    """
    Validate a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        Dict[str, bool | str]: Dictionary containing validation results
            {
                'valid': bool,
                'error': str (if any)
            }
    """
    if not os.path.exists(file_path):
        return {'valid': False, 'error': 'File does not exist'}
        
    if not file_path.lower().endswith('.pdf'):
        return {'valid': False, 'error': 'File is not a PDF'}
        
    try:
        # Try to open and read the PDF
        PdfReader(file_path)
        return {'valid': True, 'error': ''}
    except Exception as e:
        return {'valid': False, 'error': f'Invalid PDF file: {str(e)}'}