# CrewAI Agent Deployment

FastAPI service for running a CrewAI research agent. The model is configured from `.env`, and the app can run locally or through Docker Compose.

## Project Structure

```text
.
├── agents/
│   ├── __init__.py
│   └── agent.py
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── test.sh
└── .env.example
```

## Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then update the values:

```env
MODEL_NAME=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

`MODEL_NAME` is passed directly to CrewAI as the agent LLM. For Groq models, keep the `groq/...` format and provide `GROQ_API_KEY`.

## Run With Docker Compose

Build and start the API:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Stop the service:

```bash
docker compose down
```

## API Endpoints

Health check:

```bash
curl http://localhost:8000/health
```

Chat with the agent:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Research latest AI agent deployment patterns"}'
```

PowerShell example:

```powershell
curl.exe -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d "{\"message\":\"Research latest AI agent deployment patterns\"}"
```

## Test Script

After the server is running, test both `/health` and `/chat`:

```bash
bash test.sh
```

## Run Locally Without Docker

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes

- `.env` is ignored by git so secrets do not get committed.
- `SERPER_API_KEY` is required because the agent uses `SerperDevTool`.
- If `curl` returns `Empty reply from server`, check the Docker logs:

```bash
docker compose logs -f
```
