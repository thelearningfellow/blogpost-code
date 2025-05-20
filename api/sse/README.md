To run this application:

1. Make sure you have a `templates` directory with `index.html` (from the next block) inside it.
2. Create venv and install dependencies:
    ```bash
    python -m venv .venv
    .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run from your terminal: `uvicorn sse:app --reload`
4. Open your browser to http://127.0.0.1:8000/