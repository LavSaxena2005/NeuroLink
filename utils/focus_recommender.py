def get_focus_tips(mood_label):
    """Return a short tip or recommendation based on mood label."""
    mood_label = mood_label.lower()
    if "very positive" in mood_label or "positive" in mood_label:
        return "You're doing great! Try a Pomodoro (25/5) session or focus music (instrumental)."
    if "very negative" in mood_label or "negative" in mood_label:
        return "Take a 5-minute breathing break, step outside for fresh air, or do a short walk."
    if "neutral" in mood_label:
        return "Keep a short to-do list and try a single 15-minute focused task."
    return "Try a breathing exercise or listen to calming music."
