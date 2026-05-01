import os

from crewai import Agent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv


load_dotenv()

research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    llm=os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile"),
    backstory="You are an experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True,
)
