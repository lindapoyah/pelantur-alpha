# pelantur-alpha

A simple desktop application built with Python and Tkinter to generate slideshow videos from images, voice narration, and background music using FFmpeg.

This tool is designed to quickly create narrated slideshow videos automatically, where the duration of each image follows the length of the voice narration.

---

# Features

- Create slideshow video from multiple images
- Automatically sync slideshow duration with voice narration
- Optional background music
- Adjustable background music volume
- 3-second delay after narration finishes
- Automatic audio fade-out at the end
- Fade-to-black transition between images
- Export video in MP4 format (H264 + AAC)
- Simple desktop GUI

---

# How It Works

The application workflow:

1. User selects voice narration audio
2. User selects multiple images
3. User optionally selects background music
4. The program calculates:

```
image_duration = (voice_duration + 3 seconds) / number_of_images
```

5. Each image is converted to a short video clip
6. Fade in/out transitions are applied
7. All clips are concatenated into a slideshow
8. Voice and background music are mixed
9. Final video is exported using FFmpeg

---

# Requirements

Make sure the following software is installed.

## Python

Python 3.8 or newer

## FFmpeg

This application requires **FFmpeg** installed and available in the system PATH.

Download FFmpeg:

https://ffmpeg.org/download.html

Verify installation:

```bash
ffmpeg -version
```

---

# Python Dependencies

Install required Python packages:

```bash
pip install pydub
```

---

# Project Structure

```
project-folder
│
├── app.py
├── README.md
```

Temporary files created during rendering:

```
temp_*.mp4
slideshow.mp4
concat.txt
audio_mix.m4a
```

These files are automatically reused and overwritten.

---

# How To Run

Clone the repository:

```bash
git clone https://github.com/yourusername/slideshow-generator.git
```

Enter the folder:

```bash
cd slideshow-generator
```

Run the application:

```bash
python app.py
```

---

# Application Interface

The application contains two main panels.

## Left Panel – Settings

Used to configure input media.

Options:

- Upload Voice narration
- Upload Images
- Upload Background Music
- Adjust Music Volume

## Right Panel – Output Settings

Used to configure video output.

Options:

- Output file name
- Output folder
- Render video button

---

# Output Video Settings

The generated video uses:

```
Resolution: 1280x720
Frame rate: 24 fps
Video codec: H264 (libx264)
Audio codec: AAC
Container: MP4
```

---

# Video Behavior

After the narration ends:

- Background music continues for **3 seconds**
- Audio then fades out smoothly
- Video ends after fade out

---

# Supported File Formats

Voice narration:

```
mp3
wav
m4a
```

Background music:

```
mp3
wav
```

Images:

```
jpg
jpeg
png
```

---

# Known Limitations

- No image preview inside the application
- Images are resized automatically to 1280x720
- Temporary files are generated during rendering

---

# Future Improvements

Possible enhancements:

- Drag & drop image ordering
- Video preview
- Progress bar during rendering
- Ken Burns zoom effect
- Crossfade transitions
- Batch rendering

---

# License

MIT License

---

# Author

Developed for automated slideshow video generation using FFmpeg.
