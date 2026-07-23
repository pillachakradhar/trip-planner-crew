import asyncio
import threading
from crewai import Crew, Process
from agents import destination_researcher, budget_analyst, itinerary_planner
from tasks import research_task, budget_task, itinerary_task

def _run_crew_in_thread(inputs, result_holder):
    asyncio.set_event_loop(asyncio.new_event_loop())
    trip_crew = Crew(
        agents=[destination_researcher, budget_analyst, itinerary_planner],
        tasks=[research_task, budget_task, itinerary_task],
        process=Process.sequential,
        verbose=True,
    )
    result_holder["result"] = trip_crew.kickoff(inputs=inputs)

def run_trip_planner(destination, duration_days, num_people, budget_level, interests):
    inputs = {
        "destination": destination,
        "duration_days": duration_days,
        "num_people": num_people,
        "budget_level": budget_level,
        "interests": interests,
    }

    result_holder = {}
    thread = threading.Thread(target=_run_crew_in_thread, args=(inputs, result_holder))
    thread.start()
    thread.join()

    return {
        "research": research_task.output.raw,
        "budget": budget_task.output.raw,
        "itinerary": itinerary_task.output.raw,
        "final": str(result_holder["result"]),
    }