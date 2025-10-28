import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [transcript, setTranscript] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showLatin, setShowLatin] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setAudioFile(file);
    setAudioUrl(URL.createObjectURL(file));
    setTranscript(null);
    setError(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
    },
    maxSize: 100 * 1024 * 1024, // 100MB
    multiple: false
  });

  const handleTranscribe = async () => {
    if (!audioFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('audio', audioFile);
    formData.append('language', 'bn');
    formData.append('include_latin', 'true');

    try {
      const response = await axios.post(`${API_URL}/transcribe`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload progress: ${percentCompleted}%`);
        },
      });

      setTranscript(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Transcription failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadTxt = () => {
    if (!transcript) return;
    
    const text = showLatin ? transcript.transcript_latin : transcript.transcript_bangla;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript_${Date.now()}.txt`;
    a.click();
  };

  const downloadSrt = () => {
    if (!transcript) return;
    
    const text = showLatin ? transcript.transcript_latin : transcript.transcript_bangla;
    // Simple SRT format (single subtitle)
    const srt = `1\n00:00:00,000 --> 00:00:10,000\n${text}\n`;
    
    const blob = new Blob([srt], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript_${Date.now()}.srt`;
    a.click();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-indigo-900 dark:text-white mb-4">
            🎙️ Bengali ASR
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Automatic Speech Recognition for Bengali Dialects
          </p>
        </header>

        {/* Upload Area */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <div
            {...getRootProps()}
            className={`border-4 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
              isDragActive
                ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-indigo-400'
            }`}
          >
            <input {...getInputProps()} />
            <div className="text-6xl mb-4">📁</div>
            {audioFile ? (
              <p className="text-lg text-gray-700 dark:text-gray-200 font-semibold">
                Selected: {audioFile.name}
              </p>
            ) : (
              <>
                <p className="text-lg text-gray-700 dark:text-gray-200 mb-2">
                  {isDragActive
                    ? 'Drop the audio file here...'
                    : 'Drag & drop an audio file, or click to select'}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Supported: WAV, MP3, OGG, FLAC, M4A (max 100MB)
                </p>
              </>
            )}
          </div>

          {/* Audio Player */}
          {audioUrl && (
            <div className="mt-6">
              <audio controls className="w-full" src={audioUrl}>
                Your browser does not support the audio element.
              </audio>
            </div>
          )}

          {/* Transcribe Button */}
          {audioFile && (
            <button
              onClick={handleTranscribe}
              disabled={loading}
              className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-4 px-6 rounded-xl transition-colors text-lg shadow-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Transcribing...
                </span>
              ) : (
                'Transcribe Audio'
              )}
            </button>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg">
              <p className="font-semibold">Error:</p>
              <p>{error}</p>
            </div>
          )}
        </div>

        {/* Transcript Display */}
        {transcript && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
                Transcript
              </h2>
              
              {/* Toggle Script */}
              <button
                onClick={() => setShowLatin(!showLatin)}
                className="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                {showLatin ? '🇧🇩 Bangla' : '🔤 Latin'}
              </button>
            </div>

            {/* Transcript Text */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 mb-6">
              <p className="text-2xl text-gray-800 dark:text-gray-200 leading-relaxed" style={{ fontFamily: showLatin ? 'inherit' : 'Noto Sans Bengali, sans-serif' }}>
                {showLatin ? transcript.transcript_latin : transcript.transcript_bangla}
              </p>
            </div>

            {/* Metadata */}
            <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
              <div className="bg-indigo-50 dark:bg-indigo-900/30 rounded-lg p-3">
                <p className="text-gray-600 dark:text-gray-400">Confidence</p>
                <p className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
                  {(transcript.confidence * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-3">
                <p className="text-gray-600 dark:text-gray-400">Processing Time</p>
                <p className="text-xl font-bold text-green-600 dark:text-green-400">
                  {transcript.processing_time_ms.toFixed(0)}ms
                </p>
              </div>
            </div>

            {/* Download Buttons */}
            <div className="flex gap-4">
              <button
                onClick={downloadTxt}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                📄 Download .txt
              </button>
              <button
                onClick={downloadSrt}
                className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                📝 Download .srt
              </button>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-600 dark:text-gray-400">
          <p>Powered by BRAC Data Science Team | Open Source</p>
          <p className="text-sm mt-2">
            <a href="https://github.com/BRAC/bengali-dialect-transcription" className="text-indigo-600 dark:text-indigo-400 hover:underline">
              View on GitHub
            </a>
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
