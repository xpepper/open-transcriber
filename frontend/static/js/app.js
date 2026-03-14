// Open Transcriber - Main Application Logic

// State
let currentTranscription = null;
let allTranscriptions = [];
let transcriptionToDelete = null;

// DOM Elements
const libraryView = document.getElementById('library-view');
const viewerView = document.getElementById('viewer-view');
const transcriptionsList = document.getElementById('transcriptions-list');
const uploadModal = document.getElementById('upload-modal');
const deleteModal = document.getElementById('delete-modal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTranscriptionsList();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Upload button
    document.getElementById('upload-btn').addEventListener('click', showUploadModal);
    
    // Close modal
    document.getElementById('close-modal').addEventListener('click', hideUploadModal);
    document.getElementById('browse-btn').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });
    
    // File input
    document.getElementById('file-input').addEventListener('change', handleFileSelect);
    
    // Drag and drop
    const dropZone = document.getElementById('drop-zone');
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    // Back button
    document.getElementById('back-btn').addEventListener('click', showLibrary);
    
    // Delete button
    document.getElementById('delete-btn').addEventListener('click', () => {
        if (currentTranscription) {
            showDeleteModal(currentTranscription);
        }
    });
    
    // Delete modal
    document.getElementById('close-delete-modal').addEventListener('click', hideDeleteModal);
    document.getElementById('confirm-delete-btn').addEventListener('click', confirmDelete);
    document.getElementById('cancel-delete-btn').addEventListener('click', hideDeleteModal);
    
    // Duplicate handling
    document.getElementById('view-duplicate-btn').addEventListener('click', handleViewDuplicate);
    document.getElementById('cancel-duplicate-btn').addEventListener('click', () => {
        hideUploadModal();
    });
    
    // Close modals on backdrop click
    uploadModal.addEventListener('click', (e) => {
        if (e.target === uploadModal) {
            hideUploadModal();
        }
    });
    
    deleteModal.addEventListener('click', (e) => {
        if (e.target === deleteModal) {
            hideDeleteModal();
        }
    });
}

// Load Transcriptions List
async function loadTranscriptionsList() {
    try {
        const response = await fetch('/api/transcriptions');
        if (!response.ok) {
            throw new Error('Failed to load transcriptions');
        }
        
        allTranscriptions = await response.json();
        renderLibrary();
    } catch (error) {
        console.error('Error loading transcriptions:', error);
        showError('Failed to load transcriptions. Please refresh the page.');
    }
}

