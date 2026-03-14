// Open Transcriber - Audio Player and Transcript Sync

let currentTranscriptionData = null;
let isPlaying = false;

// Load Player
function loadPlayer(transcription) {
    currentTranscriptionData = transcription;
    
    const audio = document.getElementById('audio-player');
    
    // Reset state
    isPlaying = false;
    updatePlayButton();
    
    // Set audio source
    console.log('Loading audio from:', `/api/transcriptions/${transcription.id}/audio`);
    audio.src = `/api/transcriptions/${transcription.id}/audio`;
    
    // Render transcript
    renderTranscript(transcription.segments || []);
    
    // Setup audio load handlers first
    setupAudioLoadHandlers(audio);
    
    // Setup audio sync
    setupAudioSync(audio);
    
    // Setup controls
    setupPlayerControls(audio);
}

// Render Transcript
function renderTranscript(segments) {
    const container = document.getElementById('transcript-content');
    
    if (!segments || segments.length === 0) {
        container.innerHTML = '<p class="empty-transcript">No transcript available</p>';
        return;
    }
    
    container.innerHTML = segments.map((segment, idx) => `
        <div class="segment" data-segment-id="${idx}" data-start="${segment.start}" data-end="${segment.end}">
            ${segment.words.map(word => `
                <span class="word" 
                      data-start="${word.start}" 
                      data-end="${word.end}"
                      data-word="${escapeHtml(word.word)}">
                    ${escapeHtml(word.word)}
                </span>
            `).join('')}
        </div>
    `).join('');
}

// Setup Audio Load Handlers
function setupAudioLoadHandlers(audio) {
    // Remove old event listeners
    audio.removeEventListener('canplay', handleCanPlay);
    audio.removeEventListener('loadeddata', handleLoadedData);
    audio.removeEventListener('error', handleAudioError);
    
    // Add new event listeners
    audio.addEventListener('canplay', handleCanPlay);
    audio.addEventListener('loadeddata', handleLoadedData);
    audio.addEventListener('error', handleAudioError);
}

function handleCanPlay() {
    console.log('Audio is ready to play');
    // Audio is ready, enable play button
    const playBtn = document.getElementById('play-btn');
    if (playBtn) {
        playBtn.disabled = false;
    }
}

function handleLoadedData() {
    console.log('Audio data loaded');
    updateTimeDisplay(document.getElementById('audio-player'));
}

function handleAudioError(event) {
    console.error('Audio load error:', event);
    const audio = event.target;
    console.error('Audio error code:', audio.error);
    console.error('Audio src:', audio.src);
    console.error('Audio readyState:', audio.readyState);
    
    let errorMessage = 'Could not load audio file.';
    
    if (audio.error) {
        switch (audio.error.code) {
            case MediaError.MEDIA_ERR_ABORTED:
                errorMessage = 'Audio loading was aborted.';
                break;
            case MediaError.MEDIA_ERR_NETWORK:
                errorMessage = 'Network error while loading audio.';
                break;
            case MediaError.MEDIA_ERR_DECODE:
                errorMessage = 'Audio file could not be decoded.';
                break;
            case MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED:
                errorMessage = 'Audio file not found or format not supported.';
                console.error('Transcription ID:', currentTranscriptionData?.id);
                break;
        }
    }
    
    showError(errorMessage + ' Please check if the transcription exists and the audio file is available.');
}

// Setup Audio Sync
function setupAudioSync(audio) {
    // Remove old listeners to avoid duplicates
    audio.removeEventListener('timeupdate', handleTimeUpdate);
    audio.removeEventListener('play', handlePlay);
    audio.removeEventListener('pause', handlePause);
    audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
    
    // Add event listeners
    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('play', handlePlay);
    audio.addEventListener('pause', handlePause);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
}

function handleTimeUpdate() {
    const audio = this;
    const currentTime = audio.currentTime;
    
    // Remove all highlights
    document.querySelectorAll('.word.active').forEach(el => {
        el.classList.remove('active');
    });
    
    // Find current word
    const currentWord = findWordAtTime(currentTime);
    
    if (currentWord) {
        currentWord.classList.add('active');
        
        // Scroll into view if needed
        scrollWordIntoView(currentWord);
    }
    
    // Update time display
    updateTimeDisplay(audio);
}

