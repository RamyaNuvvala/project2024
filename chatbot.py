class CollegeChatBot:
    def __init__(self):
        self.courses = {
            "Computer Science": "Computer Science is the study of computers and computational systems.",
            "Engineering": "Engineering is the application of scientific principles to design and build machines, structures, and systems.",
            "Business Administration": "Business Administration focuses on managing and organizing business operations and strategies.",
            # Add more courses as needed
        }

    def start(self):
        print("Welcome to CollegeChatBot! How can I help you?")
        while True:
            user_input = input("You: ").strip().lower()
            if user_input == "exit":
                print("CollegeChatBot: Goodbye!")
                break
            elif "courses" in user_input:
                self.display_courses()
            elif "admission" in user_input:
                self.display_admission_info()
            else:
                print("CollegeChatBot: I'm sorry, I don't understand. Please ask about courses or admission.")

    def display_courses(self):
        print("CollegeChatBot: Here are the available courses:")
        for course, description in self.courses.items():
            print(f"{course}: {description}")

    def display_admission_info(self):
        print("CollegeChatBot: For admission information, please visit our college website or contact the admissions office.")

if __name__ == "__main__":
    chatbot = CollegeChatBot()
    chatbot.start()
