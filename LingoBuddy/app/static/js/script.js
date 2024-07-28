document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim()) {
        addMessage('user', userInput);
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => addMessage('bot', data.response));
        document.getElementById('user-input').value = '';
    }
});

document.getElementById('end-btn').addEventListener('click', function() {
    addMessage('bot', 'Thank you for using LingoBuddy! Have a great day!');
    document.getElementById('user-input').disabled = true;
    document.getElementById('send-btn').disabled = true;
});

function addMessage(sender, text) {
    const message = document.createElement('div');
    message.classList.add('message', sender);
    message.textContent = text;
    document.getElementById('chat-box').appendChild(message);
    message.scrollIntoView();
}
