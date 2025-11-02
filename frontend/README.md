# Frontend chat demo

This is a small text-based chat demo using a lightweight Python/Flask backend that serves a single-page UI.

How to run

1. Create a virtualenv and install dependencies (from requirements.txt`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r frontend/requirements.txt
```

2. Start the app

```bash
python frontend/app.py
```

3. Open http://127.0.0.1:5000 in your browser.

Notes

- The backend uses a tiny rule-based `generate_reply` function. You can replace it with more advanced logic (call into `bot.py` or an external API) if desired.
