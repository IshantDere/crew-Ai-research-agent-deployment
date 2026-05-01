import os

from crewai import Agent, LLM
from dotenv import load_dotenv


load_dotenv()


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def get_tools():
    if not env_flag("ENABLE_SERPER_TOOL"):
        return []

    from crewai_tools import SerperDevTool

    return [SerperDevTool()]


def get_llm() -> LLM:
    model_name = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")
    max_tokens = int(os.getenv("MODEL_MAX_TOKENS", "1024"))
    return LLM(model=model_name, max_tokens=max_tokens)


research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    llm=get_llm(),
    backstory=(
        "You are an experienced researcher with attention to detail. "
        "Answer directly from your knowledge unless an available tool is needed."
    ),
    tools=get_tools(),
    verbose=True,
)
