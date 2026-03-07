# Quotes Recommendation Chatbot (Rasa NLP + Flask)

This project now supports two run modes:
- Docker + Rasa mode (full Rasa pipeline)
- Direct local mode (built-in NLP fallback, no Docker required)

If Docker is missing, `run.sh` / `run.bat` will automatically switch to local mode.

## Features
- Quote categories: Inspiration, Motivation, Success, Love, Funny
- Conversational feedback flow (`yes` / `no`)
- Web chat UI on localhost (default `http://localhost:5000`, auto-switches if busy)
- Rasa API integration when available
- Local fallback NLP so the app still runs if Rasa is unavailable

## Project Structure

```text
CHATBOT/
├── data/
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── docker-compose.yml
├── domain.yml
├── requirements.txt
├── run.sh
├── run.bat
├── run_local.sh
└── run_local.bat
```

## Quick Start (Any PC/Laptop)

```bash
git clone https://github.com/Arpit955-ux/CHATBOT.git
cd CHATBOT
./run.sh
```

Windows:
```bat
run.bat
```

Open the URL printed in terminal.
- Default: [http://localhost:5000](http://localhost:5000)
- Also valid on loopback: [http://127.0.0.1:5001](http://127.0.0.1:5001) (if script selected port `5001`)
- If `5000` is busy, scripts auto-select next free port (for example `5001` or `5002`)

## Mode Details

### 1) Docker + Rasa Mode
Used automatically when Docker is available.

```bash
docker compose up --build
```

Services:
- Web UI: URL printed in terminal (default `http://localhost:5000`)
- Rasa API: `http://localhost:5005`

### 2) Local NLP Mode (No Docker)
Used automatically when Docker is not available.

```bash
./run_local.sh
```

Windows:
```bat
run_local.bat
```

This mode uses built-in intent detection inside `app.py` and does not require Rasa.

Custom local port:
```bash
FLASK_PORT=5050 ./run_local.sh
```

Custom Docker web port:
```bash
WEB_PORT=5050 ./run.sh
```

## Prerequisites

### For Docker + Rasa mode
- Docker Desktop
- Git

### For local mode
- Python 3.10+
- Git

## Troubleshooting

1. `zsh: command not found: docker`
- Run local mode directly: `./run_local.sh`
- Or install Docker Desktop and retry `./run.sh`

2. Browser opens but no reply
- Ensure backend is running and terminal has no crash logs.
- Retry with local mode: `FORCE_LOCAL_NLP=1 python app.py`

3. Port already in use
- macOS/Linux:
```bash
lsof -i :5000
kill -9 <PID>
```
- Or just run `./run.sh` / `./run_local.sh`; they auto-pick a free port.
- Always use the exact localhost URL shown in the startup logs.

## Optional Full Rasa Local Development
If you specifically want local Rasa without Docker, install Rasa from official docs:
- [Rasa Installation](https://rasa.com/docs/rasa/installation/)

Then run in two terminals:
```bash
# terminal 1
rasa train
rasa run --enable-api --cors "*" --port 5005

# terminal 2
pip install -r requirements.txt
python app.py
```

## Publish To GitHub (Fixes `refspec` and auth errors)

If you see:
- `src refspec main does not match any`
- `Permission denied ... 403`

Run:

```bash
git add .
git commit -m "Initial chatbot setup"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Arpit955-ux/CHATBOT.git
git push -u origin HEAD:main
```

If push returns `403`, your current GitHub account does not have write access.
Use a Personal Access Token (PAT) from the repo owner account and push again:

```bash
git remote set-url origin https://<GITHUB_USERNAME>:<GITHUB_PAT>@github.com/Arpit955-ux/CHATBOT.git
git push -u origin HEAD:main
```

Or run:

```bash
./push_github.sh
```
