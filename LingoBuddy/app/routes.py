from flask import current_app as app, render_template, request, jsonify
import requests
import os
import json
from googletrans import Translator
from werkzeug.utils import secure_filename
import PyPDF2
import chromadb

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

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

        # Extract text from PDF
        text_content = extract_text_from_pdf(filepath)

        # Create embeddings of the extracted text and store in Chroma
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

        embeddings = response_data['data']  # Extract the list of embedding objects

        # Prepare documents for ChromaDB
        documents = [
            {
                "id": str(embedding['index']),
                "embedding": embedding['embedding'],
                "metadata": {"filename": filename}
            }
            for embedding in embeddings
        ]

        
        # Add documents to ChromaDB collection
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
        # Fetch all documents from the collection
        embeddings = chroma_collection.get()
        return jsonify({'embeddings': embeddings}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")

    # Translate user input from Tamil to English
    translator = Translator()
    translated_input = translator.translate(user_input, src='ta', dest='en').text

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
      "content": user_input
    }]
    }
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer YyPiJjsgNkGJRrg7JNjT6mBGAft8mQyAGoXG87YVk2Y6qo7A"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    data = response.json()

    # Print the response details
    print("Response Status Code:", response.status_code)
    print("Response Data:", json.dumps(data, indent=2))

    api_response = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process that.")

    # Translate API response from English to Tamil
    translated_response = translator.translate(api_response, src='en', dest='ta').text

    return jsonify({"response": translated_response})
