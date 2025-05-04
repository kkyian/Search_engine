# bot.py
import argparse

def dummy_llm(msg):
    return "🤖 (echo) " + msg

def run_cli():
    from handler import handle_message
    print("Search-Chatbot CLI (type ‘exit’ to quit)")
    while True:
        msg = input("You: ")
        if msg.lower() in ("exit", "quit"):
            break
        print(handle_message(msg, dummy_llm))

def run_web(host="127.0.0.1", port=5000):
    from flask import Flask, request, render_template
    from handler import handle_message
    app = Flask(__name__, template_folder="templates")

    @app.route("/", methods=["GET", "POST"])
    def home():
        result = ""
        if request.method == "POST":
            result = handle_message(request.form["q"], dummy_llm)
        return render_template("index.html", result=result)

    app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cli", action="store_true")
    p.add_argument("--web", action="store_true")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5000)
    args = p.parse_args()

    if args.web:
        run_web(host=args.host, port=args.port)
    else:
        run_cli()