// Render Library
function renderLibrary() {
    if (allTranscriptions.length === 0) {
        transcriptionsList.innerHTML = `
            <div class="empty-state">
                <h2>📚 No lectures yet</h2>
                <p>Upload your first audio recording to get started</p>
            </div>
        `;
        return;
    }
    
    transcriptionsList.innerHTML = allTranscriptions.map(t => `
        <div class="transcription-card" data-id="${t.id}">
            <h3>📄 ${escapeHtml(t.original_filename)}</h3>
            <div class="metadata">
                ${formatDate(t.created_at)} • 
                ${formatDuration(t.duration)} • 
                ${getLanguageName(t.language)} • 
                ${t.model_used} model • 
                ${t.word_count?.toLocaleString() || 0} words
            </div>
            <div class="actions">
                <button class="btn btn-primary" onclick="viewTranscription('${t.id}')">
                    View
                </button>
                <button class="btn btn-danger" onclick="deleteTranscriptionDirect('${t.id}')">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

// View Transcription
async function viewTranscription(id) {
    try {
        const response = await fetch(`/api/transcriptions/${id}`);
        if (!response.ok) {
            throw new Error('Failed to load transcription');
        }
        
        currentTranscription = await response.json();
        
        // Update title
        document.getElementById('lecture-title').textContent = 
            currentTranscription.metadata.original_filename;
        
        // Update metadata
        const metadata = currentTranscription.metadata;
        document.getElementById('audio-metadata').innerHTML = `
            ${formatDate(metadata.created_at)} • 
            ${formatDuration(metadata.duration)} • 
            ${getLanguageName(metadata.language)} • 
            ${metadata.model_used} model
        `;
        
        // Switch to viewer view
        libraryView.classList.remove('active');
        libraryView.classList.add('hidden');
        viewerView.classList.remove('hidden');
        viewerView.classList.add('active');
        
        // Load player and transcript
        loadTranscriptionContent(currentTranscription);
        
    } catch (error) {
        console.error('Error viewing transcription:', error);
        showError('Failed to load transcription. Please try again.');
    }
}

// Load Transcription Content (delegated to player.js)
function loadTranscriptionContent(transcription) {
    if (typeof loadPlayer === 'function') {
        loadPlayer(transcription);
    }
}

// Show Library
function showLibrary() {
    viewerView.classList.remove('active');
    viewerView.classList.add('hidden');
    libraryView.classList.remove('hidden');
    libraryView.classList.add('active');
    
    // Stop audio
    const audio = document.getElementById('audio-player');
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }
    
    currentTranscription = null;
    
    // Reload list
    loadTranscriptionsList();
}

// Upload Modal
function showUploadModal() {
    uploadModal.classList.remove('hidden');
    
    // Reset state
    document.getElementById('drop-zone').classList.remove('hidden');
    document.getElementById('upload-progress').classList.add('hidden');
    document.getElementById('duplicate-message').classList.add('hidden');
    document.getElementById('file-input').value = '';
}

function hideUploadModal() {
    uploadModal.classList.add('hidden');
}

// File Selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

// File Upload
async function handleFileUpload(file) {
    // Validate file type
    const validTypes = ['audio/mpeg', 'audio/mp4', 'audio/wav', 'audio/m4a', 'audio/mp3'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const validExtensions = ['mp3', 'm4a', 'wav', 'wma', 'ogg', 'mp4', 'mpeg'];
    
    if (!validExtensions.includes(fileExtension)) {
        showError('Please upload a valid audio file (MP3, M4A, WAV, etc.)');
        return;
    }
    
    // Show progress
    document.getElementById('drop-zone').classList.add('hidden');
    document.getElementById('upload-progress').classList.remove('hidden');
    document.getElementById('duplicate-message').classList.add('hidden');
    
    // Prepare form data
    const formData = new FormData();
    formData.append('audio', file);
    formData.append('model', document.getElementById('model-select').value);
    
    try {
        const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Transcription failed');
        }
        
        const result = await response.json();
        
        if (result.status === 'duplicate') {
            // Show duplicate message
            document.getElementById('upload-progress').classList.add('hidden');
            document.getElementById('duplicate-message').classList.remove('hidden');
            
            // Store for potential view
            currentTranscription = result.transcription;
        } else {
            // Success
            hideUploadModal();
            await loadTranscriptionsList();
            viewTranscription(result.transcription.id);
        }
        
    } catch (error) {
        console.error('Error uploading file:', error);
        showError(error.message || 'Failed to transcribe file. Please try again.');
        hideUploadModal();
    }
}

// Delete Transcription
function deleteTranscriptionDirect(id) {
    const transcription = allTranscriptions.find(t => t.id === id);
    if (transcription) {
        showDeleteModal(transcription);
    }
}

function showDeleteModal(transcription) {
    transcriptionToDelete = transcription;
    deleteModal.classList.remove('hidden');
}

function hideDeleteModal() {
    deleteModal.classList.add('hidden');
    transcriptionToDelete = null;
}

async function confirmDelete() {
    if (!transcriptionToDelete) return;
    
    try {
        const response = await fetch(`/api/transcriptions/${transcriptionToDelete.id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete transcription');
        }
        
        hideDeleteModal();
        
        // If viewing the deleted transcription, go back to library
        if (currentTranscription && currentTranscription.id === transcriptionToDelete.id) {
            showLibrary();
        } else {
            loadTranscriptionsList();
        }
        
    } catch (error) {
        console.error('Error deleting transcription:', error);
        showError('Failed to delete transcription. Please try again.');
        hideDeleteModal();
    }
}

// Handle View Duplicate
function handleViewDuplicate() {
    if (currentTranscription) {
        hideUploadModal();
        viewTranscription(currentTranscription.id);
    }
}

// Utility Functions
function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
        });
    } catch {
        return dateString;
    }
}

function formatDuration(seconds) {
    if (!seconds) return '0:00';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

function getLanguageName(code) {
    const languageMap = {
        'en': 'English',
        'it': 'Italian',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi'
    };
    return languageMap[code] || code.toUpperCase();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showError(message) {
    alert(message); // Simple alert for now, could be enhanced with a toast notification
}

// Make functions available globally
window.viewTranscription = viewTranscription;
window.deleteTranscriptionDirect = deleteTranscriptionDirect;
