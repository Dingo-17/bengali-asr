// Mobile Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Upload Area - Drag and Drop
const uploadArea = document.getElementById('uploadArea');
const audioFile = document.getElementById('audioFile');
const resultArea = document.getElementById('resultArea');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.background = '#eff6ff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.background = 'var(--light-bg)';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.background = 'var(--light-bg)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

audioFile.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

function handleFileUpload(file) {
    // Validate file type
    const validTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/mpeg'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|m4a|ogg)$/i)) {
        alert('Please upload a valid audio file (MP3, WAV, M4A, or OGG)');
        return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    // Show processing message
    showNotification('Processing audio file...', 'info');

    // Simulate transcription (replace with actual API call)
    setTimeout(() => {
        showTranscriptionResult();
        showNotification('Transcription complete!', 'success');
    }, 2000);
}

// Recording Functionality
let mediaRecorder;
let audioChunks = [];
let recordingTimer;
let recordingSeconds = 0;

const recordBtn = document.getElementById('recordBtn');
const recordingStatus = document.getElementById('recordingStatus');
const recordingTime = document.getElementById('recordingTime');

recordBtn.addEventListener('click', async () => {
    if (recordBtn.textContent.includes('Start')) {
        await startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        recordingSeconds = 0;

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            // Process the recording (replace with actual API call)
            showNotification('Processing recording...', 'info');
            setTimeout(() => {
                showTranscriptionResult();
                showNotification('Transcription complete!', 'success');
            }, 2000);
        };

        mediaRecorder.start();
        recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
        recordBtn.style.background = '#ef4444';
        recordingStatus.classList.remove('hidden');

        // Update recording timer
        recordingTimer = setInterval(() => {
            recordingSeconds++;
            const minutes = Math.floor(recordingSeconds / 60);
            const seconds = recordingSeconds % 60;
            recordingTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);

    } catch (error) {
        console.error('Error accessing microphone:', error);
        showNotification('Could not access microphone. Please check permissions.', 'error');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        recordBtn.style.background = 'var(--error-color)';
        recordingStatus.classList.add('hidden');
        clearInterval(recordingTimer);
    }
}

// Tab Switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.dataset.tab;
        
        // Remove active class from all buttons and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        btn.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
});

// Show Transcription Result
function showTranscriptionResult() {
    resultArea.classList.remove('hidden');
    resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Copy to Clipboard
const copyBtns = document.querySelectorAll('.result-actions .btn-secondary');
if (copyBtns[0]) {
    copyBtns[0].addEventListener('click', () => {
        const activeTab = document.querySelector('.tab-content.active');
        const text = activeTab.querySelector('.result-text').textContent;
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        });
    });
}

// Download Result
if (copyBtns[1]) {
    copyBtns[1].addEventListener('click', () => {
        const activeTab = document.querySelector('.tab-content.active');
        const text = activeTab.querySelector('.result-text').textContent;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transcription.txt';
        a.click();
        URL.revokeObjectURL(url);
        showNotification('Downloading transcription...', 'success');
    });
}

// Share Result
if (copyBtns[2]) {
    copyBtns[2].addEventListener('click', () => {
        const activeTab = document.querySelector('.tab-content.active');
        const text = activeTab.querySelector('.result-text').textContent;
        
        if (navigator.share) {
            navigator.share({
                title: 'Bengali Transcription',
                text: text
            }).then(() => {
                showNotification('Shared successfully!', 'success');
            }).catch(() => {
                // Fallback to copy
                navigator.clipboard.writeText(text);
                showNotification('Copied to clipboard (share not available)', 'info');
            });
        } else {
            // Fallback to copy
            navigator.clipboard.writeText(text);
            showNotification('Copied to clipboard!', 'success');
        }
    });
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Scroll Animation for Elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.feature-card, .doc-card, .contact-item').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
});

// Active nav link on scroll
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section[id]');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

console.log('🎙️ BRAC Bengali ASR System - Website Loaded');
console.log('Note: This is a demo interface. For production use, connect to the API server.');
