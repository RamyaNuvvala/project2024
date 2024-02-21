from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Load faculty profiles from CSV file
faculty_profiles = {}

def load_faculty_profiles():
    with open('faculty_profiles.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip().lower()
            faculty_profiles[name] = row

# Generate a response based on user input
def generate_response(user_input):
    user_input_lower = user_input.lower()

    # Check for welcome messages
    welcome_messages = ['hi', 'hello', 'hey']
    for greeting in welcome_messages:
        if greeting in user_input_lower:
            return "Hi there! How can I assist you?"

    # Check if any part of the input matches with defined patterns
    patterns = {
        'website': {'link': 'https://rvrjcce.ac.in/', 'description': 'college website'},
        'moodle': {'link': 'http://courses.rvrjc.ac.in/moodle/', 'description': 'Moodle platform'},
        'departments': {'link': '/departments', 'description': 'departments'},
        'placements': {'link': 'https://rvrjcce.ac.in/placement_statistics.php?menu=plcmnt', 'description': 'placement information'},
        'academic calendar': {'link': 'https://rvrjcce.ac.in/academic.php', 'description': 'Academic Calendar'},
        'location': {'response': 'The RVR and JC College of Engineering is located at Chowdavaram, Guntur, Andhra Pradesh, India'},
        'courses': {'response': 'The College offers Graduate and Undergraduate education courses in Engineering and Technology'},
        'contact': {'response': 'You can contact us at contact@collegewebsite.com or call us at +1-123-456-7890.'},
        'cse': {'link': '/departments/cse', 'description': 'Computer Science and Engineering Department'},
        'ece': {'link': '/departments/ece', 'description': 'Electronics and Communication Engineering Department'},
        'eee': {'link': '/departments/eee', 'description': 'Electrical and Electronics Engineering Department'},
        'it': {'link': '/departments/it', 'description': 'Information Technology Department'},
        'mech': {'link': '/departments/mech', 'description': 'Mechanical Engineering Department'},
        'civil': {'link': '/departments/civil', 'description': 'Civil Engineering Department'},
        'chemical': {'link': '/departments/chemical', 'description': 'Chemical Engineering Department'},
        'iot': {'link': '/departments/iot', 'description': 'Internet of Things Department'},
        'data science': {'link': '/departments/data_science', 'description': 'Data Science Department'},
        'aiml': {'link': '/departments/aiml', 'description': 'Artificial Intelligence and Machine Learning Department'}
    }
    for pattern, data in patterns.items():
        if pattern in user_input_lower or any(word in user_input_lower for word in data.get('description', '').split()):
            if 'link' in data:
                return f"Sure! You can visit {data['description']} here: <a href='{data['link']}'>{data['description'].capitalize()}</a>"
            elif 'response' in data:
                return data['response']

    # Check if any part of the input matches with faculty names
    matched_faculties = []
    for name, profile in faculty_profiles.items():
        parts = name.split()
        if any(part.lower() in user_input_lower.split() for part in parts):
            matched_faculties.append(profile)

    if matched_faculties:
        responses = []
        for faculty in matched_faculties:
            response = f"{faculty['Name']} works in the {faculty['Department']} department as a {faculty['Designation']}."
            responses.append(response)
        return ' '.join(responses)
    else:
        return "I'm sorry, I couldn't understand that. How can I assist you?"

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    load_faculty_profiles()
    app.run(debug=True)
