import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'super_agent'))
from super_agent.super_agent_loop import SuperAgentLoop

def main():
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found.")
        return

    agent = SuperAgentLoop(api_key=api_key)
    
    # Check if a specific goal was passed via env or args
    goal = os.getenv("AGENT_GOAL", "Analyze the codebase, improve performance, and ensure memory management is working correctly.")
    
    agent.run_iteration(goal=goal)

if __name__ == "__main__":
    main()
