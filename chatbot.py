import csv
import random
import re
from datetime import datetime
from pathlib import Path


BOT_NAME = "SynBot"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "conversation_history.csv"


INTENTS = [
    {
        "name": "greeting",
        "patterns": [
            r"\bhi\b",
            r"\bhello\b",
            r"\bhey\b",
            r"\bgood morning\b",
            r"\bgood afternoon\b",
            r"\bgood evening\b",
        ],
        "responses": [
            "Hello! I am SynBot, your rule-based AI helper.",
            "Hi there! Ask me about AI, internships, or this chatbot project.",
            "Hey! How can I help you today?",
        ],
    },
    {
        "name": "help",
        "patterns": [
            r"\bhelp\b",
            r"\bwhat can you do\b",
            r"\bcommands\b",
            r"\boptions\b",
        ],
        "responses": [
            "I can answer small talk, explain AI basics, describe this project, and log our conversation.",
            "Try asking: what is AI, what is a rule-based chatbot, what is NLP, or how does this project work.",
        ],
    },
    {
        "name": "small_talk",
        "patterns": [
            r"\bhow are you\b",
            r"\bhow do you feel\b",
            r"\bare you fine\b",
        ],
        "responses": [
            "I am running smoothly, thanks for asking!",
            "I am doing great and ready to answer your questions.",
        ],
    },
    {
        "name": "thanks",
        "patterns": [
            r"\bthanks\b",
            r"\bthank you\b",
            r"\bthx\b",
        ],
        "responses": [
            "You are welcome!",
            "Happy to help.",
            "Anytime!",
        ],
    },
    {
        "name": "goodbye",
        "patterns": [
            r"\bbye\b",
            r"\bgoodbye\b",
            r"\bexit\b",
            r"\bquit\b",
        ],
        "responses": [
            "Goodbye! Your conversation has been saved.",
            "See you later! The chat history is logged.",
        ],
    },
]


KNOWLEDGE_BASE = {
    "ai": {
        "keywords": ["ai", "artificial intelligence"],
        "answer": "Artificial Intelligence is the field of building systems that can perform tasks that usually need human intelligence.",
    },
    "rule_based_chatbot": {
        "keywords": ["rule based chatbot", "rule-based chatbot", "pattern matching", "rules"],
        "answer": "A rule-based chatbot matches user input against predefined patterns and returns a prepared response.",
    },
    "nlp": {
        "keywords": ["nlp", "natural language processing"],
        "answer": "Natural Language Processing is a branch of AI that helps computers understand and work with human language.",
    },
    "machine_learning": {
        "keywords": ["machine learning", "ml"],
        "answer": "Machine Learning is an AI technique where systems learn patterns from data instead of being programmed with every rule manually.",
    },
    "internship": {
        "keywords": ["internship", "syntecxhub", "project"],
        "answer": "This internship project demonstrates a simple chatbot using intents, pattern matching, domain answers, console interaction, and chat logging.",
    },
    "conversation_log": {
        "keywords": ["log", "history", "conversation history"],
        "answer": "This chatbot stores each message in logs/conversation_history.csv with time, user input, bot response, and detected intent.",
    },
}


def normalize_text(text):
    """Return lowercase text with extra spaces removed."""
    return re.sub(r"\s+", " ", text.strip().lower())


def match_intent(user_text):
    """Find the first intent whose regex pattern matches the user message."""
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            if re.search(pattern, user_text):
                return intent["name"], random.choice(intent["responses"])
    return None, None


def search_knowledge_base(user_text):
    """Return a knowledge-base answer when the user asks about a known topic."""
    for topic in KNOWLEDGE_BASE.values():
        for keyword in topic["keywords"]:
            if keyword in user_text:
                return "knowledge_base", topic["answer"]
    return None, None


def get_response(user_message):
    """Choose a bot response using rules first, then the knowledge base."""
    cleaned_message = normalize_text(user_message)

    if not cleaned_message:
        return "empty", "Please type a message so I can help."

    intent, response = match_intent(cleaned_message)
    if response:
        return intent, response

    intent, response = search_knowledge_base(cleaned_message)
    if response:
        return intent, response

    return (
        "fallback",
        "I am not sure about that yet. Try asking about AI, NLP, machine learning, internships, or type help.",
    )


def log_message(user_message, bot_response, intent):
    """Append one conversation turn to a CSV log file."""
    LOG_DIR.mkdir(exist_ok=True)
    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "user_message", "bot_response", "intent"])
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_message,
                bot_response,
                intent,
            ]
        )


def run_chatbot():
    print(f"{BOT_NAME}: Hello! Type 'help' to see what I can do, or type 'exit' to quit.")

    while True:
        user_message = input("You: ")
        intent, bot_response = get_response(user_message)
        print(f"{BOT_NAME}: {bot_response}")
        log_message(user_message, bot_response, intent)

        if intent == "goodbye":
            break


if __name__ == "__main__":
    run_chatbot()
