import yt_dlp
from deep_translator import GoogleTranslator
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr
import os

def download_youtube_video(youtube_url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return 'video.mp4'

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = 'audio.wav'
    video.audio.write_audiofile(audio_path)
    return audio_path

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
    return output_path

def overlay_audio_on_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

def main(youtube_url):
    video_path = download_youtube_video(youtube_url)
    audio_path = extract_audio_from_video(video_path)

    transcription = transcribe_audio(audio_path)
    print(f"Transcription: {transcription}")

    translated_text = translate_text_to_tamil(transcription)
    print(f"Translated Text: {translated_text}")

    tamil_audio_path = 'tamil_audio.mp3'
    generate_tamil_audio(translated_text, tamil_audio_path)

    overlay_audio_on_video(video_path, tamil_audio_path, 'translated_video.mp4')
    print("Translation and overlay complete. Output saved as 'translated_video.mp4'.")

youtube_url = "https://www.youtube.com/watch?v=Sn-jsiJOKA8&t=4s"  
main(youtube_url)