function handlePlay() {
    isPlaying = true;
    updatePlayButton();
}

function handlePause() {
    isPlaying = false;
    updatePlayButton();
}

function handleLoadedMetadata() {
    updateTimeDisplay(this);
}

// Find Word at Time
function findWordAtTime(time) {
    const words = document.querySelectorAll('.word');
    let closestWord = null;
    let minDiff = Infinity;
    
    words.forEach(word => {
        const start = parseFloat(word.dataset.start);
        const end = parseFloat(word.dataset.end);
        
        // Check if time is within word range
        if (time >= start && time <= end) {
            return word;
        }
        
        // Find closest word if not in range
        const diff = Math.min(Math.abs(time - start), Math.abs(time - end));
        if (diff < minDiff && diff < 0.5) {
            minDiff = diff;
            closestWord = word;
        }
    });
    
    // If we found a word in range, return it
    for (const word of words) {
        const start = parseFloat(word.dataset.start);
        const end = parseFloat(word.dataset.end);
        if (time >= start && time <= end) {
            return word;
        }
    }
    
    // Otherwise return closest word
    return closestWord;
}

// Scroll Word into View
function scrollWordIntoView(word) {
    const container = document.getElementById('transcript-content');
    const containerRect = container.getBoundingClientRect();
    const wordRect = word.getBoundingClientRect();
    
    // Check if word is outside visible area
    if (wordRect.top < containerRect.top || wordRect.bottom > containerRect.bottom) {
        word.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// Setup Player Controls
function setupPlayerControls(audio) {
    // Play/Pause button
    const playBtn = document.getElementById('play-btn');
    playBtn.removeEventListener('click', togglePlay);
    playBtn.addEventListener('click', togglePlay);
    
    // Rewind button
    const rewBtn = document.getElementById('rew-btn');
    rewBtn.onclick = () => {
        audio.currentTime = Math.max(0, audio.currentTime - 5);
    };
    
    // Forward button
    const fwdBtn = document.getElementById('fwd-btn');
    fwdBtn.onclick = () => {
        audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
    };
    
    // Click on word to jump
    document.getElementById('transcript-content').addEventListener('click', (e) => {
        if (e.target.classList.contains('word')) {
            const start = parseFloat(e.target.dataset.start);
            audio.currentTime = start;
            audio.play().catch(err => console.error('Error playing:', err));
        }
    });
    
    // Keyboard shortcuts
    document.removeEventListener('keydown', handleKeyPress);
    document.addEventListener('keydown', handleKeyPress);
}

function handleKeyPress(e) {
    // Only handle if not in an input field
    if (e.target.matches('input, textarea, select')) {
        return;
    }
    
    const audio = document.getElementById('audio-player');
    
    switch (e.code) {
        case 'Space':
            e.preventDefault();
            togglePlay();
            break;
        case 'ArrowLeft':
            e.preventDefault();
            audio.currentTime = Math.max(0, audio.currentTime - 5);
            break;
        case 'ArrowRight':
            e.preventDefault();
            audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
            break;
    }
}

// Toggle Play/Pause
function togglePlay() {
    const audio = document.getElementById('audio-player');
    
    console.log('Toggle play called, readyState:', audio.readyState);
    console.log('Audio src:', audio.src);
    
    // Check if audio is ready
    if (audio.readyState === 0) {
        console.error('Audio not loaded yet');
        showError('Audio is still loading. Please wait a moment.');
        return;
    }
    
    if (isPlaying) {
        audio.pause();
    } else {
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            console.error('Audio error:', audio.error);
            showError('Could not play audio: ' + error.message);
        });
    }
}

// Update Play Button
function updatePlayButton() {
    const playBtn = document.getElementById('play-btn');
    
    if (isPlaying) {
        playBtn.textContent = '⏸️ Pause';
    } else {
        playBtn.textContent = '▶️ Play';
    }
}

// Update Time Display
function updateTimeDisplay(audio) {
    const display = document.getElementById('time-display');
    const current = audio.currentTime || 0;
    const duration = audio.duration || 0;
    
    display.textContent = `${formatTime(current)} / ${formatTime(duration)}`;
}

// Format Time
function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show error to user
function showError(message) {
    // Simple alert for now, could be enhanced
    alert(message);
}

// Make function available globally
window.loadPlayer = loadPlayer;
