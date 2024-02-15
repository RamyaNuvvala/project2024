$(document).ready(function() {
    // Function to append a message to the chat window
    function appendMessage(sender, message) {
        var messageElement = $('<div class="message">').text(sender + ": " + message);
        $('.chat-window').append(messageElement);
        // Scroll to the bottom of the chat window
        $('.chat-window').scrollTop($('.chat-window')[0].scrollHeight);
    }

    // Function to send user input to the server and receive chatbot response
    function sendMessage() {
        var userMessage = $('#user-input').val().trim();
        if (userMessage) {
            appendMessage("You", userMessage);
            $('#user-input').val(""); // Clear the input field
            $.post('/get_response', {user_input: userMessage}, function(data) {
                appendMessage("ChatBot", data.response);
            });
        }
    }

    // Event listener for the send button
    $('#send-button').click(sendMessage);

    // Event listener for the Enter key
    $('#user-input').keypress(function(event) {
        if (event.keyCode === 13) {
            sendMessage();
        }
    });
});
