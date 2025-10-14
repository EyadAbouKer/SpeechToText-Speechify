# Speech to Text Converter

A user-friendly desktop application that converts speech from audio and video files into text using OpenAI's Whisper AI model. Perfect for transcribing long recordings, meetings, lectures, podcasts, and more.

## Features

- 🎵 **Multi-format Support**: Works with audio files (MP3, WAV, M4A, FLAC, AAC, OGG, WMA) and video files (MP4, AVI, MOV, MKV, WebM, M4V, 3GP, FLV)
- 🎛️ **Model Selection**: Choose from 5 Whisper models (tiny, base, small, medium, large) for speed vs accuracy control
- 🚀 **GPU Acceleration**: Automatically detects and uses GPU (CUDA/MPS) for faster processing
- ⏱️ **Processing Time Tracking**: Shows exactly how long the transcription took
- 🎯 **High Accuracy**: Uses OpenAI's Whisper models with automatic model selection
- 🖥️ **User-Friendly GUI**: Clean, intuitive interface built with Tkinter
- 📝 **Text Export**: Save transcribed text to files
- ⚡ **Non-blocking UI**: Responsive interface that doesn't freeze during processing
- 🔄 **Progress Tracking**: Visual progress indicators for long files
- 🛡️ **Error Handling**: Comprehensive error handling with helpful messages

## Screenshots

The application features:
- File selection dialog for audio/video files
- Model selection dropdown with 5 Whisper models
- GPU acceleration status display
- Real-time progress tracking with time counter
- Large scrollable text area for transcribed content
- Save functionality for exported text

## Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection (for initial model download)
- PyTorch with CUDA support (optional, for GPU acceleration)

### Step 1: Install Whisper

```bash
pip install -U openai-whisper
```

### Step 2: Download the Application

1. Clone or download this repository
2. Navigate to the project directory

### Step 3: Run the Application

```bash
python main.py
```

## First Run

On the first run, Whisper will automatically download the selected model when you start transcription. Model sizes vary:
- **tiny**: ~39MB
- **base**: ~142MB (default)
- **small**: ~461MB
- **medium**: ~1.5GB
- **large**: ~2.9GB

Each model downloads only once and enables offline transcription afterward.

## GPU Acceleration

The application automatically detects and uses GPU acceleration when available, significantly speeding up transcription:

### Supported GPU Types
- **NVIDIA GPUs**: Uses CUDA acceleration (requires CUDA-compatible PyTorch)
- **Apple Silicon**: Uses MPS acceleration (M1/M2/M3 Macs)
- **CPU Fallback**: Automatically falls back to CPU if no GPU is available

### GPU Setup Instructions

**For NVIDIA GPUs:**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For Apple Silicon (M1/M2/M3):**
```bash
# PyTorch with MPS support (usually included by default)
pip install torch torchvision torchaudio
```

**For CPU only:**
```bash
# Standard PyTorch installation
pip install torch torchvision torchaudio
```

### Performance Benefits

GPU acceleration provides significant speed improvements:

| Model | CPU Time | GPU Time | Speedup |
|-------|----------|----------|---------|
| base  | 6-12 min | 1-3 min  | 3-4x faster |
| small | 10-20 min| 2-5 min  | 4-5x faster |
| medium| 20-40 min| 4-8 min  | 5-6x faster |
| large | 30-60 min| 5-12 min | 6-8x faster |

*Times for 1-hour audio files. Actual speedup depends on your GPU.*

## Usage

### Basic Workflow

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Select Your File**
   - Click "Select Audio/Video File"
   - Choose any supported audio or video file
   - The selected file name will appear below the button

3. **Choose Whisper Model**
   - Select from the dropdown: tiny, base, small, medium, or large
   - See model info (speed vs accuracy trade-off)
   - Default is "base" for good balance
   - GPU status is displayed automatically

4. **Start Transcription**
   - Click "Start Transcription"
   - The application will load the selected Whisper model (if not already loaded)
   - GPU acceleration will be used automatically if available
   - Processing will begin with progress indicators

5. **View Results**
   - Transcribed text will appear in the large text area
   - Processing time will be displayed
   - You can scroll through the text

6. **Save Text (Optional)**
   - Click "Save Text to File"
   - Choose location and filename
   - Text will be saved as a .txt file

### Supported File Formats

**Audio Files:**
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- AAC (.aac)
- OGG (.ogg)
- WMA (.wma)

**Video Files:**
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)
- M4V (.m4v)
- 3GP (.3gp)
- FLV (.flv)

## Whisper Model Selection

The application offers 5 different Whisper models, each with different speed and accuracy characteristics:

