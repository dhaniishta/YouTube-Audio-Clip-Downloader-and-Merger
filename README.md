# YouTube Audio Clip Downloader and Merger

This Flask-based web application allows users to download YouTube videos of their favorite singers and extract the first *y* seconds of audio from each video. Users can specify the singer's name, the number of videos to download, and the length of the audio clip to extract. Once the audios are processed, the application merges all the audio clips into a single output file.

## Key Features
- **Download YouTube videos** based on the provided singer's name and number of videos.
- **Extract and trim** the first *y* seconds of audio from each video.
- **Merge** the trimmed audio files into a single output.
- **User-friendly interface** with three input fields: singer name, number of videos, and audio duration to extract.
- Audio processing without relying on ffmpeg.

## Technologies Used
- **Flask** (Backend framework)
- **yt-dlp** (YouTube video downloading)
- **MoviePy** (Audio extraction and merging)
- **HTML/CSS** for front-end design

## How to Run
1. Clone the repository.
   ```bash
   git clone https://github.com/yourusername/yourrepository.git

