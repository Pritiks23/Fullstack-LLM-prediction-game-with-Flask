# TODO: Import render_template from flask
from flask import Blueprint, request, jsonify
from app.game import get_daily_prompt
from app.llm import get_llm_response_words
from app.scorer import score_guess
from app.leaderboard import submit_score, get_leaderboard

routes = Blueprint('routes', __name__)

# TODO: Add a route decorator for the root URL ("/") that accepts GET requests
# TODO: Define an index function that returns the rendered index.html template

@routes.route("/game", methods=["GET"])
def game_data():
    """
    Returns today's prompt, LLM-generated response words, and predefined breakpoints.
    Used by frontend to build the game.
    """
    prompt = get_daily_prompt()
    
    words = get_llm_response_words(
        system_prompt=prompt["system_prompt"],
        user_question=prompt["user_question"],
        model=prompt.get("llm", "gpt-4o")
    )

    return jsonify({
        "prompt": {
            "llm": prompt["llm"],
            "system_prompt": prompt["system_prompt"],
            "user_question": prompt["user_question"]
        },
        "words": words,
        "breakpoints": prompt.get("breakpoints", [])
    })


@routes.route("/submit_guess", methods=["POST"])
def submit_guess():
    """
    Receives a user guess and correct word; returns a similarity score.
    """
    data = request.json
    guess = data.get("guess", "")
    correct = data.get("correct", "")

    score = score_guess(guess, correct)
    return jsonify({"score": score})


@routes.route("/submit_score", methods=["POST"])
def submit_total_score():
    """
    Stores the final score submitted by a player.
    """
    data = request.json
    name = data.get("name")
    score = data.get("score")

    if not name or score is None:
        return jsonify({"error": "Missing name or score."}), 400

    submit_score(name=name, score=score)
    return jsonify({"success": True})


@routes.route("/leaderboard", methods=["GET"])
def leaderboard():
    """
    Returns today's leaderboard scores.
    """
    scores = get_leaderboard()
    return jsonify({"scores": scores})
