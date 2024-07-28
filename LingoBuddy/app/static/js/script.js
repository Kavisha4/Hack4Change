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

  var chatIconDiv = document.createElement("div");
  var img = document.createElement("img");
  var chatName = document.createElement("p");
  if (sender === "bot") {
    chatIconDiv.className = "chat-icon-div chat-icon-div-bot";
    img.className = "bot-img";
    img.src = "/static/images/bot.png";
    chatName.className = "chat-name chat-name-bot";
    chatName.textContent = "LingoBuddy";
  } else {
    chatIconDiv.className = "chat-icon-div chat-icon-div-user";
    img.className = "user-img";
    img.src = "/static/images/user.png";
    chatName.className = "chat-name chat-name-user";
    chatName.textContent = "User";
  }

  chatIconDiv.appendChild(img);
  chatIconDiv.appendChild(chatName);

  document.getElementById("chat-box").appendChild(lineBreak);
  document.getElementById("chat-box").appendChild(chatIconDiv);
  document.getElementById("chat-box").appendChild(message);
  message.scrollIntoView();
}
