# CrewAI Agent Deployment

FastAPI service for running a CrewAI research agent. The model is configured from `.env`, and the app can run locally or through Docker Compose.

## Project Structure

```text
.
|-- agents/
|   |-- __init__.py
|   `-- agent.py
|-- database/
|   |-- __init__.py
|   |-- database.py
|   `-- models.py
|-- api/
|   |-- __init__.py
|   `-- main.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- test.sh
`-- .env.example
```

## Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then update the values:

```env
MODEL_NAME=groq/llama-3.3-70b-versatile
MODEL_MAX_TOKENS=1024
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
ENABLE_SERPER_TOOL=false

POSTGRES_DB=crewai
POSTGRES_USER=crewai
POSTGRES_PASSWORD=crewai_password
DATABASE_URL=postgresql://crewai:crewai_password@postgres:5432/crewai
```

`MODEL_NAME` is passed directly to CrewAI as the agent LLM. For Groq models, keep the `groq/...` format and provide `GROQ_API_KEY`.

`MODEL_MAX_TOKENS` controls the maximum number of output tokens the model can generate.

`ENABLE_SERPER_TOOL` controls internet search. It defaults to `false` because some Groq models can fail during CrewAI tool/function calls with `tool_use_failed`. Set it to `true` only when you want the Serper search tool enabled.

Inside Docker, the API connects to Postgres with host `postgres` and port `5432`. From your host machine, Postgres is exposed on port `5433`.

## Run With Docker Compose

Build and start the API and Postgres:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Postgres will be available from your host machine at:

```text
localhost:5433
```

Stop the services:

```bash
docker compose down
```

Stop the services and delete the Postgres volume:

```bash
docker compose down -v
```

## API Endpoints

Health check:

```bash
curl http://localhost:8000/health
```

Database health check:

```bash
curl http://localhost:8000/health/db
```

Chat with the agent:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Research latest AI agent deployment patterns"}'
```

The `/chat` endpoint stores each request and response in the `chat_messages` table.

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
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

If you run the API outside Docker but Postgres inside Docker, use this local database URL:

```env
DATABASE_URL=postgresql://crewai:crewai_password@localhost:5433/crewai
```

## Notes

- `.env` is ignored by git so secrets do not get committed.
- `SERPER_API_KEY` is required because the agent uses `SerperDevTool`.
- Postgres data is persisted in the `postgres-data` Docker volume.
- Chat history is stored in the `chat_messages` table.
- If `curl` returns `Empty reply from server`, check the Docker logs:

```bash
docker compose logs -f
```
