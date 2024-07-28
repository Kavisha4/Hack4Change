import yt_dlp
import requests
import io
import os

def get_youtube_audio_stream(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': '-',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    audio_data = io.BytesIO()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(youtube_url, download=False)
        audio_stream_url = result['url']
        response = requests.get(audio_stream_url, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_data.write(chunk)
    audio_data.seek(0)
    return audio_data

def save_audio_to_file(audio_data, filename, folder='audio'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        f.write(audio_data.read())
    return filepath

# Example usage
youtube_url = "https://www.youtube.com/watch?v=Sn-jsiJOKA8&t=4s"  # Replace with your YouTube URL

audio_data = get_youtube_audio_stream(youtube_url)
audio_filename = "extracted_audio.mp3"  # You can customize the filename here
saved_filepath = save_audio_to_file(audio_data, audio_filename)

print(f"Audio saved to {saved_filepath}")


