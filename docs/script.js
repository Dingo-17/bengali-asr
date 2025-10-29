// ===== Configuration =====
const API_URL = 'https://bengali-asr-demo.onrender.com';  // Live Render backend

// ===== Mobile Menu Toggle =====
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
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
}

// ===== Smooth Scrolling =====
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

// ===== Audio Upload and Transcription =====
const audioFileInput = document.getElementById('audioFile');
const uploadArea = document.getElementById('uploadArea');
const transcribeBtn = document.getElementById('transcribeBtn');
const resultArea = document.getElementById('resultArea');

let selectedFile = null;

// Handle file selection
if (audioFileInput) {
    audioFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

// Handle drag and drop
if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#A66F5B';
        uploadArea.style.background = '#FBF2ED';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#D6D9CC';
        uploadArea.style.background = '#FBF2ED';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#D6D9CC';
        uploadArea.style.background = '#FBF2ED';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    uploadArea.addEventListener('click', () => {
        audioFileInput.click();
    });
}

// Handle file selection
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/mpeg', 'audio/x-m4a'];
    const validExtensions = /\.(mp3|wav|m4a|ogg)$/i;
    
    if (!validTypes.includes(file.type) && !file.name.match(validExtensions)) {
        showNotification('Please upload a valid audio file (MP3, WAV, M4A, or OGG)', 'error');
        return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }

    selectedFile = file;
    
    // Show file name
    const fileName = document.createElement('p');
    fileName.textContent = `Selected: ${file.name}`;
    fileName.style.marginTop = '1rem';
    fileName.style.color = '#A66F5B';
    fileName.style.fontWeight = '600';
    
    // Clear previous file name if exists
    const existingFileName = uploadArea.querySelector('p[style*="margin-top"]');
    if (existingFileName) {
        existingFileName.remove();
    }
    uploadArea.appendChild(fileName);

    // Enable transcribe button
    if (transcribeBtn) {
        transcribeBtn.disabled = false;
        transcribeBtn.style.opacity = '1';
        transcribeBtn.style.cursor = 'pointer';
    }

    showNotification(`File "${file.name}" ready for transcription`, 'success');
}

// Handle transcription
if (transcribeBtn) {
    transcribeBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            showNotification('Please select an audio file first', 'error');
            return;
        }

        await transcribeAudio(selectedFile);
    });
}

// Transcribe audio using backend API
async function transcribeAudio(file) {
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    // Show loading state
    if (btnText && btnLoader) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        transcribeBtn.disabled = true;
    }

    try {
        // Create form data
        const formData = new FormData();
        formData.append('audio', file);
        formData.append('language', 'bn');

        // Call API
        const response = await fetch(`${API_URL}/transcribe`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        // Display results
        displayTranscription(data);
        showNotification('Transcription complete!', 'success');

    } catch (error) {
        console.error('Transcription error:', error);
        showNotification(`Error: ${error.message}. Make sure the API server is running.`, 'error');
    } finally {
        // Reset button state
        if (btnText && btnLoader) {
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            transcribeBtn.disabled = false;
        }
    }
}

// Display transcription results
function displayTranscription(data) {
    const bengaliText = document.getElementById('bengaliText');
    const latinText = document.getElementById('latinText');
    const ipaText = document.getElementById('ipaText');
    const confidenceScore = document.getElementById('confidenceScore');
    const demoResult = document.getElementById('demoResult');

    if (bengaliText) {
        bengaliText.textContent = data.transcript_bangla || data.transcript || 'No transcription available';
    }

    if (latinText) {
        latinText.textContent = data.transcript_latin || convertToLatin(data.transcript_bangla) || 'Not available';
    }

    if (ipaText) {
        ipaText.textContent = data.transcript_ipa || 'Not available';
    }

    if (confidenceScore) {
        const confidence = (data.confidence * 100).toFixed(1);
        confidenceScore.textContent = `${confidence}%`;
        confidenceScore.style.color = confidence > 80 ? '#10b981' : confidence > 60 ? '#f59e0b' : '#ef4444';
    }

    if (demoResult) {
        demoResult.style.display = 'block';
    }
}

// Simple Bengali to Latin conversion (fallback)
function convertToLatin(bengaliText) {
    // This is a very basic transliteration - backend should provide better one
    const mapping = {
        'আ': 'a', 'ই': 'i', 'উ': 'u', 'এ': 'e', 'ও': 'o',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'y', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh',
        'স': 's', 'হ': 'h', 'া': 'a', 'ি': 'i', 'ী': 'i',
        'ু': 'u', 'ূ': 'u', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o',
        'ৌ': 'ou'
    };
    
    let result = '';
    for (let char of bengaliText) {
        result += mapping[char] || char;
    }
    return result;
}

// Tab switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Remove active from all tabs
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        // Add active to clicked tab
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Copy text to clipboard
const copyBtn = document.getElementById('copyBtn');
if (copyBtn) {
    copyBtn.addEventListener('click', () => {
        const activeTab = document.querySelector('.tab-content.active');
        const text = activeTab.querySelector('.result-text').textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Text copied to clipboard!', 'success');
        }).catch(err => {
            showNotification('Failed to copy text', 'error');
        });
    });
}

// Download transcription
const downloadBtn = document.getElementById('downloadBtn');
if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
        const bengaliText = document.getElementById('bengaliText').textContent;
        const latinText = document.getElementById('latinText').textContent;
        
        const content = `Bengali ASR Transcription\n\nBengali:\n${bengaliText}\n\nLatin:\n${latinText}\n\nGenerated: ${new Date().toLocaleString()}`;
        
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transcription.txt';
        a.click();
        URL.revokeObjectURL(url);
        
        showNotification('Transcription downloaded!', 'success');
    });
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-size: 0.95rem;
        font-weight: 500;
        max-width: 400px;
    `;

    document.body.appendChild(notification);

    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Add CSS animations
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

// Check API health on page load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✓ API server is running');
        }
    } catch (error) {
        console.warn('⚠ API server not accessible. Transcription will not work until you start the server.');
        console.log('To start the server, run: cd inference && python server.py');
    }
}

// Check API on load
window.addEventListener('load', () => {
    checkAPIHealth();
});
