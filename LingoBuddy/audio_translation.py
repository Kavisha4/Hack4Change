import yt_dlp
from deep_translator import GoogleTranslator
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import speech_recognition as sr
import os
import shutil
import time
import textwrap

def download_youtube_video(youtube_url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()  

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    transcription = recognizer.recognize_google(audio)
    return transcription

def translate_text_to_tamil(text):
    translator = GoogleTranslator(source='auto', target='ta')
    translated_text = translator.translate(text)
    return translated_text

def generate_tamil_audio(text, output_path):
    tts = gTTS(text=text, lang='ta')
    tts.save(output_path)

def overlay_audio_on_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    
    video.close()
    audio.close()

def save_transcriptions_to_txt(original_transcription, translated_transcription, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Original Transcription:\n")
        wrapped_text = textwrap.fill(original_transcription, width=80)
        f.write(wrapped_text + "\n\n")
        f.write("Translated Transcription (Tamil):\n")
        wrapped_translated_text = textwrap.fill(translated_transcription, width=80)
        f.write(wrapped_translated_text + "\n")

def clear_folders(folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def main(youtube_url):
    
    video_path = 'source_video/video.mp4'
    audio_path = 'audio/audio.wav'
    tamil_audio_path = 'translated_audio/tamil_audio.mp3'
    final_video_path = 'translated_video/translated_video.mp4'
    transcription_txt_path = 'transcription/transcription.txt'

    
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(tamil_audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
    os.makedirs(os.path.dirname(transcription_txt_path), exist_ok=True)

    
    download_youtube_video(youtube_url, video_path)
    extract_audio_from_video(video_path, audio_path)

    
    transcription = transcribe_audio(audio_path)
    print(f"Transcription: {transcription}")

    translated_text = translate_text_to_tamil(transcription)
    print(f"Translated Text: {translated_text}")
    save_transcriptions_to_txt(transcription, translated_text, transcription_txt_path)

    generate_tamil_audio(translated_text, tamil_audio_path)

    
    overlay_audio_on_video(video_path, tamil_audio_path, final_video_path)
    print(f"Translation and overlay complete. Output saved as '{final_video_path}'.")

    
    time.sleep(2) 

    
    clear_folders([
        'source_video',
        'audio',
        'translated_audio'
    ])

youtube_url = "https://www.youtube.com/watch?v=Sn-jsiJOKA8&t=4s"  
main(youtube_url)
