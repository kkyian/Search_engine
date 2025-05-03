# handler.py
from search_web import search_web

def handle_message(user_msg: str, llm_fallback):
    """
    If the user starts with "search:", do a web lookup.
    Otherwise delegate to an LLM or other chatbot logic.
    """
    if user_msg.lower().startswith("search:"):
        query = user_msg.split(":", 1)[1].strip()
        hits = search_web(query)
        if not hits:
            return "Sorry, I couldn't find any results for that."
        # build a markdown-style reply
        reply = "Here are the top results I found:\n\n"
        for url, snippet in hits:
            reply += f"- **{url}**\n  {snippet}\n\n"
        return reply
    else:
        # your existing chatbot or LLM call
        return llm_fallback(user_msg)
