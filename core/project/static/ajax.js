const messagesDisplay = document.getElementById('messagesDisplay');
const fileButton = document.getElementById('fileButton');
const fileInput = document.getElementById('fileInput');
const submitButton = document.getElementById("submitButton");
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

if (messagesDisplay) {
    messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
}

fileButton.addEventListener('click', function (e) {
    e.preventDefault;
    fileInput.click();
});

messageInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        submitButton.click();
    }
});

chatForm.addEventListener('submit', function (e) {
    // prevents page reload when submitting
    e.preventDefault();

    // prevents the user from sending another message if it didn't yet
    // received a proper response from the api
    submitButton.disabled = true;

    const formData = new FormData(this);

    // message render
    if (formData.get('message')?.trim()) {
        if (fileInput.files.length > 0) {
            formData.append("file", fileInput.files[0]);
        }

        const newMessages = document.createElement('div');

        newMessages.classList.add('d-flex', 'justify-content-end', 'user-messages');
        newMessages.innerHTML = `<div class="message-bubble">${formData.get('message')}</div>`;

        messagesDisplay.appendChild(newMessages);

        // clears the input field
        messageInput.value = '';

        // waiting for response template message
        const responseMessage = document.createElement('div');
        responseMessage.classList.add("d-flex", "justify-content-start", "user-messages");
        responseMessage.style.alignItems = "flex-start";
        responseMessage.innerHTML = `<div class="message-bubble response">...</div>`;

        messagesDisplay.appendChild(responseMessage);

        messagesDisplay.scrollTop = messagesDisplay.scrollHeight;

        // AJAX Logic
        // logic for receiving a API response
        fetch('/send/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.sucess) {
                    responseMessage.innerHTML = `<div class="message-bubble response">${data.message_text}</div>`;
                }
                else throw new Error('ERROR WHILE GETTING THE RESPONSE');
            })
            .catch(e => console.error('ERROR:', e))
            .finally(() => {
                submitButton.disabled = false;
                messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
            });
    }
    else submitButton.disabled = false;
});
