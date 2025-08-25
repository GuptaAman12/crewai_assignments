from cli1.tools.custom_tool import FileSaverTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Mycrew():
    """Mycrew crew"""
    agents: List[BaseAgent]
    tasks: List[Task]

    @tool
    def file_saver(self) -> FileSaverTool:
        return FileSaverTool()
    
    @agent
    def problem_setter(self) -> Agent:
        return Agent(
            config=self.agents_config['problem_setter'],
            verbose=True
        )

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True
        )

    @task
    def define_problem(self) -> Task:
        return Task(
            config=self.tasks_config['define_problem'],
        )

    @task
    def generate_code(self) -> Task:
        return Task(
            config=self.tasks_config['generate_code'],
            output_file='outputs/solution.py'
        )

    @task
    def review_code(self) -> Task:
        return Task(
            config=self.tasks_config['review_code'],
            output_file='outputs/review.txt'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )