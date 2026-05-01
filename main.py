import asyncio

from crewai import Crew, Task
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

from agents.agent import research_agent


load_dotenv()

app = FastAPI(title="CrewAI Agent API")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    input: str
    output: str


@app.get("/health")
def health():
    return {"status": "ok"}


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
async def chat(req: ChatRequest):
    output = await asyncio.to_thread(run_agent, req.message)
    return {"input": req.message, "output": output}
