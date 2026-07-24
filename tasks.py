from crewai import Task
from agents import destination_researcher, budget_analyst, itinerary_planner, transport_finder

research_task = Task(
    description=(
        "Research {destination} for a trip focused on {interests}. "
        "Find top attractions, best neighborhoods to stay in, local tips, "
        "and the best time of year to visit. Be specific and current."
    ),
    expected_output=(
        "A structured list of 8-10 attractions/activities with 1-2 sentence "
        "descriptions, plus 3-4 practical travel tips."
    ),
    agent=destination_researcher,
)

budget_task = Task(
    description=(
        "Estimate a realistic budget for {duration_days} days in {destination} "
        "for a group of {num_people} people, at a {budget_level} level. Break down "
        "flights, accommodation, food, local transport, and activities. Give both "
        "the per-person cost and the total cost for the whole group."
    ),
    expected_output=(
        "A cost breakdown by category with a per-person daily average, a total "
        "cost for {num_people} people, and a grand total estimate, in USD."
    ),
    agent=budget_analyst,
)

itinerary_task = Task(
    description=(
        "Using the research and budget information, create a day-by-day "
        "itinerary for {duration_days} days in {destination}. Group nearby "
        "attractions together to minimize travel time. Include a rough daily "
        "cost alongside each day."
    ),
    expected_output=(
        "A day-by-day itinerary (Day 1, Day 2, etc.) with morning/afternoon/"
        "evening activities and an estimated daily cost, formatted in markdown."
    ),
    agent=itinerary_planner,
    context=[research_task, budget_task],  # <- this is the key line
    output_file="itinerary.md",
)
transport_task = Task(
    description=(
        "Research transport options from {origin} to {destination} for a trip "
        "starting around {travel_date}. Cover flights (airlines that fly this "
        "route, typical duration), trains (if applicable for this route), buses, "
        "and cruises (if it's a coastal/island destination). Note typical price "
        "ranges if available, but do not attempt to check live seat availability "
        "or exact prices."
    ),
    expected_output=(
        "A breakdown by transport mode (Flights / Trains / Buses / Cruises) with "
        "2-3 options or airlines/operators per mode, approximate journey time, "
        "and general price range, in markdown."
    ),
    agent=transport_finder,
)