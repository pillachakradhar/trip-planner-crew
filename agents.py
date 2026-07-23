from crewai import Agent, LLM
from crewai_tools import SerperDevTool
import os

search_tool = SerperDevTool()

gemini_llm = LLM(
    model="gemini/gemini-flash-lite-latest",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5,
)

destination_researcher = Agent(
    role="Destination Researcher",
    goal="Find the best attractions, activities, and practical tips for {destination}",
    backstory=(
        "You are a well-traveled expert who knows how to find hidden gems "
        "and practical, up-to-date travel information for any destination."
    ),
    tools=[search_tool],
    llm=gemini_llm,          # <- add this
    verbose=True,
    allow_delegation=False,
)

budget_analyst = Agent(
    role="Budget Analyst",
    goal=(
        "Estimate realistic costs for a {duration_days}-day trip to {destination} "
        "for {num_people} people at a {budget_level} budget level"
    ),
    backstory=(
        "You are a meticulous financial planner specializing in travel budgets, "
        "skilled at estimating flights, accommodation, food, and activity costs "
        "for both individuals and groups."
    ),
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

itinerary_planner = Agent(
    role="Itinerary Planner",
    goal="Create a detailed, realistic day-by-day itinerary for {destination}",
    backstory=(
        "You are a professional travel planner who excels at organizing "
        "activities into logical, well-paced daily schedules."
    ),
    llm=gemini_llm,          # <- add this
    verbose=True,
    allow_delegation=False,
)