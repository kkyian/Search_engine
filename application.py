# application.py

import os
from bot import app

if __name__ == "__main__":
    # Allow running locally with `python application.py`
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5000))
    # `debug=True` is optional for local development
    app.run(host=host, port=port, debug=True)
