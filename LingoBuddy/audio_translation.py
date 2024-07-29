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

youtube_url = "https://www.youtube.com/watch?v=Sn-jsiJOKA8&t=4s"  