# Multilingual Education Enhancer

## Introduction

Today's online education doesn’t encompass learning modules in the various Indian languages. Our aim is to bridge the gap in Online Learning Platforms to students from various vernacular backgrounds in India and give them access to educational resources.

## Objectives

Our motive is to have:
1. Multilingual learning with translational capabilities, with engaging learning content
2. Skills assessment and personalised recommendations
3. Summarised version of a textbook or PDF
4. New transcript/Closed captions in vernacular language

## Target Consumers

Students from different vernacular backgrounds.

## How We Plan to Achieve This

1. Process the existing English lectures, audios and videos
2. Generate subtitles for the video using AI and create a corpus of transcripts along with timestamps
3. Use NLP to identify and categorise the transcript into important topics
4. Save timestamps corresponding to the topics identified
5. Perform a translation of the corpus into the preferred language
6. Integrate the translated vernacular into a single transcript
7. Create a new audio in the specified vernacular language
8. Sync the new transcript along with new dubbed audio

## Progress So Far

- Created a chatbot using Python
- Developed a simple front end with JavaScript
- Created a Google Chrome extension for the same
- Built a quizzing platform which can be in any language you require

## How to Use

### Prerequisites

- Python 3.x
- Node.js
- Chrome browser

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/multilingual-education-enhancer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd multilingual-education-enhancer
    ```
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Install JavaScript dependencies:
    ```bash
    npm install
    ```

### Running the Project

1. Start the backend server:
    ```bash
    python server.py
    ```
2. Open the frontend:
    ```bash
    open index.html
    ```
3. Load the Chrome extension:
    - Open Chrome and go to `chrome://extensions/`
    - Enable Developer mode
    - Click "Load unpacked" and select the `chrome-extension` directory

