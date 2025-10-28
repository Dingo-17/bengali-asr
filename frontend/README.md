# Bengali ASR Frontend

React-based web interface for Bengali speech-to-text transcription.

## Features

- 🎤 Drag & drop audio file upload
- ▶️ Audio player with preview
- 🔄 Real-time transcription progress
- 🌐 Toggle between Bangla script and Latin phonetic
- 💾 Download transcripts as .txt or .srt
- 📱 Responsive design (mobile & desktop)
- ♿ WCAG 2.1 AA accessible
- 🎨 Tailwind CSS styling with dark mode

## Tech Stack

- **React** 18+ (with Vite)
- **Tailwind CSS** for styling
- **Axios** for API requests
- **Wavesurfer.js** for audio visualization
- **React Dropzone** for file uploads

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_API_KEY=your_api_key  # Optional
```

## Deployment

### GitHub Pages

```bash
# Build and deploy
cd ..
bash scripts/deploy_frontend.sh
```

### Vercel

```bash
npm i -g vercel
vercel --prod
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

## Configuration

Edit `src/config.js` to customize:
- API endpoint
- Supported file formats
- Max file size
- UI theme colors

## Project Structure

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── AudioUploader.jsx
│   │   ├── AudioPlayer.jsx
│   │   ├── TranscriptDisplay.jsx
│   │   └── DownloadButtons.jsx
│   ├── utils/
│   │   ├── api.js
│   │   └── srtGenerator.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## API Integration

The frontend communicates with the backend API:

```javascript
// Transcribe audio
const response = await axios.post('/transcribe', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

// Response format
{
  "transcript_bangla": "আমি বাংলায় কথা বলি",
  "transcript_latin": "ami banglay kotha boli",
  "confidence": 0.95,
  "tokens": ["আমি", "বাংলায়", "কথা", "বলি"],
  "processing_time_ms": 1234.56
}
```

## Accessibility

- Keyboard navigation support
- Screen reader compatible
- ARIA labels for all interactive elements
- High contrast mode
- Focus indicators
- Error announcements

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

MIT License - see [LICENSE](../LICENSE) file.

## Support

For issues or questions:
- GitHub Issues: https://github.com/BRAC/bengali-dialect-transcription/issues
- Email: [TODO: Add contact email]

---

*Last Updated: October 29, 2025*
