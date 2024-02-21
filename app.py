from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Load faculty profiles from CSV file
faculty_profiles = {}
student_details = {}

def load_faculty_profiles():
    with open('faculty_profiles.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip().lower()
            faculty_profiles[name] = row
def load_student_details():
    student_details.clear()  # Clear existing data
    with open('student_details.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert registration number to uppercase for consistency
            regno = row['Regno'].upper()
            Name = row['name'].upper()
            student_details[regno] = row
            student_details[Name] = row

             
           
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
    matched_students = []
    for regno, profile in student_details.items():
        if regno.lower() in user_input_lower or profile['name'].lower() in user_input_lower:
            matched_students.append(profile)

    if matched_students:
        responses = []
        for student in matched_students:
            response = f"<p><strong>Student Details:</strong></p>"
            for key, value in student.items():
                response += f"<p><strong>{key}:</strong> {value}</p>"
            responses.append(response)
        return responses
    matched_faculties = []
    for name, profile in faculty_profiles.items():
        parts = [part for part in name.split() if not part.endswith('.')]
        # If the name has only one part, consider it as a match if it's present in the user input
        if len(parts) == 1 and parts[0].lower() in user_input_lower.split():
            matched_faculties.append(profile)
        # If the name has multiple parts, match based on the threshold of at least 2 matched parts
        elif len(parts) > 1:
            matched_parts = sum(part.lower() in user_input_lower.split() for part in parts)
            if matched_parts >= 2:  # Adjust the threshold as needed
                matched_faculties.append(profile)

    if matched_faculties:
        responses = []
        for faculty in matched_faculties:
            response = f"<p><strong>Name:</strong> {faculty['Name']}</p>"
            response += f"<p><strong>Department:</strong> {faculty['Department']}</p>"
            response += f"<p><strong>Qualification:</strong> {faculty['Qualification']}</p>"
            response += f"<p><strong>Designation:</strong> {faculty['Designation']}</p>"
            responses.append(response)
        return responses
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
    load_student_details()
    app.run(debug=True)
