# api_server.py

import os
from flask import Flask, request, jsonify
from search_web import search_web

# Initialize Flask application
app = Flask(__name__)

@app.route('/api/search', methods=['GET', 'POST'])
def api_search():
    """
    JSON API endpoint for search queries.
    Supports both GET and POST:

    GET:  /api/search?q=your+query
    POST: /api/search  with JSON body {"q": "your query"}

    Returns JSON:
      {
        "query": "...",
        "results": [
          {"url": "...", "snippet": "..."},
          ...
        ]
      }
    """
    # Determine query parameter from GET or POST
    q = None
    if request.method == 'GET':
        q = request.args.get('q', '').strip()
    else:  # POST
        data = request.get_json(silent=True) or {}
        q = data.get('q', '').strip() if isinstance(data, dict) else ''

    if not q:
        return jsonify({'error': "Missing 'q' parameter in request"}), 400

    try:
        hits = search_web(q)
        data = [{'url': url, 'snippet': snippet} for url, snippet in hits]
        return jsonify({'query': q, 'results': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Bind to PORT for production or default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
