from cli2.crew import TravelPlannerCrew

def run():
    """
    Run the crew.
    """
    region = input("What is your preferred region or destination? (e.g., Europe, Japan): ")
    trip_type = input("What type of trip are you looking for? (e.g., budget-friendly, luxury, adventure): ")

    inputs = {
        'region': region,
        'trip_type': trip_type
    }
    
    TravelPlannerCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()