### Model Comparison

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **tiny** | ~39MB | Fastest | Basic | Quick tests, low-quality audio |
| **base** | ~142MB | Fast | Good | General use, most files |
| **small** | ~461MB | Moderate | Better | Important documents, clear audio |
| **medium** | ~1.5GB | Slow | High | Professional work, noisy audio |
| **large** | ~2.9GB | Slowest | Best | Critical transcriptions, complex audio |

### Model Selection Guide

**🚀 For Speed (tiny)**
- Use when you need quick results
- Good for testing or previews
- Lower accuracy but very fast processing

**⚖️ For Balance (base) - Recommended**
- Default choice for most users
- Good balance of speed and accuracy
- Suitable for most audio/video files

**🎯 For Accuracy (small/medium/large)**
- Use when accuracy is more important than speed
- Better for professional or important transcriptions
- Larger models handle complex audio better

### Choosing the Right Model

- **1-hour podcast**: Use "base" or "small"
- **Meeting recording**: Use "small" or "medium"
- **Lecture with background noise**: Use "medium" or "large"
- **Quick test**: Use "tiny"
- **Critical transcription**: Use "large"

## Performance Expectations

### Processing Times (Approximate)

*Times vary significantly based on the selected model and your computer's performance.*

| File Length | tiny Model | base Model | small Model | medium Model | large Model |
|-------------|------------|------------|-------------|--------------|-------------|
| 5 minutes   | 15-30 sec  | 30-60 sec  | 1-2 min     | 2-4 min      | 3-6 min      |
| 30 minutes  | 1-2 min    | 3-6 min    | 5-10 min    | 10-20 min    | 15-30 min    |
| 1 hour      | 2-4 min    | 6-12 min   | 10-20 min   | 20-40 min    | 30-60 min    |
| 2 hours     | 4-8 min    | 12-24 min  | 20-40 min   | 40-80 min    | 60-120 min   |

### Model Information

- **Model Used**: Whisper models (tiny, base, small, medium, large)
- **Model Sizes**: 39MB to 2.9GB depending on selection
- **Accuracy**: Varies by model - larger models are more accurate
- **Languages**: Supports 99+ languages automatically
- **Download**: Each model downloads only once

## Troubleshooting

### Common Issues

**"Failed to load Whisper model"**
- Ensure you have a stable internet connection for the first run
- Check that you have sufficient disk space (39MB to 2.9GB depending on model)
- Try running: `pip install --upgrade openai-whisper`
- Try switching to a smaller model if you have limited disk space

**"Transcription failed"**
- Verify your audio/video file is not corrupted
- Ensure the file contains audio content
- Check that the file format is supported

**Slow Performance**
- Close other applications to free up system resources
- Try using a smaller model (tiny or base) for faster processing
- Consider using shorter audio segments for very long files
- Ensure your computer meets the minimum requirements

**GUI Not Responding**
- The application uses threading, so the UI should remain responsive
- If it appears frozen, wait for processing to complete
- Check the progress indicators for current status

### System Requirements

**Minimum:**
- 4GB RAM
- 2GB free disk space (for largest models)
- Python 3.7+

**Recommended:**
- 8GB RAM
- 5GB free disk space
- Modern multi-core processor
- SSD storage (faster model loading)

**For Large Models (medium/large):**
- 16GB RAM recommended
- 10GB free disk space
- Modern CPU with good single-core performance

**For GPU Acceleration:**
- NVIDIA GPU with CUDA support (RTX series recommended)
- Apple Silicon Mac (M1/M2/M3)
- 8GB+ VRAM recommended for large models
- Latest GPU drivers installed

## Advanced Usage

### Command Line Alternative

If you prefer command-line usage, you can also use Whisper directly:

```bash
# Install whisper
pip install openai-whisper

# Transcribe a file
whisper your_audio_file.mp3

# Specify model size
whisper your_audio_file.mp3 --model base

# Output to specific file
whisper your_audio_file.mp3 --output_format txt
```

### Model Options

The application now includes a dropdown menu to select from all available Whisper models:

- `tiny` - Fastest, least accurate (~39MB)
- `base` - Good balance, default (~142MB)
- `small` - Better accuracy, slower (~461MB)
- `medium` - High accuracy, slower (~1.5GB)
- `large` - Best accuracy, slowest (~2.9GB)

You can switch models anytime using the dropdown menu in the GUI.

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source. The Whisper model is provided by OpenAI under the MIT License.

## Acknowledgments

- OpenAI for the amazing Whisper model
- The Python community for excellent libraries
- Contributors and users who provide feedback

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the application
3. Ensure all dependencies are properly installed
4. Check that your file format is supported

---

**Happy Transcribing! 🎤➡️📝**
