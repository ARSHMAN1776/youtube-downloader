# YouTube Downloader

A simple YouTube video downloader with Python backend and web interface.

## Features

- Download YouTube videos
- Simple web interface
- Choose video quality
- MP4 format support

## Requirements

- Python 3.8+
- yt-dlp

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py
```

Open your browser and go to `http://localhost:5000`

## Project Structure

```
youtube-downloader/
├── app.py              # Flask app
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html     # Frontend
└── downloads/         # Downloaded videos
```

## How to Use

1. Start the application
2. Paste YouTube URL
3. Click Download
4. Video saves to `downloads/` folder

## Dependencies

```
Flask==3.0.0
yt-dlp==2023.12.30
```

## License

MIT License

## Disclaimer

For educational purposes only. Respect YouTube's Terms of Service.
