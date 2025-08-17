from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# In-memory storage for simplicity (replace with a DB in production)
leaderboard = []

# Example game data
example_prompts = [
    {
        "llm": "GPT-4",
        "system_prompt": "Complete the sentence predictively.",
        "user_question": "Predict the next words in this sentence:"
    },
    {
        "llm": "GPT-5",
        "system_prompt": "Finish the following text intelligently.",
        "user_question": "Next token prediction:"
    }
]

example_words = [
    "The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"
]

example_breakpoints = [2, 5]  # User guesses after word 2 and 5

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    prompt = random.choice(example_prompts)
    
    # Shuffle words to make it slightly dynamic (optional)
    words = example_words.copy()
    
    return jsonify({
        "prompt": prompt,
        "words": words,
        "breakpoints": example_breakpoints
    })

@app.route("/submit_guess", methods=["POST"])
def submit_guess():
    data = request.get_json()
    guess = data.get("guess", "").lower()
    correct = data.get("correct", "").lower()
    
    # Simple scoring: +10 if exact match, else 0
    score = 10 if guess == correct else 0
    
    return jsonify({"score": score})

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name", "Anonymous")
    score = data.get("score", 0)
    
    leaderboard.append({"name": name, "score": score})
    
    # Sort leaderboard descending
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    
    return jsonify({"status": "ok"})

@app.route("/leaderboard")
def get_leaderboard():
    # Return top 10 scores
    top_scores = leaderboard[:10]
    return jsonify({"scores": top_scores})

if __name__ == "__main__":
    app.run(debug=True)
