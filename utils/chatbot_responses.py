import random

RESPONSES = {
    "Very Positive": [
        "Amazing — keep riding this wave of momentum! Remember to take micro-breaks.",
        "Great energy today! Use it to complete a tiny high-impact task."
    ],
    "Positive": [
        "Nice! Small consistent actions build big results.",
        "Keep going — your progress matters."
    ],
    "Neutral": [
        "You're doing okay. A short walk or a glass of water can help.",
        "Try focusing on one small task to get momentum."
    ],
    "Negative": [
        "It's okay to feel this way — try a 3-minute breathing exercise.",
        "Be kind to yourself. Take a short break and come back refreshed."
    ],
    "Very Negative": [
        "This sounds tough. If you're overwhelmed, try reaching out to someone you trust.",
        "Take small steps — even tiny progress counts. Consider a calming activity now."
    ]
}

def get_chat_response(mood_label):
    for key in RESPONSES:
        if key.lower() in mood_label.lower():
            return random.choice(RESPONSES[key])
    # fallback
    all_responses = sum(RESPONSES.values(), [])
    return random.choice(all_responses)
