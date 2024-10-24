from flask import Flask, render_template, request
import os
import yt_dlp
from moviepy.editor import AudioFileClip, concatenate_audioclips

app = Flask(__name__)

# Function to download videos and convert them to audio without ffmpeg
def download_audio(singer, number_of_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(os.path.expanduser("~"), 'Desktop', '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    search_url = f"ytsearch{number_of_videos}:{singer}"

    # Download audio without postprocessing
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(search_url, download=True)
            audio_files = []
            if 'entries' in result:
                for entry in result['entries']:
                    audio_file = os.path.join(os.path.expanduser("~"), 'Desktop', f"{entry['title']}.webm")  # Keeping it as .webm initially
                    audio_files.append(audio_file)
            return audio_files
        except Exception as e:
            print(f"Error: {e}")
            return []

# Function to trim the first 'duration' seconds from an audio file
def trim_audio(audio_file, duration):
    try:
        audio_clip = AudioFileClip(audio_file)
        # Trim to only the first 'duration' seconds
        trimmed_clip = audio_clip.subclip(0, min(duration, audio_clip.duration))  # Ensure it doesn't exceed duration
        output_file = audio_file.replace(".webm", "_trimmed.m4a")  # Change extension to m4a
        trimmed_clip.write_audiofile(output_file, codec='aac')  # Save as m4a
        audio_clip.close()
        trimmed_clip.close()
        return output_file
    except Exception as e:
        print(f"Error trimming audio: {e}")
        return None

# Function to merge all audio files into one
def merge_audio_files(audio_files):
    try:
        audio_clips = [AudioFileClip(file) for file in audio_files]
        combined_audio = concatenate_audioclips(audio_clips)
        output_file = os.path.join(os.path.expanduser("~"), 'Desktop', 'combined_audio.m4a')
        combined_audio.write_audiofile(output_file, codec='aac')  # Specify audio codec for merging
        for clip in audio_clips:
            clip.close()
        return output_file
    except Exception as e:
        print(f"Error merging audio files: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    singer = request.form.get('singer')
    number_of_videos = request.form.get('number_of_videos')
    duration = request.form.get('duration')

    if not singer or not number_of_videos or not duration:
        return "Please provide all inputs: singer, number of videos, and duration.", 400

    try:
        number_of_videos = int(number_of_videos)
        duration = int(duration)
    except ValueError:
        return "Please provide valid numbers for the number of videos and duration.", 400

    # Download and process audio files
    audio_files = download_audio(singer, number_of_videos)

    if not audio_files:
        return "No audio files downloaded. Please check the singer's name or the number of videos.", 400

    trimmed_files = [trim_audio(file, duration) for file in audio_files]

    # Filter out any None results (in case of trimming errors)
    trimmed_files = [file for file in trimmed_files if file is not None]

    if not trimmed_files:
        return "No audio files were trimmed successfully.", 400

    result_file = merge_audio_files(trimmed_files)

    if result_file:
        return f"Audio files merged and saved as: {result_file}"
    else:
        return "Failed to merge audio files. Please try again.", 500

if __name__ == "__main__":
    app.run(debug=True)


