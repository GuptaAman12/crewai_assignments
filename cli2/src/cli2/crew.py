from cli2.tools.custom_tool import FileSaverTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class TravelPlannerCrew():
    """TravelPlannerCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @tool
    def file_saver(self) -> FileSaverTool:
        return FileSaverTool()

    @agent
    def destination_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['destination_expert'],
            verbose=True
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_planner'],
            verbose=True
        )

    @agent
    def budget_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_advisor'],
            verbose=True
        )

    @task
    def suggest_destinations(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_destinations'],
            agent=self.destination_expert()
        )

    @task
    def plan_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config['plan_itinerary'],
            agent=self.itinerary_planner()
        )

    @task
    def estimate_budget(self) -> Task:
        return Task(
            config=self.tasks_config['estimate_budget'],
            agent=self.budget_advisor(),
            output_file='outputs/trip_plan.txt'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )