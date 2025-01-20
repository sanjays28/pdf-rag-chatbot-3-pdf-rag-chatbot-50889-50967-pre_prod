"""Integration tests for the PDF RAG Chatbot API endpoints."""
import os
import pytest
from io import BytesIO
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.test_client() as client:
        yield client
    # Cleanup test uploads after tests
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    os.rmdir(app.config['UPLOAD_FOLDER'])

def create_test_pdf():
    """Create a test PDF file in memory."""
    return (BytesIO(b'%PDF-1.4 Test PDF content'), 'test.pdf')

def test_upload_endpoint_valid_pdf(client):
    """Test successful PDF upload."""
    test_file, filename = create_test_pdf()
    response = client.post(
        '/upload',
        data={'file': (test_file, filename)},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    assert response.json['message'] == 'File uploaded and processed successfully'

def test_upload_endpoint_no_file(client):
    """Test upload endpoint with no file."""
    response = client.post('/upload')
    assert response.status_code == 400
    assert response.json['error'] == 'No file part'

def test_upload_endpoint_empty_filename(client):
    """Test upload endpoint with empty filename."""
    response = client.post(
        '/upload',
        data={'file': (BytesIO(b''), '')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert response.json['error'] == 'No selected file'

def test_upload_endpoint_invalid_file_type(client):
    """Test upload endpoint with invalid file type."""
    response = client.post(
        '/upload',
        data={'file': (BytesIO(b'test content'), 'test.txt')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert response.json['error'] == 'File type not allowed'

def test_upload_endpoint_file_size_limit(client):
    """Test upload endpoint with file exceeding size limit."""
    large_content = b'0' * (16 * 1024 * 1024 + 1)  # 16MB + 1 byte
    response = client.post(
        '/upload',
        data={'file': (BytesIO(large_content), 'large.pdf')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 413  # Request Entity Too Large

def test_chat_endpoint_valid_query(client):
    """Test chat endpoint with valid query."""
    response = client.post(
        '/chat',
        json={'message': 'What is the content about?'}
    )
    assert response.status_code == 200
    assert 'response' in response.json

def test_chat_endpoint_empty_message(client):
    """Test chat endpoint with empty message."""
    response = client.post(
        '/chat',
        json={'message': ''}
    )
    assert response.status_code == 200
    assert 'response' in response.json

def test_chat_endpoint_missing_message(client):
    """Test chat endpoint with missing message field."""
    response = client.post(
        '/chat',
        json={}
    )
    assert response.status_code == 400
    assert response.json['error'] == 'No message provided'

def test_chat_endpoint_invalid_json(client):
    """Test chat endpoint with invalid JSON."""
    response = client.post(
        '/chat',
        data='invalid json',
        content_type='application/json'
    )
    assert response.status_code == 400

def test_chat_endpoint_context_handling(client):
    """Test chat endpoint with context-aware query."""
    # First upload a PDF
    test_file, filename = create_test_pdf()
    client.post(
        '/upload',
        data={'file': (test_file, filename)},
        content_type='multipart/form-data'
    )
    
    # Then make a context-aware query
    response = client.post(
        '/chat',
        json={'message': 'Summarize the uploaded document'}
    )
    assert response.status_code == 200
    assert 'response' in response.json