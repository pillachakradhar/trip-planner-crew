from dotenv import load_dotenv
load_dotenv()

from crew import trip_crew

inputs = {
    "destination": "Kyoto, Japan",
    "duration_days": 4,
    "budget_level": "mid-range",
    "interests": "history, food, and quiet temples",
}

result = trip_crew.kickoff(inputs=inputs)

print("\n\n=== FINAL ITINERARY ===\n")
print(result)