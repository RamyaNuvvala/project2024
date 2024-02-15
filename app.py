from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_input']
    chatbot_response = generate_response(user_message)
    return jsonify({'response': chatbot_response})

def generate_response(user_message):
    # Add your chatbot logic here to generate a response based on user input
    if 'courses' in user_message.lower():
        return "Our college offers a variety of courses in fields such as computer science, engineering, business, etc."
    elif 'faculty' in user_message.lower():
        return "We have highly qualified faculty members who are experts in their respective fields."
    elif 'admission' in user_message.lower():
        return "For information about admission procedures, requirements, and deadlines, please visit our college website."
    elif 'facilities' in user_message.lower():
        return "Our campus provides state-of-the-art facilities including libraries, labs, sports facilities, and more."
    else:
        return "I'm sorry, I didn't understand that. How can I assist you?"

if __name__ == '__main__':
    app.run(debug=True)
