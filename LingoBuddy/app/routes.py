from flask import current_app as app, render_template, request, jsonify
import requests
import os
import json
from googletrans import Translator

@app.route("/")
def index():
    return render_template("index.html")

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
    "Authorization": "Bearer <API KEY>"
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
