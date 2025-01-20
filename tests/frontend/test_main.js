/**
 * Unit tests for PDF RAG Chatbot frontend functionality
 */

// Mock DOM elements
document.body.innerHTML = `
    <div id="drop-zone"></div>
    <input type="file" id="file-input">
    <button id="upload-btn">Upload</button>
    <div id="upload-status"></div>
    <div id="upload-section"></div>
    <div id="chat-section" class="hidden">
        <div id="chat-messages"></div>
        <textarea id="user-input"></textarea>
        <button id="send-btn">Send</button>
    </div>
    <div id="loading-overlay" class="hidden">
        <div id="loading-text"></div>
    </div>
    <div id="error-modal">
        <div id="error-message"></div>
    </div>
`;

// Mock fetch function
global.fetch = jest.fn();

describe('PDF RAG Chatbot Frontend Tests', () => {
    let dropZone, fileInput, uploadBtn, uploadStatus, uploadSection, 
        chatSection, chatMessages, userInput, sendBtn, loadingOverlay,
        loadingText, errorModal, errorMessage;

    beforeEach(() => {
        // Reset fetch mock
        fetch.mockClear();

        // Initialize DOM elements
        dropZone = document.getElementById('drop-zone');
        fileInput = document.getElementById('file-input');
        uploadBtn = document.getElementById('upload-btn');
        uploadStatus = document.getElementById('upload-status');
        uploadSection = document.getElementById('upload-section');
        chatSection = document.getElementById('chat-section');
        chatMessages = document.getElementById('chat-messages');
        userInput = document.getElementById('user-input');
        sendBtn = document.getElementById('send-btn');
        loadingOverlay = document.getElementById('loading-overlay');
        loadingText = document.getElementById('loading-text');
        errorModal = document.getElementById('error-modal');
        errorMessage = document.getElementById('error-message');

        // Trigger DOMContentLoaded to initialize event listeners
        document.dispatchEvent(new Event('DOMContentLoaded'));
    });

    describe('File Upload Functionality', () => {
        test('should handle drag and drop events', () => {
            // Test dragover
            dropZone.dispatchEvent(new DragEvent('dragover'));
            expect(dropZone.classList.contains('drag-over')).toBe(true);

            // Test dragleave
            dropZone.dispatchEvent(new DragEvent('dragleave'));
            expect(dropZone.classList.contains('drag-over')).toBe(false);
        });

        test('should handle file drop', async () => {
            const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
            const dropEvent = new DragEvent('drop');
            Object.defineProperty(dropEvent, 'dataTransfer', {
                value: {
                    files: [file]
                }
            });

            fetch.mockImplementationOnce(() => 
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ success: true })
                })
            );

            await dropZone.dispatchEvent(dropEvent);
            
            expect(fetch).toHaveBeenCalledWith('/upload', expect.any(Object));
            expect(uploadStatus.textContent).toBe('File uploaded successfully!');
        });

        test('should reject non-PDF files', async () => {
            const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
            const dropEvent = new DragEvent('drop');
            Object.defineProperty(dropEvent, 'dataTransfer', {
                value: {
                    files: [file]
                }
            });

            await dropZone.dispatchEvent(dropEvent);
            
            expect(errorMessage.textContent).toBe('Please upload a PDF file.');
            expect(fetch).not.toHaveBeenCalled();
        });

        test('should reject files over 10MB', async () => {
            const largeFile = new File(['x'.repeat(11 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' });
            const dropEvent = new DragEvent('drop');
            Object.defineProperty(dropEvent, 'dataTransfer', {
                value: {
                    files: [largeFile]
                }
            });

            await dropZone.dispatchEvent(dropEvent);
            
            expect(errorMessage.textContent).toBe('File size should not exceed 10MB.');
            expect(fetch).not.toHaveBeenCalled();
        });
    });

    describe('Chat Functionality', () => {
        test('should send message and display response', async () => {
            const testMessage = 'Hello, bot!';
            const botResponse = 'Hello, human!';

            userInput.value = testMessage;
            fetch.mockImplementationOnce(() => 
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ response: botResponse })
                })
            );

            await sendBtn.click();

            const messages = chatMessages.querySelectorAll('.message');
            expect(messages[0].textContent).toBe(testMessage);
            expect(messages[0].classList.contains('user')).toBe(true);
            expect(messages[1].textContent).toBe(botResponse);
            expect(messages[1].classList.contains('bot')).toBe(true);
        });

        test('should handle chat API errors', async () => {
            userInput.value = 'Test message';
            fetch.mockImplementationOnce(() => Promise.reject('API Error'));

            await sendBtn.click();

            expect(errorMessage.textContent).toBe('Failed to get response. Please try again.');
        });

        test('should not send empty messages', async () => {
            userInput.value = '   ';
            await sendBtn.click();
            
            expect(fetch).not.toHaveBeenCalled();
            expect(chatMessages.children.length).toBe(0);
        });
    });

    describe('UI State Management', () => {
        test('should show and hide loading overlay', () => {
            const loadingText = 'Loading test...';
            
            // Show loading
            loadingOverlay.classList.remove('hidden');
            loadingText.textContent = loadingText;
            expect(loadingOverlay.classList.contains('hidden')).toBe(false);
            expect(loadingText.textContent).toBe(loadingText);

            // Hide loading
            loadingOverlay.classList.add('hidden');
            expect(loadingOverlay.classList.contains('hidden')).toBe(true);
        });

        test('should show and hide error modal', () => {
            const errorText = 'Test error message';
            
            // Show error
            errorMessage.textContent = errorText;
            errorModal.classList.add('show');
            expect(errorModal.classList.contains('show')).toBe(true);
            expect(errorMessage.textContent).toBe(errorText);

            // Hide error
            window.closeErrorModal();
            expect(errorModal.classList.contains('show')).toBe(false);
        });

        test('should switch from upload to chat section after successful upload', async () => {
            const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
            const dropEvent = new DragEvent('drop');
            Object.defineProperty(dropEvent, 'dataTransfer', {
                value: {
                    files: [file]
                }
            });

            fetch.mockImplementationOnce(() => 
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ success: true })
                })
            );

            await dropZone.dispatchEvent(dropEvent);
            
            // Wait for the transition timeout
            await new Promise(resolve => setTimeout(resolve, 1600));
            
            expect(uploadSection.classList.contains('hidden')).toBe(true);
            expect(chatSection.classList.contains('hidden')).toBe(false);
        });
    });
});