# ![logo](/app/static/images/favicon-32x32.png)skill.io

## Important Links

<div>
    🚀<a href="https://samyuktha1262.pythonanywhere.com/" style="display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-decoration: none; color: #007bff; background-color: #f8f9fa; font-size: 16px; text-align: center;">
        Deployment
    </a>
    <br/>
    📹<a href="https://youtu.be/oQCjwEJQZIM" style="display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-decoration: none; color: #007bff; background-color: #f8f9fa; font-size: 16px; text-align: center;">
         Demo Video
    </a>
    <br/>
    📄<a href="technical_documentation.pdf" style="display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-decoration: none; color: #007bff; background-color: #f8f9fa; font-size: 16px; text-align: center;">
         Technical Documentation
    </a>
    <br/>
    📘<a href="https://solution-document-link.com" style="display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-decoration: none; color: #007bff; background-color: #f8f9fa; font-size: 16px; text-align: center;">
         Solution PDF
    </a>
    <br/>
    📊<a href="https://colab.research.google.com/drive/1gLYyMbe0OXLiVNX7ttxFgzq5a6ixiZoX#scrollTo=dDEIkxucr8No" style="display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-decoration: none; color: #007bff; background-color: #f8f9fa; font-size: 16px; text-align: center;">
         Benchmarking Tests
    </a>
</div>



## Introduction

Today's online education doesn’t encompass learning modules in the various Indian languages. Our aim is to bridge the gap in Online Learning Platforms to students from various vernacular backgrounds in India and give them access to educational resources.

## Objectives

Our motive is to have:
1. Multilingual learning with translational capabilities, with engaging learning content
2. Skills assessment and personalised recommendations
3. RAG based Question Answering on English books using vernacular languages
4. New transcript/Closed captions in vernacular language

## Target Consumers

Students from different vernacular backgrounds.

## How We Plan to Achieve This

1. Process the existing English lectures, audios and videos
2. Generate subtitles for the video using AI and create a corpus of transcripts along with timestamps
3. Save timestamps corresponding to the topics identified
4. Perform a translation of the corpus into the preferred language
5. Integrate the translated vernacular into a single transcript
6. Create a new audio in the specified vernacular language
7. Sync the new transcript along with new dubbed audio

## Progress So Far

- Created a chatbot using Python
- Developed a simple front end using Flask and Jinja2 templates with HTML, CSS, and JavaScript.
- Created a Google Chrome extension for the same
- Built a quizzing platform which can be in any language you require

## LLM-RAG Based Multi-lingual Chatbot

1. RAG Search (Retrieval-Augmented Generation):
   - RAG combines retrieval and generation to produce more accurate and contextually relevant responses.
   - The model first retrieves relevant documents or text chunks from a knowledge base and then generates an answer based on the retrieved content.
     
2. Chroma DB:
   - Chroma DB is a vector database used to store and query embeddings (vector representations) of documents.
   - It helps in efficient similarity searches by comparing user queries with stored document embeddings to find the most relevant matches.
     
3. Context-Based Answering:
   - The chatbot uses context from previously retrieved documents to generate responses.
   - By providing relevant context, it ensures that the answers are coherent and relevant to the user's query.
     
4. LLM Model (Large Language Model):
   - The chatbot uses a large language model Mixtral to understand and generate human-like text based on the input it receives.
   - This model helps in generating fluent and contextually appropriate responses to user queries.

5. Fireworks AI:
   - Fireworks AI provides API endpoints for various AI tasks, including embeddings and chat completions.
   - In this chatbot, Fireworks AI is used to generate embeddings for documents and to facilitate chat-based interactions with the user.
     
## Video Translator

1. YouTube Video Download:
   - The system uses a function to download videos from YouTube, saving them locally for further processing.
   - This allows users to input any YouTube link and have the video content processed.
     
2. Audio Extraction and Transcription:
   - After downloading the video, the audio is extracted.
   - The extracted audio is then transcribed into text, which forms the basis for translation.

3. Text Translation:
   - The transcribed text is translated into Tamil (or other specified languages) using a translation service.
   - This enables the content to be accessible in different languages.

4. Audio Generation and Overlay:
   - A new audio file is generated from the translated text.
   - This new audio is then overlaid onto the original video, creating a translated version of the video with synchronized audio.

## Quiz Platform

1. Quiz Setup and Session Management:
   - The quiz functionality sets up questions and manages the quiz state using session variables.
   - Each user session tracks the current question index and the user's score.

2. Question Handling:
   - Questions are served one at a time, with multiple-choice options provided.
   - The user's answer is checked against the correct answer, and their score is updated accordingly.

4. Question Navigation:
   - The system handles navigation between questions, ensuring the user can proceed through the quiz seamlessly.
   - After answering all questions, the quiz is marked as completed, and the final score is calculated.

5. Scoring and Results:
   - The user's score is calculated based on their correct answers.
   - The final results are displayed at the end of the quiz, showing the user's performance.

6. Subject and Skill Level Recommendations:
   - The quiz includes a feature for recommending content based on the subject and skill level selected by the user.
   - This personalized recommendation system helps users find relevant learning materials.

## How to Use

### Prerequisites

- Python 3.11
- Chrome browser

### Running the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/multilingual-education-enhancer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd LingoBuddy
    ```
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python run.py
    ```

### Running the Chrome Extension

1. Load the Chrome extension:
    - Open Chrome and go to `chrome://extensions/`
    - Enable Developer mode
    - Click "Load unpacked" and select the `Chrome Extension` directory

