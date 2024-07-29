document.getElementById('translate').addEventListener('click', () => {
  const language = document.getElementById('language').value;
  const audioFile = document.getElementById('audio-file').files[0];
  const formData = new FormData();
  formData.append('audio', audioFile);
  formData.append('language', language);

  fetch('http://localhost:5000/translate', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('translated-text').innerText = data.translated_text;
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('send-chat').addEventListener('click', () => {
  const message = document.getElementById('chat-input').value;

  fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: message })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('chat-response').innerText = data.response;
  })
  .catch(error => console.error('Error:', error));
});