import re
import random
import threading

def respond_to_greeting(user_input):
    greetings = ["Hello, my name is Chatbot trial.", 
                 "Hi there! I'm Chatbot trial.", 
                 "Greetings! I'm Chatbot trial."]
    if re.search(r"\bhello\b|\bhi\b", user_input.lower()):
        return random.choice(greetings)
    return None

def respond_to_farewell(user_input):
    if re.search(r"\bgoodbye\b", user_input.lower()):
        return "Goodbye! Have a great day!"
    return None

def respond_to_thank_you(user_input):
    if re.search(r"\bthank you\b|\bthanks\b", user_input.lower()):
        return "You're welcome!"
    return None

def respond_to_how_are_you(user_input):
    if re.search(r"\bhow are you\b", user_input.lower()):
        return "I'm a bot, so I don't have feelings, but thanks for asking!"
    return None

def respond_to_name_introduction(user_input):
    if re.search(r"\bmy name is\b", user_input.lower()):
        name = re.search(r"\bmy name is ([a-zA-Z ]+)", user_input, re.IGNORECASE)
        if name:
            return f"Nice to meet you, {name.group(1).strip()}!"
    return None

def set_reminder(user_input):
    # More lenient pattern to match various reminder formats
    pattern = re.compile(
        r"\bremind me to (.+?)(?: in (\d+)\s*(seconds?|minutes?|hours?)| at (\d{1,2}:\d{2}))?\b", re.IGNORECASE)
    match = pattern.search(user_input)
    
    if match:
        task = match.group(1).strip()
        time_amount = match.group(2)
        time_unit = match.group(3)
        time_at = match.group(4)
        
        if time_at:
            # Specific time given, calculate delay
            reminder_time = datetime.strptime(time_at, '%H:%M').time()
            now = datetime.now()
            reminder_datetime = datetime.combine(now, reminder_time)
            if reminder_datetime < now:
                reminder_datetime += timedelta(days=1)
            delay = (reminder_datetime - now).total_seconds()
        else:
            # Relative time given
            amount = int(time_amount)
            if time_unit.startswith("second"):
                delay = amount
            elif time_unit.startswith("minute"):
                delay = amount * 60
            elif time_unit.startswith("hour"):
                delay = amount * 3600
        
        threading.Timer(delay, lambda: print(f"Reminder: {task}")).start()
        return f"Reminder set for {task} in {time_amount} {time_unit}" if time_amount else f"Reminder set for {task} at {time_at}"
    return None

def main():
    while True:
        user_input = input("You: ")
        
        # Try to get a response from different response functions
        response = (
            respond_to_greeting(user_input) or
            respond_to_farewell(user_input) or
            respond_to_thank_you(user_input) or
            respond_to_how_are_you(user_input) or
            respond_to_name_introduction(user_input) or
            set_reminder(user_input)
        )
        
        if response:
            print("Bot:", response)
            if response.startswith("Goodbye"):
                break  # Exit the loop if the response is a farewell message
        else:
            print("Bot: Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()
