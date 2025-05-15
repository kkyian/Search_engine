# bot.py

import os
import argparse
from handler import handle_message
from flask import Flask, request, render_template

# Initialize Flask application
app = Flask(__name__, template_folder="templates")

# Simple fallback LLM for non-search queries
def dummy_llm(msg: str) -> str:
    return "🤖 (echo) " + msg

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Web endpoint: render chat UI and handle form submissions.
    """
    result = ""
    if request.method == "POST":
        user_input = request.form.get("q", "")
        result = handle_message(user_input, dummy_llm)
    return render_template("index.html", result=result)

# CLI chat loop
def run_cli():
    print("Search-Chatbot CLI (type 'exit' to quit)")
    while True:
        msg = input("You: ")
        if msg.lower() in ("exit", "quit"):
            break
        print(handle_message(msg, dummy_llm))

# Web server runner
def run_web(host: str, port: int):
    """
    Run the Flask server on the given host and port.
    """
    app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Search-Enabled Chatbot")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--web", action="store_true", help="Run in web (Flask) mode")
    parser.add_argument(
        "--host", default="0.0.0.0",
        help="Host interface to bind the web server to"
    )
    parser.add_argument(
        "--port", type=int,
        default=int(os.environ.get("PORT", 5000)),
        help="Port to bind the web server to"
    )
    args = parser.parse_args()

    if args.web:
        run_web(args.host, args.port)
    else:
        run_cli()
