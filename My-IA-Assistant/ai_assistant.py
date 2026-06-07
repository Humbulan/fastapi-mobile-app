import random
from datetime import datetime

class AIAssistant:
    def __init__(self):
        self.mode = "assistant"
        self.conversation = []
        
        print("🚀 MY IA ASSISTANT ACTIVATED!")
        print("💡 Type 'help' for commands")
        print("💡 Type 'quit' to exit\n")
        
        self.response("My IA Assistant ready! How can I help you?")
    
    def response(self, text):
        print(f"🤖 {text}")
        self.conversation.append(f"AI: {text}")
    
    def help(self):
        help_text = """
🎯 MY IA ASSISTANT - COMMANDS:

**AI MODES:**
assistant, creative, expert, friendly, coder

**BASIC FEATURES:**
time, date, joke, fact, advice
quote, story, code, status, history

**ADVANCED FEATURES:**
project tech - Technology project plan
project business - Business project plan  
project creative - Creative project plan
project learning - Learning project plan
calc 15+8 - Math calculations

**EXAMPLES:**
creative -> story -> project creative
coder -> code -> calc 15+8
expert -> project tech -> advice
"""
        print(help_text)
    
    def get_time(self):
        now = datetime.now()
        return f"🕒 Time: {now.strftime('%I:%M %p')}"
    
    def get_date(self):
        now = datetime.now()
        return f"📅 Date: {now.strftime('%A, %B %d, %Y')}"
    
    def get_joke(self):
        jokes = [
            "Why don't scientists trust atoms? They make up everything!",
            "Why did the scarecrow win an award? Outstanding in his field!",
            "What do you call a fake noodle? An impasta!"
        ]
        return f"😂 {random.choice(jokes)}"
    
    def get_fact(self):
        facts = [
            "Honey never spoils! 3000-year-old honey still edible.",
            "Octopuses have three hearts and blue blood!",
            "The Eiffel Tower grows 15cm taller in summer!"
        ]
        return f"🔍 {random.choice(facts)}"
    
    def get_advice(self):
        advice = [
            "Break big tasks into small steps!",
            "Take breaks to stay focused.",
            "Learn something new every day!"
        ]
        return f"💡 {random.choice(advice)}"
    
    def get_quote(self):
        quotes = [
            "Do great work by loving what you do. - Steve Jobs",
            "Believe in the beauty of your dreams. - Eleanor Roosevelt",
            "Courage to continue counts. - Winston Churchill"
        ]
        return f"💫 {random.choice(quotes)}"
    
    def get_story(self):
        stories = [
            "Once a programmer found magical code! 🌟",
            "In a digital kingdom, AI helped people! 🏰",
            "A wise computer knew answers to questions! 💫"
        ]
        return f"📖 {random.choice(stories)}"
    
    def get_project(self, project_type):
        projects = {
            "tech": "🚀 TECH PROJECT:\n1. Plan requirements\n2. Choose technology\n3. Build prototype\n4. Test thoroughly\n5. Launch and improve",
            "business": "💼 BUSINESS PROJECT:\n1. Market research\n2. Business model\n3. Build MVP\n4. Customer testing\n5. Launch strategy",
            "creative": "🎨 CREATIVE PROJECT:\n1. Find inspiration\n2. Brainstorm ideas\n3. Create prototype\n4. Get feedback\n5. Finalize work",
            "learning": "📚 LEARNING PROJECT:\n1. Set goals\n2. Find resources\n3. Create schedule\n4. Practice daily\n5. Apply knowledge"
        }
        return projects.get(project_type, "Use: project tech, business, creative, or learning")
    
    def get_code(self):
        return """💻 PYTHON CODE EXAMPLE:

# Simple Calculator
def calculator():
    num1 = float(input('Enter first number: '))
    num2 = float(input('Enter second number: '))
    operation = input('Enter operation (+, -, *, /): ')
    
    if operation == '+': result = num1 + num2
    elif operation == '-': result = num1 - num2
    elif operation == '*': result = num1 * num2
    elif operation == '/': result = num1 / num2
    else: result = 'Invalid operation'
    
    print(f'Result: {result}')

calculator()"""
    
    def calculate(self, text):
        try:
            if "+" in text:
                parts = text.split("+")
                a = float(''.join(c for c in parts[0] if c.isdigit()))
                b = float(''.join(c for c in parts[1] if c.isdigit()))
                return f"📊 {a} + {b} = {a+b}"
            elif "-" in text:
                parts = text.split("-")
                a = float(''.join(c for c in parts[0] if c.isdigit()))
                b = float(''.join(c for c in parts[1] if c.isdigit()))
                return f"📊 {a} - {b} = {a-b}"
            return "Try: calc 15+8 or calc 20-5"
        except:
            return "Use numbers like: calc 15+8"
    
    def show_history(self):
        print("\n📜 CONVERSATION HISTORY:")
        if not self.conversation:
            print("No conversation yet.")
        else:
            for msg in self.conversation[-5:]:
                print(msg)
        print()
    
    def show_status(self):
        print(f"\n📊 SYSTEM STATUS:")
        print(f"Mode: {self.mode}")
        print(f"Messages: {len(self.conversation)}")
        print("Status: ✅ Operational\n")
    
    def run(self):
        while True:
            try:
                user_input = input("You: ").strip().lower()
                self.conversation.append(f"You: {user_input}")
                
                if user_input == "quit":
                    self.response("Goodbye! 👋")
                    break
                elif user_input == "help":
                    self.help()
                elif user_input == "history":
                    self.show_history()
                elif user_input == "status":
                    self.show_status()
                elif user_input in ["assistant", "creative", "expert", "friendly", "coder"]:
                    self.mode = user_input
                    self.response(f"Switched to {self.mode} mode! 🎯")
                elif user_input == "time":
                    self.response(self.get_time())
                elif user_input == "date":
                    self.response(self.get_date())
                elif user_input == "joke":
                    self.response(self.get_joke())
                elif user_input == "fact":
                    self.response(self.get_fact())
                elif user_input == "advice":
                    self.response(self.get_advice())
                elif user_input == "quote":
                    self.response(self.get_quote())
                elif user_input == "story":
                    self.response(self.get_story())
                elif user_input.startswith("project "):
                    project_type = user_input[8:]
                    self.response(self.get_project(project_type))
                elif user_input == "code":
                    self.response(self.get_code())
                elif user_input.startswith("calc"):
                    math_text = user_input[4:].strip()
                    self.response(self.calculate(math_text))
                elif user_input == "":
                    continue
                else:
                    self.response("Type 'help' for commands!")
                
            except KeyboardInterrupt:
                self.response("Session ended. Goodbye! 👋")
                break
            except Exception as e:
                self.response("Error occurred. Please try again.")

if __name__ == "__main__":
    ai = AIAssistant()
    ai.run()
