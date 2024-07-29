from flask import current_app as app, render_template, request, jsonify, send_file, url_for, send_from_directory, session, redirect
import requests
import os
import json
from deep_translator import GoogleTranslator
from werkzeug.utils import secure_filename
import PyPDF2
import chromadb
from audio_translation import (
    download_youtube_video, extract_audio_from_video, transcribe_audio,
    translate_text_to_tamil, generate_tamil_audio, overlay_audio_on_video,
    save_transcriptions_to_txt, clear_folders
)
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
local_embeddings = []
VIDEO_DIR = '../../translated_video'
TRANSCRIPTION_TXT_DIR = '../../transcription'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("pdf_embeddings")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Quiz
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Madrid'],
        'answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {
        'question': 'Who wrote "To Kill a Mockingbird"?',
        'options': ['Harper Lee', 'Mark Twain', 'Ernest Hemingway', 'F. Scott Fitzgerald'],
        'answer': 'Harper Lee'
    }
]

recommendations = {
    'Python': {
        'Beginner': ['Introduction to Python', 'Python for Beginners'],
        'Intermediate': ['Intermediate Python', 'Python Data Structures'],
        'Advanced': ['Advanced Python Programming', 'Python Machine Learning']
    },
    'JavaScript': {
        'Beginner': ['JavaScript Basics', 'JavaScript for Beginners'],
        'Intermediate': ['Intermediate JavaScript', 'JavaScript and DOM'],
        'Advanced': ['Advanced JavaScript', 'JavaScript Frameworks']
    },
    'Data Structures': {
        'Beginner': ['Introduction to Data Structures', 'Basic Data Structures'],
        'Intermediate': ['Intermediate Data Structures', 'Data Structures in Practice'],
        'Advanced': ['Advanced Data Structures', 'Data Structures and Algorithms']
    }
}

@app.route("/")
def index():
    return render_template("index.html", subjects=recommendations.keys())

@app.route("/translation")
def translation():
    return render_template("translation.html")

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text_content = extract_text_from_pdf(filepath)

        create_and_store_embeddings(text_content, filename)

        return jsonify({'message': 'File uploaded successfully!', 'content': text_content}), 200

def extract_text_from_pdf(filepath):
    reader = PyPDF2.PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_and_store_embeddings(text_content, filename):
    url = "https://api.fireworks.ai/inference/v1/embeddings"
    payload = {
        "input": text_content,
        "model": "nomic-ai/nomic-embed-text-v1.5",
        "dimensions": 1536
    }
    headers = {
        "Authorization": "Bearer YyPiJjsgNkGJRrg7JNjT6mBGAft8mQyAGoXG87YVk2Y6qo7A",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        embeddings = response_data['data']  

        documents = [
            {
                "id": str(embedding['index']),
                "embedding": embedding['embedding'],
                "metadata": {"filename": filename}
            }
            for embedding in embeddings
        ]

        local_embeddings.extend(documents)
        
        chroma_collection.add(
            embeddings=[doc["embedding"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents],
            ids=[doc["id"] for doc in documents]
        )
        
        for doc in documents:
            print(doc['embedding'])
            print(doc['metadata'])
            print(doc['id'])
        print("Embeddings successfully added to ChromaDB.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching embeddings: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/get_embeddings', methods=['GET'])
def get_embeddings():
    try:
        embeddings = chroma_collection.get()
        return jsonify({'embeddings': embeddings}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    translated_input = GoogleTranslator(source='ta', target='en').translate(user_input)

    relevant_docs = []  
    
    for doc in local_embeddings:
        if translated_input in doc['metadata']['filename']:  
            relevant_docs.append(doc)

    if relevant_docs:
        context = " ".join([doc['embedding'] for doc in relevant_docs])
    else:
        context = ""

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
    "model": "accounts/fireworks/models/mixtral-8x22b-instruct",
    "max_tokens": 8192,
    "top_p": 1,
    "top_k": 40,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "temperature": 0.6,
    "messages": [{
            "role": "user",
            "content": translated_input
        }, {
            "role": "system",
            "content": context  
        }]
    }
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer YyPiJjsgNkGJRrg7JNjT6mBGAft8mQyAGoXG87YVk2Y6qo7A"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    data = response.json()

    print("Response Status Code:", response.status_code)
    print("Response Data:", json.dumps(data, indent=2))

    api_response = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process that.")

    translated_response = GoogleTranslator(source='en', target='ta').translate(api_response)
    return jsonify({"response": translated_response})

@app.route('/video_translation', methods=['POST'])
def video_translation():
    youtube_url = request.form['youtube_url']
    
    # Define paths
    video_path = 'app/static/videos/source_video/video.mp4'
    audio_path = 'app/static/audio/audio.wav'
    tamil_audio_path = 'app/static/translated_audio/tamil_audio.mp3'
    final_video_path = 'app/static/videos/translated_video/translated_video.mp4'
    transcription_txt_path = 'app/static/transcription/transcription.txt'
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(tamil_audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
    os.makedirs(os.path.dirname(transcription_txt_path), exist_ok=True)
    
    # Processing
    download_youtube_video(youtube_url, video_path)
    extract_audio_from_video(video_path, audio_path)
    
    transcription = transcribe_audio(audio_path)
    translated_text = translate_text_to_tamil(transcription)
    generate_tamil_audio(translated_text, tamil_audio_path)
    
    save_transcriptions_to_txt(transcription, translated_text, transcription_txt_path)
    
    overlay_audio_on_video(video_path, tamil_audio_path, final_video_path)
    
    # Delay to ensure all processes are completed
    time.sleep(2)
    
    # Clear folders
    clear_folders([
        'app/static/videos/source_video',
        'app/static/audio',
        'app/static/translated_audio'
    ])
    
    return jsonify({
        'translated_text': translated_text
    }) 

@app.route('/quiz')
def home():
    return render_template('quiz/index.html', subjects=recommendations.keys())

@app.route('/quiz/start_quiz')
def start_quiz():
    session['question_index'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz/quiz', methods=['GET', 'POST'])
def quiz():
    question_index = session.get('question_index', 0)
    score = session.get('score', 0)

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == questions[question_index]['answer']:
            session['score'] = score + 1
        session['question_index'] = question_index + 1
        if question_index + 1 >= len(questions):
            return redirect(url_for('result'))
        else:
            return redirect(url_for('quiz'))

    if question_index >= len(questions):
        return redirect(url_for('result'))

    question = questions[question_index]
    return render_template('quiz/quiz.html', question=question, question_index=question_index)

@app.route('/quiz/result')
def result():
    score = session.get('score', 0)
    return render_template('quiz/result.html', score=score, total=len(questions))

@app.route('/get_analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'GET':
        subject = request.args['subject']
        skill_level = request.args['skill_level']
        recommended_content = recommendations.get(subject, {}).get(skill_level, [])
        return jsonify({"recommended_content": recommended_content, "selected_subject": subject, "selected_skill_level":skill_level})
    return jsonify({"response": recommendations.keys()})
