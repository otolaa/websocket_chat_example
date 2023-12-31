const getRandomInt = (max) => {
    return Math.floor(Math.random() * max);
}

document.addEventListener('DOMContentLoaded', function() {
    
    const messagesContainer = document.querySelector('#messages_container');
    const messageForm = document.querySelector('[name=form_message]');
    const messageInput = document.querySelector('[name=message_input]');
    const sendMessageButton = document.querySelector('[name=send_message_button]');

    let us_ = `user_js_${getRandomInt(100)}`;
    let websocketClient = new WebSocket(`ws://127.0.0.1:3193/${us_}`);

    websocketClient.onopen = () => {
        console.log('[+] cliend commected!');
        
        messageForm.onsubmit = (e) => {
            e.preventDefault();

            websocketClient.send(messageInput.value);
            messageInput.value = "";

            return false;
        }
        
    }

    websocketClient.onmessage = (message) => {
        console.log(message);
        const newMessage = document.createElement('div');
        newMessage.innerHTML = message.data;
        messagesContainer.appendChild(newMessage);
    }

}, false);