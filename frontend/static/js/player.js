// Open Transcriber - Audio Player and Transcript Sync

let currentTranscriptionData = null;
let isPlaying = false;

// Load Player
function loadPlayer(transcription) {
    currentTranscriptionData = transcription;
    
    const audio = document.getElementById('audio-player');
    
    // Set audio source
    audio.src = `/api/transcriptions/${transcription.id}/audio`;
    
    // Render transcript
    renderTranscript(transcription.segments || []);
    
    // Setup audio sync
    setupAudioSync(audio);
    
    // Setup controls
    setupPlayerControls(audio);
    
    // Reset state
    isPlaying = false;
    updatePlayButton();
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

// Setup Audio Sync
function setupAudioSync(audio) {
    audio.addEventListener('timeupdate', () => {
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
    });
    
    audio.addEventListener('play', () => {
        isPlaying = true;
        updatePlayButton();
    });
    
    audio.addEventListener('pause', () => {
        isPlaying = false;
        updatePlayButton();
    });
    
    audio.addEventListener('loadedmetadata', () => {
        updateTimeDisplay(audio);
    });
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
    document.getElementById('play-btn').addEventListener('click', togglePlay);
    
    // Rewind button
    document.getElementById('rew-btn').addEventListener('click', () => {
        audio.currentTime = Math.max(0, audio.currentTime - 5);
    });
    
    // Forward button
    document.getElementById('fwd-btn').addEventListener('click', () => {
        audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
    });
    
    // Click on word to jump
    document.getElementById('transcript-content').addEventListener('click', (e) => {
        if (e.target.classList.contains('word')) {
            const start = parseFloat(e.target.dataset.start);
            audio.currentTime = start;
            audio.play();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Only handle if not in an input field
        if (e.target.matches('input, textarea, select')) {
            return;
        }
        
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
    });
}

// Toggle Play/Pause
function togglePlay() {
    const audio = document.getElementById('audio-player');
    
    if (isPlaying) {
        audio.pause();
    } else {
        audio.play();
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

// Make function available globally
window.loadPlayer = loadPlayer;
