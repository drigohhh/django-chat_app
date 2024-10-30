const messagesDisplay = document.getElementById('messagesDisplay');
const fileButton = document.getElementById('fileButton');
const fileInput = document.getElementById('fileInput');
const submitButton = document.getElementById("submitButton");
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

// Forces the scrollbar to the bottom of the display
if (messagesDisplay) {
    messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
}

fileButton.addEventListener('click', function (e) {
    e.preventDefault;
    fileInput.value = '';
    fileInput.click();
});

messageInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        submitButton.click();
    }
});

chatForm.addEventListener('submit', function (e) {
    // Prevents page reload when submitting
    e.preventDefault();

    if (e.target.getAttribute("name") === "file") return;

    // Prevents the user from sending another message if it didn't
    // receive a proper response from the api
    submitButton.disabled = true;

    const formData = new FormData(this);

    // Message render
    const responseMessage = document.createElement('div');

    if (formData.get('message')?.trim()) {
        // In case the user has sent a file
        if (fileInput.files.length > 0) {
            formData.append("file", fileInput.files[0]);
        }

        // For markdown parsing in the BackEnd
        fetch('/send/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.sucess) {
                    const newMessages = document.createElement('div');
                    newMessages.classList.add('d-flex', 'justify-content-end', 'user-messages');
                    newMessages.innerHTML = `<div class="message-bubble">${data.markdown_text}</div>`;

                    messagesDisplay.appendChild(newMessages);
                    // clears the input fields
                    messageInput.value = '';
                    fileInput.value = '';

                    // waiting for response template message
                    responseMessage.classList.add("d-flex", "justify-content-start", "user-messages");
                    responseMessage.style.alignItems = "flex-start";
                    responseMessage.innerHTML = `<div class="message-bubble response">...</div>`;

                    messagesDisplay.appendChild(responseMessage);

                    messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
                }
                else throw new Error("ERROR WHILE SENDING THE MESSAGE");
            })
            .catch(e => console.error("ERROR:", e));

        // Receiving an API response
        fetch('/receive/', {
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
