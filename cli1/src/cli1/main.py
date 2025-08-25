import sys
import warnings
from cli1.crew import Mycrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    user_input = input("Your query?: ")
    inputs = {
        'user_query': user_input
    }
    try:
        Mycrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    inputs = {'user_query': 'Implement bubble sort in python'}
    try:
        Mycrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        Mycrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {'user_query': 'Implement bubble sort in python'}
    try:
        Mycrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")