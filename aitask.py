#Chatbot
import re
import random
from datetime import datetime


# --------------------------------------------------
# RESPONSES (patterns → replies)
# --------------------------------------------------

responses = {

    # greetings
    "greet": {
        "patterns": [
            r"\b(hi|hello|hey|howdy|sup|yo|hiya)\b",
        ],
        "replies": [
            "Hey there! How can I help you today?",
            "Hello! What's up?",
            "Hi! Good to see you. What do you need?",
        ],
    },

    # how are you
    "how_are_you": {
        "patterns": [
            r"how (are you|r u|do you do)",
            r"(how's it going|what's up|how have you been)",
        ],
        "replies": [
            "Doing great, thanks for asking! What about you?",
            "All good on my end! How can I help?",
            "I'm just a bot, but I'm feeling pretty good!",
        ],
    },

    # name
    "name": {
        "patterns": [
            r"what('s| is) your name",
            r"who are you",
            r"(tell me your name|your name)",
        ],
        "replies": [
            "I'm ChatBot — a simple rule-based assistant!",
            "People call me ChatBot. Nice to meet you!",
        ],
    },

    # jokes
    "joke": {
        "patterns": [
            r"\b(joke|funny|make me laugh|tell me a joke|humor)\b",
        ],
        "replies": [
           "Why don't scientists trust atoms?Because they makeup everything",
           "Why do programmers prefer dark mode? Light attracts bugs!",
           "Why was the math book sad? It had too many problems.",
        ],
    },

    # time
    "time": {
        "patterns": [
            r"\b(time|what time|current time|clock)\b",
        ],
        "replies": [
            lambda: f"Current time: {datetime.now().strftime('%I:%M %p')}",
        ],
    },

    # date
    "date": {
        "patterns": [
            r"\b(date|today|what day|current date|day is it)\b",
        ],
        "replies": [
            lambda: (
                "Today is "
                f"{datetime.now().strftime('%A, %B %d %Y')}"
            ),
        ],
    },

    # thanks
    "thanks": {
        "patterns": [
            r"\b(thanks|thank you|thx|ty|cheers)\b",
        ],
        "replies": [
            "You're welcome!",
            "Happy to help!",
            "No problem at all!",
        ],
    },

    # math
    "math": {
        "patterns": [
            r"\d+\s*[\+\-\*\/]\s*\d+",
        ],
        "replies": [
            "math_eval",
        ],
    },

    # bye
    "bye": {
        "patterns": [
            r"\b(bye|goodbye|exit|quit|farewell|ciao)\b",
        ],
        "replies": [
            "Goodbye! Come back anytime.",
            "See you later!",
            "Take care! Bye!",
        ],
    },
}


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def evaluate_math(user_input):
    """Safely evaluate a simple math expression."""
    match = re.search(r"\d+\s*[\+\-\*\/]\s*\d+", user_input)
    if not match:
        return "Please enter a valid math expression."

    expr = match.group()

    try:
        result = eval(expr, {"__builtins__": None}, {})
        return f"{expr} = {result}"
    except Exception:
        return "I couldn't calculate that expression."


def get_response(user_input):
    """Return chatbot reply."""
    text = user_input.lower().strip()

    for data in responses.values():
        for pattern in data["patterns"]:
            if re.search(pattern, text, re.IGNORECASE):
                reply = random.choice(data["replies"])

                if callable(reply):
                    return reply()

                if reply == "math_eval":
                    return evaluate_math(text)

                return reply

    return random.choice([
        "I didn't understand that.",
        "Can you rephrase?",
        "Ask me about time, date, or jokes!",
    ])


# --------------------------------------------------
# MAIN CHAT LOOP
# --------------------------------------------------

def main():
    print("=" * 50)
    print("        Welcome to ChatBot")
    print("Type 'bye' or 'quit' to exit")
    print("=" * 50)

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nChatBot: Goodbye!")
            break

        if not user_input:
            print("ChatBot: Say something!")
            continue

        response = get_response(user_input)
        print(f"ChatBot: {response}")

        if re.search(r"\b(bye|quit|exit)\b", user_input, re.IGNORECASE):
            break


if __name__ == "__main__":
    main()
