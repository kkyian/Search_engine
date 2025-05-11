# bot.py

import os
import argparse
from handler import handle_message
from flask import Flask, request, render_template

# Flask application setup
app = Flask(__name__, template_folder="templates")

def dummy_llm(msg: str) -> str:
    """
    Placeholder LLM function for non-search queries.
    """
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

def run_web(host: str = '0.0.0.0', port: int = 5000):
    """
    Run the Flask dev server, binding to the given host and port.
    """
    # Allow overriding via environment if not passed explicitly
    port_env = os.environ.get("PORT")
    effective_port = port if port_env is None else int(port_env)
    app.run(host=host, port=effective_port, debug=True)

def run_cli():
    """
    Run a simple CLI loop for chat.
    """
    print("Search-Chatbot CLI (type 'exit' to quit)")
    while True:
        msg = input("You: ")
        if msg.lower() in ("exit", "quit"):
            break
        print(handle_message(msg, dummy_llm))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Search-Enabled Chatbot")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--web", action="store_true", help="Run in web (Flask) mode")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the web server to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind the web server to")
    args = parser.parse_args()

    if args.web:
        run_web(host=args.host, port=args.port)
    else:
        run_cli()