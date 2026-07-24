import asyncio
import threading
from crewai import Crew, Process
from agents import destination_researcher, budget_analyst, itinerary_planner, transport_finder
from tasks import research_task, budget_task, itinerary_task, transport_task

def _run_crew_in_thread(inputs, result_holder):
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        trip_crew = Crew(
            agents=[destination_researcher, budget_analyst, transport_finder, itinerary_planner],
            tasks=[research_task, budget_task, transport_task, itinerary_task],
            process=Process.sequential,
            verbose=True,
        )
        result_holder["result"] = trip_crew.kickoff(inputs=inputs)
    except Exception as e:
        result_holder["error"] = str(e)

def run_trip_planner(origin, destination, travel_date, duration_days, num_people, budget_level, interests):
    inputs = {
        "origin": origin,
        "destination": destination,
        "travel_date": str(travel_date),
        "duration_days": duration_days,
        "num_people": num_people,
        "budget_level": budget_level,
        "interests": interests,
    }

    result_holder = {}
    thread = threading.Thread(target=_run_crew_in_thread, args=(inputs, result_holder))
    thread.start()
    thread.join()

    if "error" in result_holder:
        raise RuntimeError(f"Crew execution failed: {result_holder['error']}")

    return {
        "research": research_task.output.raw,
        "budget": budget_task.output.raw,
        "transport": transport_task.output.raw,
        "itinerary": itinerary_task.output.raw,
        "final": str(result_holder["result"]),
    }