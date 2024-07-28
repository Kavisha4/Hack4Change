from flask import current_app as app, render_template, request, jsonify
import requests
import os
import json
from deep_translator import GoogleTranslator
from werkzeug.utils import secure_filename
import PyPDF2
import yt_dlp
import io
import chromadb

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
local_embeddings = []

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("pdf_embeddings")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")

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

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    if not youtube_url:
        return jsonify({'error': 'No YouTube URL provided'}), 400

    try:
        audio_data = get_youtube_audio_stream(youtube_url)

        files = {
            'file': ('audio.mp3', audio_data, 'audio/mpeg')
        }
        payload = {
            'model': 'whisper-v3',
            'prompt': 'null',
            'response_format': 'json',
            'temperature': 0.5
        }
        headers = {
            "Authorization": "Bearer YyPiJjsgNkGJRrg7JNjT6mBGAft8mQyAGoXG87YVk2Y6qo7A"
        }
        url = "https://api.fireworks.ai/inference/v1/audio/translations"
        response = requests.post(url, files=files, data=payload, headers=headers)
        response_data = response.json()

        print("Response Status Code:", response.status_code)
        print("Response Data:", json.dumps(response_data, indent=2))

        return jsonify({"response": response_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
