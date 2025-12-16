# Media Converter

A Python script to convert HEIC images to PNG, MOV videos to MP4, and automatically extract and process ZIP archives containing these files.

## Features

- **HEIC to PNG**: Converts High Efficiency Image Container files to standard PNG images.
- **MOV to MP4**: Converts Apple QuickTime movies to proper MP4 video files with AAC audio.
- **Zip Support**: Automatically extracts `.zip` archives and processes all compatible media files found within.
- **Batch Processing**: Recursively scans directories when handling zip files.

## Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/) (usually handled automatically by `moviepy`, but may be needed on system path)

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Single File
Convert a single `.heic` or `.mov` file:
```bash
python converter.py path/to/image.heic
```
This will create `path/to/image.png`.

### Zip Archive
Extract and convert a zip file:
```bash
python converter.py path/to/archive.zip
```
This will:
1. Extract `archive.zip` to a folder named `extracted_archive` in the same directory.
2. Recursively find and convert all `.heic` and `.mov` files within that folder.

## Troubleshooting

- **FFmpeg not found**: If you encounter errors related to `moviepy` or `ffmpeg`, ensure you have FFmpeg installed and added to your system PATH, or let `imageio-ffmpeg` (installed with moviepy) handle it.
