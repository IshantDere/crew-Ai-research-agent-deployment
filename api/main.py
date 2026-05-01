import asyncio

from crewai import Crew, Task
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from agents.agent import research_agent
from database.database import create_tables, get_db
from database.models import ChatMessage


load_dotenv()

app = FastAPI(title="CrewAI Agent API")


@app.on_event("startup")
def on_startup():
    create_tables()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    input: str
    output: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


def run_agent(message: str) -> str:
    task = Task(
        description=(
            "Research and answer the user's request clearly and concisely.\n\n"
            f"User request: {message}"
        ),
        expected_output="A clear, useful response to the user's request.",
        agent=research_agent,
    )
    crew = Crew(
        agents=[research_agent],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    return str(result)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    output = await asyncio.to_thread(run_agent, req.message)
    db.add(ChatMessage(input=req.message, output=output))
    db.commit()
    return {"input": req.message, "output": output}
