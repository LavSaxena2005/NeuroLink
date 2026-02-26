import pathway as pw
from models.mood_analyzer import analyze_mood_with_score

# Define schema
class MoodInput(pw.Schema):
    text: str

# Watch CSV file in streaming mode
table = pw.io.csv.read(
    "data/mood_data.csv",
    schema=MoodInput,
    mode="streaming"
)

# Automatically apply mood analysis when new row arrives
result = table.select(
    text=table.text,
    mood=pw.apply(lambda t: analyze_mood_with_score(t)[0], table.text),
    score=pw.apply(lambda t: analyze_mood_with_score(t)[1], table.text)
)

# Output processed stream
pw.io.csv.write(result, "data/pathway_output.csv")

pw.run()
