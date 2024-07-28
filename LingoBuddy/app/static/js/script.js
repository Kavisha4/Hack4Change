document.getElementById("send-btn").addEventListener("click", function () {
  const userInput = document.getElementById("user-input").value;
  if (userInput.trim()) {
    addMessage("user", userInput);
    fetch("/get_response", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput }),
    })
      .then((response) => response.json())
      .then((data) => addMessage("bot", data.response));
    document.getElementById("user-input").value = "";
  }
});

document.getElementById("upload-btn").addEventListener("click", function () {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload_pdf", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        const uploadStatus = document.getElementById("upload-status");
        if (data.error) {
          uploadStatus.textContent = `Error: ${data.error}`;
          uploadStatus.style.color = "red";
        } else {
          uploadStatus.textContent = "File uploaded successfully!";
          uploadStatus.style.color = "green";
          document.getElementsByClassName(
            "file-upload-button"
          )[0].disabled = true;
          document.getElementById("upload-btn").disabled = true;
          document.getElementById("file-input").disabled = true;
          console.log("Extracted text:", data.content);
        }
      })
      .catch((error) => {
        const uploadStatus = document.getElementById("upload-status");
        uploadStatus.textContent = `Error: ${error.message}`;
        uploadStatus.style.color = "red";
      });
  } else {
    const uploadStatus = document.getElementById("upload-status");
    uploadStatus.textContent = "Please select a file to upload.";
    uploadStatus.style.color = "red";
  }
});

function addMessage(sender, text) {
  const message = document.createElement("div");
  message.classList.add("message", sender);
  message.textContent = text;
  const lineBreak = document.createElement("br");
  var icon = document.createElement("img");
  if (sender === "bot") {
    icon.className = "bot-img";
    icon.src = "{{ url_for('static', filename='images/bot.png') }}";
  } else {
    icon.className = "user-img";
    icon.src = "{{ url_for('static', filename='images/user.png') }}";
  }
  document.getElementById("chat-box").appendChild(lineBreak);
  document.getElementById("chat-box").appendChild(icon);
  document.getElementById("chat-box").appendChild(message);
  message.scrollIntoView();
}

document.getElementById('translate-btn').addEventListener('click', function() {
    const youtubeUrl = document.getElementById('youtube-url').value;

    if (youtubeUrl.trim()) {
        fetch('/upload_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ youtube_url: youtubeUrl })
        })
        .then(response => response.json())
        .then(data => {
            const uploadStatus = document.getElementById('upload-status');
            if (data.error) {
                uploadStatus.textContent = `Error: ${data.error}`;
                uploadStatus.style.color = 'red';
            } else {
                uploadStatus.textContent = 'Audio translated successfully!';
                uploadStatus.style.color = 'green';
                console.log('Translated text:', data.response);
                addMessage('bot', data.response);
            }
        })
        .catch(error => {
            const uploadStatus = document.getElementById('upload-status');
            uploadStatus.textContent = `Error: ${error.message}`;
            uploadStatus.style.color = 'red';
        });
    } else {
        const uploadStatus = document.getElementById('upload-status');
        uploadStatus.textContent = 'Please enter a YouTube URL.';
        uploadStatus.style.color = 'red';
    }
});
