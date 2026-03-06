# Quotes Recommendation Chatbot (Rasa NLP + Flask)

A fully working quote recommendation chatbot with:
- Rasa NLU for intent detection
- Rule/story-based dialogue flow
- Flask web chat interface
- Docker setup for cross-machine execution

This project is configured so it can run on any PC/laptop with Docker installed.

## Features
- Intents: `greet`, `motivation`, `inspiration`, `love`, `funny`, `success`, `satisfied`, `not_satisfied`, `thanks`, `goodbye`
- Contextual quote replies with follow-up feedback (`yes/no`)
- Browser-based chat UI
- Automated model training on first startup
- Test stories for validation

## Project Structure

```text
CHATBOT/
├── actions/
├── data/
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── models/
├── scripts/
│   └── start_rasa.sh
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_stories.yml
├── app.py
├── config.yml
├── credentials.yml
├── docker-compose.yml
├── Dockerfile.web
├── domain.yml
├── endpoints.yml
├── requirements.txt
└── README.md
```

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

## Run on Any PC/Laptop (Recommended)

```bash
git clone https://github.com/Arpit955-ux/CHATBOT.git
cd CHATBOT
./run.sh
```

Direct one-command run:
- macOS/Linux:
```bash
./run.sh
```
- Windows:
```bat
run.bat
```

Manual alternative:
```bash
docker compose up --build
```

What happens:
- Rasa container starts.
- If no model exists, it runs `rasa train` automatically.
- Flask web app starts and connects to Rasa REST API.

Open in browser:
- UI: [http://localhost:5000](http://localhost:5000)
- Rasa API: [http://localhost:5005](http://localhost:5005)

Stop:
```bash
docker compose down
```

## Test the Bot

1. Open [http://localhost:5000](http://localhost:5000)
2. Try messages like:
- `hi`
- `inspirational quote`
- `motivational quote`
- `funny quote`
- `yes`
- `no`
- `bye`

## Optional: Local Development (Advanced)
If you want to run without Docker, install Rasa from official docs first:
- [Rasa Installation Docs](https://rasa.com/docs/rasa/installation/)

Then run:
```bash
# terminal 1
rasa train
rasa run --enable-api --cors "*" --port 5005

# terminal 2
pip install -r requirements.txt
python app.py
```

## Workflow Mapping (Milestones)

### Milestone 1: Problem Understanding
- Business problem identified: manual quote discovery is slow and non-personalized.
- Requirements defined: intent accuracy, engagement, and web accessibility.

### Milestone 2: Environment Setup
- Rasa project structure prepared.
- Docker-based environment added for portability.

### Milestone 3: Data & Model Building
- `data/nlu.yml`: training examples and intents.
- `domain.yml`: response templates.
- `data/stories.yml` + `data/rules.yml`: dialogue logic.
- Model training and storage in `models/`.

### Milestone 4: Testing & Deployment
- CLI testing with Rasa shell (optional).
- Test stories in `tests/test_stories.yml`.
- Web deployment via Flask + Rasa REST API.

## Common Fixes
1. `Web page loads but bot gives no response`
- Ensure Rasa service is running on port `5005`.
- If using Docker, verify both containers are up: `docker compose ps`.
- Check logs:
  - `docker compose logs rasa`
  - `docker compose logs web`

2. `Port already in use`
- Stop conflicting services or change mapped ports in `docker-compose.yml`.

3. `Model not found`
- Delete old/broken files in `models/` and restart:
  - `docker compose down`
  - `docker compose up --build`

4. `run.sh` / `run.bat` fails immediately
- Start Docker Desktop first.
- Wait until Docker is fully running.
- Retry `./run.sh` (Linux/macOS) or `run.bat` (Windows).

## Future Enhancements
- Emotion detection with sentiment models
- Personalized quote ranking from user history
- Multilingual support
- Voice input/output
- Messaging app integrations (WhatsApp/Telegram)
- External quote API integration
- Analytics dashboard

## GitHub Push

```bash
git add .
git commit -m "Build complete Quotes Recommendation Chatbot with Rasa, Flask UI, Docker, and README"
git push origin main
```
